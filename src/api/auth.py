from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.users import UserCreate, Token, User, RequestEmail
from src.services.auth import (
    create_access_token,
    Hash,
    get_email_from_token,
    get_email_from_reset_token,
)
from src.services.users import UserService
from src.services.email import send_email, send_reset_password_email
from src.services.auth import get_current_admin_user
from src.database.db import get_db
from src.database.models import UserRole
from src.conf import messages

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    Args:
        user_data: UserCreate object containing user details.
        background_tasks: BackgroundTasks instance for sending email confirmation.
        request: Request object for base URL access.
        db: Database session dependency.

    Returns:
        The newly created User object.
    """
    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=messages.EMAIL_EXISTS,
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=messages.USERNAME_ALREADY_EXISTS,
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url
    )
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate and log in a user.

    Args:
        form_data: OAuth2PasswordRequestForm with login credentials.
        db: Database session dependency.

    Returns:
        Access token and token type if authentication is successful.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.WRONG_LOGIN_OR_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.EMAIL_NOT_CONFIRMED,
        )
    access_token = await create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm a user's email using a token.

    Args:
        token: The confirmation token.
        db: Database session dependency.

    Returns:
        A success message if email is confirmed.
    """
    email = await get_email_from_token(token)
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR
        )
    if user.confirmed:
        return {"message": messages.EMAIL_ALREADY_CONFIRMED}
    await user_service.confirmed_email(email)
    return {"message": messages.EMAIL_CONFIRMED}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Request an email confirmation to be resent.

    Args:
        body: RequestEmail object with user email.
        background_tasks: BackgroundTasks instance for sending email confirmation.
        request: Request object for base URL access.
        db: Database session dependency.

    Returns:
        A message indicating the email confirmation request was processed.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if user.confirmed:
        return {"message": messages.EMAIL_ALREADY_CONFIRMED}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url
        )
    return {"message": messages.CHECK_EMAIL}


@router.post("/forgot-password")
async def forgot_password(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Initiate the password reset process by sending a reset link to the user's email.

    Args:
        body: RequestEmail object containing the user's email.
        background_tasks: BackgroundTasks instance for sending the reset password email.
        request: Request object for base URL access.
        db: Database session dependency.

    Returns:
        A message indicating that the reset link has been sent.

    Raises:
        HTTPException: If the user is not found.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )

    background_tasks.add_task(
        send_reset_password_email, user.email, user.username, request.base_url
    )

    return {"message": messages.INSTRUCTION_RESET_PASSWORD}


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
):
    """
    Reset the user's password using the provided token.

    Args:
        body: ResetPassword object containing the reset token and new password.
        db: Database session dependency.

    Returns:
        A success message confirming that the password has been reset.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    email = await get_email_from_reset_token(token)
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )

    hashed_password = Hash().get_password_hash(new_password)
    await user_service.update_password(user.email, hashed_password)

    return {"message": messages.PASSWORD_CHANGED}


@router.post("/make-admin", response_model=User)
async def make_admin(
    email: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Promote a user to admin.

    Args:
        email: The email address of the user to be promoted.
        current_admin: The currently authenticated admin user (ensures only admins can perform this action).
        db: Database session dependency.

    Returns:
        The updated User object with admin role.

    Raises:
        HTTPException: If the user does not exist.
        HTTPException: If the user is already an admin.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
        )

    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_ADMIN
        )

    updated_user = await user_service.update_user_role(user, UserRole.ADMIN)
    return updated_user
