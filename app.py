import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-pacas-app")

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

# Si no hay DATABASE_URL, usamos SQLite local
if not DATABASE_URL:
    logging.warning("DATABASE_URL no encontrada. Usando SQLite local.")
    DATABASE_URL = "sqlite:///data.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to create tables
    import models
    db.create_all()

# Import utility functions for templates
from utils import format_currency, format_percentage, format_number

# Make utility functions available in templates
app.jinja_env.globals.update(
    format_currency=format_currency,
    format_percentage=format_percentage,
    format_number=format_number
)

# Import routes after app creation to avoid circular imports
from routes import *
