# URL Shortener

A modern, asynchronous URL shortening service built with Python FastAPI. This project features user authentication, rate limiting, and a robust backend architecture.

## Features

- **URL Shortening**: Create short aliases for long URLs
- **User Authentication**: Secure signup and login with JWT tokens
- **Rate Limiting**: Prevent abuse with configurable rate limits
- **Asynchronous Database**: High-performance async database operations
- **Logging**: Comprehensive logging with ELK stack integration
- **Security**: Password hashing with bcrypt, JWT authentication

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

### URL Management (Planned)

- `POST /api/v0/urls` - Create a new short URL
- `GET /api/v0/urls/{short_code}` - Redirect to original URL
- `GET /api/v0/urls` - List user's URLs
- `DELETE /api/v0/urls/{short_code}` - Delete a short URL

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
     -d '{"username": "testuser", "password": "Test123!@#"}'
   ```

## Development

### Prerequisites

- Python 3.13+
- PostgreSQL database
- Virtual environment (recommended)

### Setting up for Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"  # If you add dev dependencies to pyproject.toml
   ```

3. Run in development mode:
   ```bash
   python main.py
   ```

### Code Quality

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write unit tests for new functionality

## Configuration

The application can be configured using environment variables in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | (required) |
| SECRET_KEY | JWT secret key | (required) |
| ALGORITHM | JWT algorithm | HS256 |

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

## Logging

The application features comprehensive logging with ELK stack integration for monitoring and debugging.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This is a practice project designed to demonstrate modern Python web development practices
- Built with FastAPI for high performance and automatic API documentation
- Uses SQLAlchemy 2.0 for robust database interactions