# Clinical Scheduling API


The project was built to practice moving from simple in-memory APIs to a more realistic backend architecture with **asynchronous database operations, persistent data storage, authentication, validation, pagination, and modular API routing**.

## How It Works

The API manages two main resources:

* **Patients** — stores patient information such as name, age, diagnosis, and active status.
* **Appointments** — stores appointments associated with patients, including the doctor, appointment time, reason, and status.

The application uses **PostgreSQL** for persistent storage and **SQLModel with SQLAlchemy's asynchronous engine** for database operations.

Authentication is handled using an API key supplied through the `X-Api-Key` request header.

## Features

### Patient Management

* Create a patient
* Retrieve all patients
* Retrieve a patient by ID
* Update patient information
* Delete a patient
* Validate patient input
* Paginate patient results

### Appointment Management

* Create an appointment
* Retrieve all appointments
* Retrieve an appointment by ID
* Filter appointments by patient ID
* Update appointment information
* Delete an appointment
* Validate that the referenced patient exists
* Paginate appointment results

### API & Backend Features

* RESTful API design
* Asynchronous request handling
* PostgreSQL database integration
* SQLModel ORM
* Pydantic-based validation
* API-key authentication
* Dependency injection
* Modular routers
* Pagination with `offset` and `limit`
* Query parameter filtering
* HTTP exception handling
* Appropriate HTTP status codes
* Environment-based configuration
* Automatic database table creation during application startup
* Interactive API documentation through Swagger UI

## API Endpoints

### Patients

| Method   | Endpoint                 | Description            |
| -------- | ------------------------ | ---------------------- |
| `POST`   | `/patients/`             | Create a patient       |
| `GET`    | `/patients/`             | Get patients           |
| `GET`    | `/patients/{patient_id}` | Get a specific patient |
| `PATCH`  | `/patients/{patient_id}` | Update a patient       |
| `DELETE` | `/patients/{patient_id}` | Delete a patient       |

### Appointments

| Method   | Endpoint                         | Description                |
| -------- | -------------------------------- | -------------------------- |
| `POST`   | `/appointments/`                 | Create an appointment      |
| `GET`    | `/appointments/`                 | Get appointments           |
| `GET`    | `/appointments/{appointment_id}` | Get a specific appointment |
| `PATCH`  | `/appointments/{appointment_id}` | Update an appointment      |
| `DELETE` | `/appointments/{appointment_id}` | Delete an appointment      |

## Query Parameters

The API supports pagination on patient and appointment listings.

Example:

```text
GET /patients/?offset=0&limit=20
```

Appointments can additionally be filtered by patient:

```text
GET /appointments/?patient_id=1
```

The appointment endpoint also supports pagination:

```text
GET /appointments/?patient_id=1&offset=0&limit=20
```

The maximum `limit` is restricted to **100**.

## Authentication

All API routes require an API key.

The key is supplied through the request header:

```text
X-Api-Key: your-api-key
```

Requests with a missing or invalid API key receive:

```text
401 Unauthorized
```

The API key is loaded from environment configuration rather than being hard-coded into the application.

## Data Validation

Request and response schemas are separated from the database models.

For example, patient creation validates:

* `full_name` — 2–130 characters
* `age` — greater than 0
* `diagnosis` — required

Appointment data includes:

* Patient ID
* Doctor name
* Appointment time
* Appointment reason
* Appointment status

Partial updates are supported through dedicated update schemas.

## Database

The project uses **PostgreSQL** as its persistent database.

SQLModel provides the database models and integrates with SQLAlchemy for asynchronous database access.

The application uses:

* `AsyncSession`
* `create_async_engine`
* `async_sessionmaker`
* SQLModel queries
* Foreign-key relationships between appointment records and patients

An appointment cannot be created for a patient that does not exist. The API checks the patient ID before creating the appointment and returns `404 Not Found` when the patient cannot be found.

## Project Structure

```text
Clinical-Scheduling-API/
│
├── app/
│   ├── routers/
│   │   ├── appointments.py
│   │   ├── patients.py
│   │   └── __init__.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── __init__.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Architecture

* **`main.py`** — creates the FastAPI application, authentication dependency, database startup lifecycle, and router registration.
* **`routers/`** — contains the API endpoints for patients and appointments.
* **`models.py`** — defines the SQLModel database tables.
* **`schemas.py`** — defines request and response models.
* **`database.py`** — configures the asynchronous PostgreSQL engine and database sessions.
* **`config.py`** — manages application settings and environment variables.

This separation keeps routing, database configuration, data models, and application configuration from being placed in one large file.

## Environment Variables

The application expects configuration through a `.env` file.

Example:

```env
APP_NAME=Clinical Scheduling API
ENVIRONMENT=development
PORT=8000
DATABASE_URL=postgresql+asyncpg://username:password@localhost/database_name
API_KEY=your-secret-api-key
```

**Do not commit `.env` to GitHub.** It contains secrets and environment-specific configuration.

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Clinical-Scheduling-API
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it according to your operating system.

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The project includes a `requirements.txt` file containing the required Python dependencies.

## Database Setup

Make sure PostgreSQL is running and that the database specified in `DATABASE_URL` exists.

The application creates the required SQLModel tables when it starts.

## How To Run

The project uses the FastAPI CLI:

```bash
fastapi dev app/main.py
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to test the endpoints and provide the required API key.

## HTTP Status Codes

The API uses standard HTTP status codes to communicate the result of requests:

* `200 OK` — successful retrieval or update
* `201 Created` — resource successfully created
* `204 No Content` — resource successfully deleted
* `401 Unauthorized` — invalid or missing API key
* `404 Not Found` — requested resource does not exist
* `422 Unprocessable Entity` — request data failed validation

## Topics Covered

* FastAPI
* REST API development
* CRUD operations
* PostgreSQL
* SQLModel
* SQLAlchemy
* Asynchronous database operations
* `AsyncSession`
* Pydantic/SQLModel validation
* Request and response schemas
* API-key authentication
* FastAPI dependencies
* `APIRouter`
* Query parameters
* Path parameters
* Pagination
* Foreign keys
* HTTP status codes
* `HTTPException`
* Environment variables
* Application lifespan
* Database initialization
* Modular backend architecture

## Key Concepts Demonstrated

* **Router separation:** Patient and appointment endpoints are separated into different router modules.
* **Dependency injection:** Database sessions and authentication are provided through FastAPI dependencies.
* **Async database access:** Database operations use `AsyncSession` and `await`.
* **Schema separation:** Create, read, and update schemas serve different API responsibilities.
* **Persistent storage:** Data is stored in PostgreSQL rather than an in-memory Python collection.
* **Pagination:** Large collections can be retrieved using `offset` and `limit`.
* **Resource validation:** Appointments verify that their referenced patient exists before creation.
* **Authentication:** A reusable API-key dependency protects the API.
* **Configuration management:** Sensitive values such as database credentials and API keys are loaded from environment variables.

## Future Improvements

* Add user accounts and role-based authentication
* Replace API-key authentication with JWT authentication
* Add doctor management
* Add appointment conflict detection
* Prevent overlapping appointments
* Add appointment status validation using enums
* Add database migrations with Alembic
* Add automated tests with Pytest
* Add structured logging
* Add centralized exception handling
* Add Docker support
* Add deployment configuration
* Add production-ready database configuration and connection management
