from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator

"""
Defines Pydantic schemas for contact-related operations.
"""


class ContactBase(BaseModel):
    """
    Base schema for a contact, used for creating and updating contacts.
    """

    first_name: str = Field(max_length=50, min_length=2)
    last_name: str = Field(max_length=50, min_length=2)
    email: EmailStr
    phone_number: str = Field(max_length=20, min_length=6)
    birthday: date
    additional_data: Optional[str] = Field(max_length=200)

    @field_validator("birthday")
    def validate_birthday(cls, value):
        """
        Validates that the birthday is not in the future.

        Args:
            value: The provided birth date.

        Returns:
            The validated birth date.

        Raises:
            ValueError: If the birthday is in the future.
        """
        if value > date.today():
            raise ValueError("Birthday cannot be in the future")
        return value


class ContactResponse(ContactBase):
    """
    Schema for returning contact data with additional metadata.
    """

    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None
    model_config = ConfigDict(from_attributes=True)


class ContactBirthdayRequest(BaseModel):
    """
    Schema for requesting contacts with upcoming birthdays.
    """

    days: int = Field(ge=0, le=365)
