from application import db
from datetime import datetime, timedelta, timezone


class Medication(db.Model):

    __tablename__ = "medications"

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
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def run_out_date(self):
        """
        Calculate estimated medication depletion date.
        """
        return self.last_requested + timedelta(
            days=self.duration_days
        )

    def days_remaining(self):
        """
        Calculate number of days left.
        """
        return (
            self.run_out_date() - datetime.now(timezone.utc)
        ).days

    def running_low(self):
        """
        Return True if medication has
        1–7 days remaining.
        """
        return 0 < self.days_remaining() <= 7

    def status(self):
        """
        Return medication status.

        OUT = overdue or empty
        CRITICAL = extremely low
        LOW = ≤ 7 days remaining
        OK = enough medication
        """

        days = self.days_remaining()

        if days <=0:
            return "OUT"
        
        elif days <= 3:
            return "CRITICAL"

        elif days <= 7:
            return "LOW"

        return "OK"

    def __repr__(self):
        """
        Helpful for debugging.
        """
        return f"<Medication {self.name}>"