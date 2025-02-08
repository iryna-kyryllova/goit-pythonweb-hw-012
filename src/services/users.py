from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas.users import UserCreate
from src.services.cache import cache
from src.database.models import UserRole, User
from src.conf import messages


class UserService:
    """
    Service layer for handling user-related operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the UserService.

        Args:
            db: Database session dependency.
        """
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Create a new user with an optional Gravatar avatar.

        Args:
            body: UserCreate object containing user details.

        Returns:
            The newly created user object.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        user = await self.repository.create_user(body, avatar)

        if user:
            await cache.set_user(user)

        return user

    async def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Retrieve a user by their email address.

        Args:
            email: The email address of the user to retrieve.

        Returns:
            The user object if found, otherwise None.
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        """
        Confirm a user's email address.

        Args:
            email: The email address of the user to confirm.

        Returns:
            None
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """
        Update a user's avatar URL.

        Args:
            email: The email address of the user whose avatar is being updated.
            url: The new avatar URL.

        Returns:
            The updated user object.
        """
        user = await self.repository.update_avatar_url(email, url)
        if user:
            await cache.delete_user(user.id)
            await cache.set_user(user)

        return user

    async def update_password(self, email: str, new_hashed_password: str):
        """
        Update the password for a user.

        Args:
            email: The email address of the user whose password is being updated.
            new_password: The new password to be set.

        Returns:
            The updated User object.
        """
        user = await self.repository.get_user_by_email(email)
        if user:
            user.hashed_password = new_hashed_password
            await self.repository.db.commit()
        return user

    async def update_user_role(self, user: User, new_role: UserRole):
        """
        Update the role of a user.

        Args:
            user: The user object whose role is being updated.
            new_role: The new role to assign to the user.

        Returns:
            The updated User object.
        """
        return await self.repository.update_user_role(user, new_role)
