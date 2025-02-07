from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactBase
from src.database.models import User


class ContactService:
    """
    Service layer for handling contact-related operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the ContactService.

        Args:
            db: Database session dependency.
        """
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User):
        """
        Create a new contact for the given user.

        Args:
            body: ContactBase object containing contact details.
            user: The authenticated user creating the contact.

        Returns:
            The newly created contact object.
        """
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, user: User):
        """
        Retrieve a list of contacts for the given user with pagination.

        Args:
            skip: Number of contacts to skip.
            limit: Maximum number of contacts to return.
            user: The authenticated user retrieving the contacts.

        Returns:
            A list of contact objects.
        """
        return await self.contact_repository.get_contacts(skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        """
        Retrieve a specific contact by ID.

        Args:
            contact_id: The ID of the contact to retrieve.
            user: The authenticated user retrieving the contact.

        Returns:
            The contact object if found, otherwise None.
        """
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactBase, user: User):
        """
        Update an existing contact for the given user.

        Args:
            contact_id: The ID of the contact to update.
            body: ContactBase object containing updated details.
            user: The authenticated user updating the contact.

        Returns:
            The updated contact object if found, otherwise None.
        """
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Delete a specific contact by ID.

        Args:
            contact_id: The ID of the contact to delete.
            user: The authenticated user deleting the contact.

        Returns:
            The deleted contact object if found, otherwise None.
        """
        return await self.contact_repository.remove_contact(contact_id, user)

    async def search_contacts(self, search: int, skip: int, limit: int, user: User):
        """
        Search for contacts based on a query string.

        Args:
            search: The search query string.
            skip: Number of contacts to skip.
            limit: Maximum number of contacts to return.
            user: The authenticated user performing the search.

        Returns:
            A list of matching contact objects.
        """
        return await self.contact_repository.search_contacts(search, skip, limit, user)

    async def get_week_birthdays(self, days: int, user: User):
        """
        Retrieve contacts with upcoming birthdays within a given number of days.

        Args:
            days: The number of days to check for upcoming birthdays.
            user: The authenticated user retrieving the birthday list.

        Returns:
            A list of contacts with upcoming birthdays.
        """
        return await self.contact_repository.get_week_birthdays(days, user)
