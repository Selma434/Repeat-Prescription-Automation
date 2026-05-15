from application import app
from application.models import Medication


with app.app_context():

    medications = Medication.query.all()

    for med in medications:

        print("-" * 50)

        print(f"Medication: {med.name}")
        print(f"Last requested: {med.last_issued}")
        print(f"Duration: {med.duration_days} days")
        print(f"Run out date: {med.run_out_date}")
        print(f"Days remaining: {med.days_remaining}")
        print(f"Status: {med.status}")