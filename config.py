import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Set Flask configuration from .env file."""
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_APP = 'run.py'

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False