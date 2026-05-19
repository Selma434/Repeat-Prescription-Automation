from flask import render_template

from application import app
from application.models import Medication


@app.route("/")
def index():

    medications = Medication.query.filter_by(
        active=True
        ).all()

    return render_template(
        "index.html",
        medications=medications
    )

@app.route("/medications")
def medications():

    medications = Medication.query.all()

    return render_template(
        "medications.html",
        medications=medications
    )