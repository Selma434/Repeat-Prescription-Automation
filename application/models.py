from application import db
from datetime import datetime, timedelta, timezone


class Medication(db.Model):

    __tablename__ = "medication"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    last_issued = db.Column(
        db.Date,
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

    @property
    def run_out_date(self):
        return self.last_issued + timedelta(
            days=self.duration_days
        )

    @property
    def days_remaining(self):
        return (
            self.run_out_date -
            datetime.now(
                timezone.utc
            ).date()
        ).days

    @property
    def running_low(self):
        """
        Return True if medication has
        1–7 days remaining.
        """
        return 0 < self.days_remaining <= 7

    @property
    def status(self):
        """
        Return medication status.

        OUT = overdue or empty
        CRITICAL = extremely low
        LOW = ≤ 7 days remaining
        OK = enough medication
        """

        days = self.days_remaining

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