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

app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

if not app.config['SQLALCHEMY_DATABASE_URI']:
    app.logger.error("DATABASE_URI is not set")

if not app.config['SECRET_KEY']:
    app.logger.error("SECRET_KEY is not set")

db = SQLAlchemy()
db.init_app(app)

from application import routes