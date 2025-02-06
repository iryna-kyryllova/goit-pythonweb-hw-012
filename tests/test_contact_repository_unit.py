import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timedelta, timezone

from src.database.models import Contact, User
from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactBase

test_contact = {
    "first_name": "John",
    "last_name": "Dou",
    "email": "john@gmail.com",
    "phone_number": "+380995555555",
    "birthday": "1990-01-01",
    "additional_data": "Some extra text",
}


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser")


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(
            id=1,
            first_name=test_contact["first_name"],
            last_name=test_contact["last_name"],
            email=test_contact["email"],
            phone_number=test_contact["phone_number"],
            birthday=date.fromisoformat(test_contact["birthday"]),
            additional_data=test_contact["additional_data"],
            user=user,
        )
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    contacts = await contact_repository.get_contacts(skip=0, limit=10, user=user)

    assert len(contacts) == 1
    assert contacts[0].first_name == test_contact["first_name"]
    assert contacts[0].last_name == test_contact["last_name"]
    assert contacts[0].email == test_contact["email"]


@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1,
        first_name=test_contact["first_name"],
        last_name=test_contact["last_name"],
        email=test_contact["email"],
        phone_number=test_contact["phone_number"],
        birthday=date.fromisoformat(test_contact["birthday"]),
        additional_data=test_contact["additional_data"],
        user=user,
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    contact = await contact_repository.get_contact_by_id(contact_id=1, user=user)

    assert contact is not None
    assert contact.id == 1
    assert contact.first_name == test_contact["first_name"]
    assert contact.last_name == test_contact["last_name"]
    assert contact.email == test_contact["email"]


@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, user):
    body = ContactBase(**test_contact)

    created_contact = Contact(
        id=1,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_data=body.additional_data,
        user=user,
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = created_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await contact_repository.create_contact(body=body, user=user)

    assert isinstance(result, Contact)
    assert result.id == 1
    assert result.first_name == body.first_name
    assert result.last_name == body.last_name
    assert result.email == body.email
    assert result.phone_number == body.phone_number
    assert result.birthday == body.birthday
    assert result.additional_data == body.additional_data

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    mock_session.execute.assert_awaited()


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    existing_contact = Contact(
        id=1,
        first_name=test_contact["first_name"],
        last_name=test_contact["last_name"],
        email=test_contact["email"],
        phone_number=test_contact["phone_number"],
        birthday=date.fromisoformat(test_contact["birthday"]),
        additional_data=test_contact["additional_data"],
        user=user,
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    deleted_contact = await contact_repository.remove_contact(contact_id=1, user=user)

    assert deleted_contact is not None
    assert deleted_contact.id == 1

    mock_session.delete.assert_awaited_once_with(existing_contact)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    existing_contact = Contact(
        id=1,
        first_name=test_contact["first_name"],
        last_name=test_contact["last_name"],
        email=test_contact["email"],
        phone_number=test_contact["phone_number"],
        birthday=date.fromisoformat(test_contact["birthday"]),
        additional_data=test_contact["additional_data"],
        user=user,
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    update_data = ContactBase(
        first_name="Johnny",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="+380991112299",
        birthday=date(1991, 1, 2),
        additional_data="New info",
    )

    updated_contact = await contact_repository.update_contact(
        contact_id=1, body=update_data, user=user
    )

    assert updated_contact is not None
    assert updated_contact.first_name == "Johnny"
    assert updated_contact.last_name == "Doe"
    assert updated_contact.email == "john.doe@example.com"
    assert updated_contact.phone_number == "+380991112299"
    assert updated_contact.birthday == date(1991, 1, 2)
    assert updated_contact.additional_data == "New info"

    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_contact)


@pytest.mark.asyncio
async def test_search_contacts(contact_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(
            id=1,
            first_name=test_contact["first_name"],
            last_name=test_contact["last_name"],
            email=test_contact["email"],
            phone_number=test_contact["phone_number"],
            birthday=date.fromisoformat(test_contact["birthday"]),
            additional_data=test_contact["additional_data"],
            user=user,
        )
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    search_str = "john"
    contacts = await contact_repository.search_contacts(
        search=search_str, skip=0, limit=10, user=user
    )

    assert len(contacts) == 1
    assert contacts[0].first_name == test_contact["first_name"]
    assert contacts[0].last_name == test_contact["last_name"]
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_week_birthdays(contact_repository, mock_session, user):
    today = datetime(2025, 2, 6, tzinfo=timezone.utc).date()
    days = 7
    end_date = today + timedelta(days=days)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(
            id=1,
            first_name="John",
            last_name="Dou",
            email="john@example.com",
            phone_number="+380991112233",
            birthday=date(1990, 2, 6),
            user=user,
        ),
        Contact(
            id=2,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone_number="+380991112244",
            birthday=date(1992, 2, 10),
            user=user,
        ),
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    contacts = await contact_repository.get_week_birthdays(days=days, user=user)

    assert len(contacts) == 2
    assert contacts[0].id == 1
    assert contacts[1].id == 2
    mock_session.execute.assert_awaited_once()
