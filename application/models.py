from application import db
from datetime import datetime, timedelta


class Medication(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    last_requested = db.Column(
        db.DateTime,
        nullable=False
    )

    duration_days = db.Column(
        db.Integer,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def run_out_date(self):
        return self.last_requested + timedelta(days=self.duration_days)

    def days_remaining(self):
        return (
            self.run_out_date() - datetime.utcnow()
        ).days

    def running_low(self):
        return self.days_remaining() <= 7