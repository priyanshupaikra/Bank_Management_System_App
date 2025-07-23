from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# Update login_view to point to the blueprint's login route
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register the blueprint
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import models so they are known to the app
    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    # Configure Gemini API
    import google.generativeai as genai
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)

    return app