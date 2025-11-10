from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.database import create_tables

# Create database tables
create_tables()

app = FastAPI(
    title="Secure FastAPI User Management",
    description="A secure FastAPI application with user authentication, password hashing, and comprehensive testing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Welcome to the Secure FastAPI User Management System"}


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
