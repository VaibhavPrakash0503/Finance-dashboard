from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    # App Settings
    APP_NAME = "Finance Dashboard API"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
    
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Security Validation
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in .env file")
    
    # CORS Settings (for frontend)
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
