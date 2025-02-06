from src.conf import messages

test_contact = {
    "first_name": "John",
    "last_name": "Dou",
    "email": "john@gmail.com",
    "phone_number": "+380995555555",
    "birthday": "1990-01-01",
    "additional_data": "Some extra text"
}

def test_create_contact(client, get_token):
    response = client.post(
        "/api/contacts",
        json=test_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == test_contact["first_name"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_contact(client, get_token):
    response = client.get(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == test_contact["first_name"]
    assert "id" in data


def test_get_contact_not_found(client, get_token):
    response = client.get(
        "/api/contacts/2", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND


def test_get_contacts(client, get_token):
    response = client.get("/api/contacts", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == test_contact["first_name"]
    assert "id" in data[0]
    assert len(data) > 0


def test_update_contact(client, get_token):
    updated_contact = test_contact.copy()
    updated_contact["first_name"] = "Updated John"
    response = client.put(
        "/api/contacts/1",
        json=updated_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == updated_contact["first_name"]
    assert "id" in data


def test_update_contact_not_found(client, get_token):
    updated_contact = test_contact.copy()
    updated_contact["first_name"] = "Updated John"
    response = client.put(
        "/api/contacts/2",
        json=updated_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND


def test_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 204, response.text
    data = response._content
    assert data == b""


def test_repeat_delete_contact(client, get_token):
    response = client.delete(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == messages.CONTACT_NOT_FOUND
