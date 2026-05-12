from application import app, db
from application.models import Medication
from application.utils.logger import setup_logger

logger = setup_logger(__name__, "app.log")

with app.app_context():

    db.drop_all()
    db.create_all()

    app.logger.info("Database recreated")