# URL Shortener

A modern, asynchronous URL shortening service built with Python FastAPI. This
project features user authentication and a robust backend architecture.

> **Status**: a practice project, under active development. The sections below
> mark anything not yet built as **Planned**. Nothing marked Planned exists in
> the code — it is intent, not documentation.

## Features

### Implemented

- **URL Shortening**: Create short aliases for long URLs
- **User Authentication**: Secure signup and login with JWT tokens
- **Asynchronous Database**: High-performance async database operations with
  connection pooling
- **Security**: Password hashing with bcrypt, JWT authentication

### Planned

- **Rate Limiting**: Prevent abuse with configurable rate limits — *not
  implemented; no limiter or dependency is wired up*
- **Logging**: Comprehensive logging with ELK stack integration — *not
  implemented; the app does no application-level logging beyond uvicorn's
  access log*
- **Automated Tests**: *no test suite or test dependencies exist yet*

## Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy 2.0 (Async)
- **Authentication**: JWT tokens with python-jose
- **Password Security**: bcrypt hashing
- **Database Migrations**: Alembic
- **Environment Management**: pydantic-settings

## Project Structure

```
url-shortener/
├── app/
│   ├── api/              # API routes
│   │   └── v0/           # API version 0
│   ├── core/             # Core functionality (auth, security, deps)
│   ├── db/               # Database configuration
│   ├── models/           # Database models
│   ├── repositories/     # Data access layer
│   ├── schemas/          # Pydantic models for validation
│   ├── services/         # Business logic
│   └── config.py         # Configuration settings
├── alembic/              # Database migrations
├── main.py               # Application entry point
├── pyproject.toml        # Project dependencies
└── .env                  # Environment variables
```

## API Endpoints

### Authentication

- `POST /api/v0/auth/signup` - Create a new user account
- `POST /api/v0/auth/login` - Authenticate and receive access token

### URL Management

All except the redirect require authentication via the `access_token` cookie.

- `POST /api/v0/urls` - Create a new short URL
- `GET /api/v0/urls/{short_code}` - Redirect to original URL (public — no auth,
  so shared links work for everyone)
- `GET /api/v0/urls` - List user's URLs
- `DELETE /api/v0/urls/{short_code}` - Delete a short URL (owner only)

Short codes are 7 random base62 characters. A code you don't own is reported as
`url_not_found` rather than `403`, so the API can't be used to probe which codes
exist.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd url-shortener
   ```

2. **Install dependencies**:
   ```bash
   pip install .
   ```

3. **Set up environment variables**:
   Create a `.env` file based on the existing `.env`:
   ```env
   DB_PASSWORD=your_db_password
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the server**:
   ```bash
   python main.py
   ```

## Usage

### Authentication

1. **Sign Up**:
   ```bash
   curl -X POST "http://localhost:5000/api/v0/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "Test123!@#"}'
   ```

2. **Log In**:
   ```bash
   curl -X POST "http://localhost:5000/api/v0/auth/login" \
     -H "Content-Type: application/json" \
     -c cookies.txt \
     -d '{"username": "testuser", "password": "Test123!@#"}'
   ```

### Shortening a URL

1. **Create a short URL** (using the cookie saved above):
   ```bash
   curl -X POST "http://localhost:5000/api/v0/urls" \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{"value": "https://example.com/some/very/long/path"}'
   ```

2. **Follow it** — no cookie needed:
   ```bash
   curl -i "http://localhost:5000/api/v0/urls/<short_code>"
   ```

3. **List your URLs**:
   ```bash
   curl -b cookies.txt "http://localhost:5000/api/v0/urls"
   ```

4. **Delete one**:
   ```bash
   curl -X DELETE -b cookies.txt "http://localhost:5000/api/v0/urls/<short_code>"
   ```

## Development

### Prerequisites

- Python 3.13.12+ (as pinned by `requires-python` in `pyproject.toml`)
- PostgreSQL database
- Virtual environment (recommended)

### Setting up for Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```
   There is no `[dev]` extra — no development or test dependencies are declared
   in `pyproject.toml` yet.

3. Run in development mode:
   ```bash
   python main.py
   ```

### Code Quality

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write unit tests for new functionality — aspirational for now; there is no
  test suite, runner, or fixtures in the repo to add tests to

## Configuration

The application can be configured using environment variables in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | (required) |
| SECRET_KEY | JWT secret key | (required) |
| ALGORITHM | JWT algorithm | (required) |

`DB_PASSWORD`, `SECRET_KEY` and `ALGORITHM` have no defaults in `config.py` —
omitting any of them fails at startup. See `.env.example`, which sets
`ALGORITHM=HS256`. There is no `DB_NAME` setting; the connection URL in
`db/session.py` specifies no database, so Postgres falls back to the default for
the user.

## Security

### Password Policy

Passwords must meet the following requirements:
- At least 8 characters long
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one digit
- Contains at least one special character

### Authentication

- JWT tokens are used for authentication
- Tokens expire after 15 minutes
- Passwords are hashed using bcrypt

## Logging (Planned)

Comprehensive logging with ELK stack integration is intended for monitoring and
debugging, but **is not implemented**. Today the only output is uvicorn's access
log, enabled in `main.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

Intended to be MIT licensed. **No LICENSE file has been added to the repository
yet**, so no license currently applies.

## Acknowledgments

- This is a practice project designed to demonstrate modern Python web development practices
- Built with FastAPI for high performance and automatic API documentation
- Uses SQLAlchemy 2.0 for robust database interactions