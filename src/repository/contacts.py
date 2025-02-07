from typing import List
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, or_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contacts import ContactBase


class ContactRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize a ContactRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_contacts(self, skip: int, limit: int, user: User) -> List[Contact]:
        """
        Retrieve a paginated list of contacts owned by a user.

        Args:
            skip: Number of contacts to skip.
            limit: Maximum number of contacts to return.
            user: The owner of the contacts.

        Returns:
            A list of Contact objects.
        """
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """
        Retrieve a contact by its ID.

        Args:
            contact_id: The ID of the contact to retrieve.
            user: The owner of the contact.

        Returns:
            The Contact object if found, otherwise None.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        """
        Create a new contact.

        Args:
            body: A ContactBase object containing contact details.
            user: The owner of the new contact.

        Returns:
            The newly created Contact object.
        """
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id, user)

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """
        Delete a contact by its ID.

        Args:
            contact_id: The ID of the contact to delete.
            user: The owner of the contact.

        Returns:
            The deleted Contact object if found, otherwise None.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactBase, user: User
    ) -> Contact | None:
        """
        Update a contact's details.

        Args:
            contact_id: The ID of the contact to update.
            body: A ContactBase object with updated contact details.
            user: The owner of the contact.

        Returns:
            The updated Contact object if found, otherwise None.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in body.dict(exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def search_contacts(
        self, search: str, skip: int, limit: int, user: User
    ) -> List[Contact]:
        """
        Search for contacts by first name, last name, or email.

        Args:
            search: The search query string.
            skip: Number of contacts to skip.
            limit: Maximum number of contacts to return.
            user: The owner of the contacts.

        Returns:
            A list of matching Contact objects.
        """
        stmt = (
            select(Contact)
            .filter(
                Contact.user == user,
                or_(
                    Contact.first_name.ilike(f"%{search}%"),
                    Contact.last_name.ilike(f"%{search}%"),
                    Contact.email.ilike(f"%{search}%"),
                ),
            )
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_week_birthdays(self, days: int, user: User) -> List[Contact]:
        """
        Retrieve contacts whose birthdays fall within the next given number of days.

        Args:
            days: The number of days to check for upcoming birthdays.
            user: The owner of the contacts.

        Returns:
            A list of Contact objects with birthdays within the given range.
        """
        today = datetime.now(timezone.utc).date()
        end_date = today + timedelta(days=days)

        stmt = select(Contact).filter(
            Contact.user == user,
            (extract("month", Contact.birthday) == today.month)
            & (extract("day", Contact.birthday) >= today.day)
            | (extract("month", Contact.birthday) == end_date.month)
            & (extract("day", Contact.birthday) <= end_date.day),
        )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()
