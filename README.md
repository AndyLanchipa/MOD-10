# Secure FastAPI User Management System

A robust FastAPI application with secure user authentication, password hashing, comprehensive testing, and automated CI/CD pipeline.

## Features

- **Secure User Authentication**: JWT-based authentication with password hashing using bcrypt
- **Data Validation**: Comprehensive input validation using Pydantic schemas
- **Database Integration**: SQLAlchemy ORM with PostgreSQL support
- **Comprehensive Testing**: Unit and integration tests with high coverage
- **CI/CD Pipeline**: Automated testing and Docker deployment via GitHub Actions
- **Security Scanning**: Automated security checks for vulnerabilities
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Technology Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Testing**: pytest with comprehensive test suite
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions
- **Security**: Bandit and Safety for security scanning

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── database.py          # Database models and connection
│   ├── schemas.py           # Pydantic models for validation
│   ├── auth.py              # Authentication utilities
│   ├── crud.py              # Database operations
│   └── routers/
│       ├── __init__.py
│       └── auth.py          # Authentication routes
├── tests/
│   ├── __init__.py
│   ├── test_auth.py         # Authentication unit tests
│   ├── test_schemas.py      # Schema validation tests
│   ├── test_crud.py         # Database operation tests
│   └── test_integration.py # API integration tests
├── .github/workflows/
│   └── ci-cd.yml           # GitHub Actions workflow
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml     # Local development setup
├── pyproject.toml         # pytest configuration
└── README.md              # This file
```

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MOD\ 10
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run with Docker Compose (Recommended)**
   ```bash
   docker-compose up --build
   ```

6. **Or run locally with PostgreSQL**
   ```bash
   # Make sure PostgreSQL is running
   uvicorn app.main:app --reload
   ```

The application will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Running Tests Locally

### Prerequisites
- Python 3.11+
- PostgreSQL (for integration tests)
- All dependencies installed

### Run All Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_auth.py tests/test_schemas.py -v

# Database tests (requires PostgreSQL)
pytest tests/test_crud.py -v

# Integration tests (requires PostgreSQL)
pytest tests/test_integration.py -v
```

### Test Database Setup
For tests requiring a real database, ensure PostgreSQL is running:
```bash
# Using Docker
docker run --name test_postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=testdb -p 5432:5432 -d postgres:13

# Set environment variable
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/testdb
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information (requires authentication)

### Health Checks
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## User Model

### Database Schema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### User Registration Requirements
- **Username**: 3-50 characters, alphanumeric and underscores only
- **Email**: Valid email format
- **Password**: Minimum 8 characters with at least:
  - One uppercase letter
  - One lowercase letter  
  - One digit

## Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive request validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **CORS Configuration**: Proper cross-origin request handling
- **Security Scanning**: Automated vulnerability checks

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Testing Phase**:
   - Runs unit tests for authentication and validation
   - Executes integration tests with PostgreSQL
   - Generates coverage reports

2. **Security Phase**:
   - Scans code for security vulnerabilities
   - Checks dependencies for known issues

3. **Deployment Phase** (on main branch):
   - Builds Docker image
   - Pushes to Docker Hub
   - Runs security scan on Docker image

### Required GitHub Secrets
```
DOCKER_USERNAME - Your Docker Hub username
DOCKER_PASSWORD - Your Docker Hub access token
```

## Docker Hub Repository

The application is automatically deployed to Docker Hub at:
**[Your Docker Hub Repository URL]** - Update this with your actual Docker Hub repository

### Pull and Run from Docker Hub
```bash
docker pull your-username/fastapi-secure-user-app:latest
docker run -p 8000:8000 -e DATABASE_URL=your_db_url your-username/fastapi-secure-user-app:latest
```

## Development Workflow

1. Create feature branch from `main`
2. Make changes and add tests
3. Ensure all tests pass locally
4. Push to GitHub (triggers CI pipeline)
5. Create pull request
6. After review and CI success, merge to `main`
7. Automatic deployment to Docker Hub

## Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Configuration
The application supports PostgreSQL by default. For development, you can use the provided Docker Compose setup.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is developed for educational purposes as part of a FastAPI learning module.

## Support

For issues and questions, please use the GitHub issue tracker.
