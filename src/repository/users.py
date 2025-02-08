from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, UserRole
from src.schemas.users import UserCreate


class UserRepository:
    """
    Handles database operations for the User model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize a UserRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email: The email of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def update_user_role(self, user: User, role: UserRole):
        """
        Update the role of a user.

        Args:
            user: The user object whose role is being updated.
            role: The new role to be assigned to the user.

        Returns:
            The updated user object with the new role.
        """
        user.role = role
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user.

        Args:
            body: A UserCreate object containing user details.
            avatar: An optional avatar URL for the user.

        Returns:
            The newly created User object.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Confirm a user's email address.

        Args:
            email: The email of the user to confirm.

        Returns:
            None
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Update the avatar URL of a user.

        Args:
            email: The email of the user whose avatar is to be updated.
            url: The new avatar URL.

        Returns:
            The updated User object.
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user
