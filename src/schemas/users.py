from pydantic import BaseModel, ConfigDict, EmailStr
from src.database.models import UserRole

"""
Defines Pydantic schemas for user-related operations.
"""


class User(BaseModel):
    """
    Schema for returning user information.
    """

    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Schema for user registration request.
    """

    username: str
    email: str
    password: str
    role: UserRole


class Token(BaseModel):
    """
    Schema for authentication token response.
    """

    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    """
    Schema for requesting email verification.
    """

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """
    Schema for requesting a password reset.
    """

    email: EmailStr


class ResetPassword(BaseModel):
    """
    Schema for resetting the password using a token.
    """

    token: str
    new_password: str
