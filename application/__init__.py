from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.utils.logger import setup_logger
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

logger = setup_logger(__name__, "app.log")

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

app.logger.info("Flask app initialized")

try:
    database_uri = getenv("DATABASE_URI")
    secret_key = getenv("SECRET_KEY")

    if not database_uri:
        logger.error("DATABASE_URI is not set")
        raise ValueError("DATABASE_URI missing")

    if not secret_key:
        logger.error("SECRET_KEY is not set")
        raise ValueError("SECRET_KEY missing")
    
    app.logger.info("Environment variables loaded")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key

    app.logger.info("Database configuration loaded")

    db = SQLAlchemy()
    db.init_app(app)

    app.logger.info("Database initialized successfully")

except Exception as e:
    app.logger.exception(f"Database initialization failed: {e}")
    raise

from application import routes