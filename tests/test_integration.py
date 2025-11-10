import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.crud import create_user
from app.schemas import UserCreate

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAuthenticationEndpoints:
    """Test authentication API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to the Secure FastAPI User Management System" in response.json()["message"]

    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_register_user_success(self):
        """Test successful user registration."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data  # Password should not be in response
        assert "password_hash" not in data  # Password hash should not be in response
        assert "id" in data
        assert "created_at" in data

    def test_register_user_invalid_email(self):
        """Test user registration with invalid email."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "Password123!"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_register_user_weak_password(self):
        """Test user registration with weak password."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_register_user_duplicate_username(self):
        """Test user registration with duplicate username."""
        user_data = {
            "username": "testuser",
            "email": "test1@example.com",
            "password": "Password123!"
        }
        
        # Register first user
        response1 = client.post("/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same username
        user_data["email"] = "test2@example.com"
        response2 = client.post("/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "Username already exists" in response2.json()["detail"]

    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email."""
        user_data1 = {
            "username": "testuser1",
            "email": "test@example.com",
            "password": "Password123!"
        }
        user_data2 = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "Password123!"
        }
        
        # Register first user
        response1 = client.post("/auth/register", json=user_data1)
        assert response1.status_code == 201
        
        # Try to register with same email
        response2 = client.post("/auth/register", json=user_data2)
        assert response2.status_code == 400
        assert "Email already exists" in response2.json()["detail"]

    def test_login_success(self):
        """Test successful user login."""
        # First register a user
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }
        client.post("/auth/register", json=user_data)
        
        # Then login
        login_data = {
            "username": "testuser",
            "password": "Password123!"
        }
        response = client.post("/auth/token", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_wrong_password(self):
        """Test login with wrong password."""
        # First register a user
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }
        client.post("/auth/register", json=user_data)
        
        # Try to login with wrong password
        login_data = {
            "username": "testuser",
            "password": "WrongPassword123!"
        }
        response = client.post("/auth/token", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        login_data = {
            "username": "nonexistent",
            "password": "Password123!"
        }
        response = client.post("/auth/token", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_get_current_user_success(self):
        """Test getting current user information."""
        # Register and login to get token
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!"
        }
        client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "Password123!"
        }
        login_response = client.post("/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data
        assert "password_hash" not in data

    def test_get_current_user_no_token(self):
        """Test getting current user without token."""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
