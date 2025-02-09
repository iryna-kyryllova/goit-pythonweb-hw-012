# 📌 Contacts API

## 📚 Description

Contacts API is an asynchronous RESTful web service built with FastAPI. It allows users to manage a list of contacts, authenticate, cache requests using Redis, and upload avatars to Cloudinary.

## 🚀 Technologies

- Python 3.11
- FastAPI
- PostgreSQL + SQLAlchemy + Alembic
- Redis
- Cloudinary
- Docker + Docker Compose
- Poetry (dependency management)

## 📦 Installation & Running

### 🔹 Local Run

1. **Clone the repository**

   ```sh
   git clone https://github.com/iryna-kyryllova/goit-pythonweb-hw-012
   cd repository
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux & macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```sh
   poetry install
   ```

4. **Set up environment variables**  
   Create a `.env` file based on `.env.example` and update the variable values.

5. **Run the server**

   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **API documentation is available at:**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🐳 Running with Docker

1. **Ensure Docker and Docker Compose are installed.**
2. **Start the container:**
   ```sh
   docker-compose up --build
   ```

## 🔑 Authentication & Authorization

- Uses JWT tokens.
- Users receive an access token upon registration.
- Only authenticated users can access contacts.
- The administrator can change user roles.

## 📝 API Endpoints

### 🔹 Authentication

- `POST /api/auth/register` - register a new user
- `POST /api/auth/login` - login and get a JWT token
- `POST /api/auth/make-admin?email={email}` - grant admin role to a user (admin only)

### 🔹 Contacts

- `GET /api/contacts` - get a list of contacts
- `POST /api/contacts` - add a new contact
- `GET /api/contacts/{id}` - get a contact by ID
- `PUT /api/contacts/{id}` - update a contact
- `DELETE /api/contacts/{id}` - delete a contact

### 🔹 Users

- `PATCH /api/users/avatar` - update avatar (authorized users only)

## 🛠 Testing

Run tests with:

```sh
pytest --cov=.
```

## 📌 Author

- **Iryna Kyryllova** ([keira.kirillova@gmail.com](mailto:keira.kirillova@gmail.com))

## ⭐ License

This project is open-source and follows the [MIT License](LICENSE).
