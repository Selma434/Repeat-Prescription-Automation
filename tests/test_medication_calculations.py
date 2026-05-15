from application import app, db
from application.models import Medication


from application import app, db
from application.models import Medication


with app.app_context():

    print("\nMEDICATION CALCULATIONS")

    medications = Medication.query.all()

    for med in medications:

        print("-" * 50)

        print(f"Medication: {med.name}")
        print(f"Last issued: {med.last_issued}")
        print(f"Duration: {med.duration_days} days")
        print(f"Run out date: {med.run_out_date}")
        print(f"Days remaining: {med.days_remaining}")
        print(f"Status: {med.status}")

    print("\nALL MEDICATIONS")

    for med in medications:
        print(med.name)

    print("\nACTIVE MEDICATIONS")

    active_medications = Medication.query.filter_by(
        active=True
    ).all()

    for med in active_medications:
        print(med.name)

    print("\nMEDICATION BY ID")

    medication = db.session.get(
        Medication,
        2
    )

    print(medication.name)