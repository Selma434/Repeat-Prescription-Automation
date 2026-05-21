from flask import render_template, redirect, url_for, request, flash

from application import app, db
from application.models import Medication
from application.forms import AddMedicationForm, EditMedicationForm

@app.route("/")
@app.route("/dashboard")
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

@app.route("/add-medication", methods=["GET", "POST"])
def add_medication():

    form = AddMedicationForm()

    print("FORM SUBMITTED")

    if form.validate_on_submit():

        print("FORM VALIDATED")

        medication = Medication(
            name=form.name.data,
            last_issued=form.last_issued.data,
            duration_days=form.duration_days.data,
            active=form.active.data
        )

        db.session.add(medication)
        db.session.commit()

        print("MEDICATION SAVED")

        return redirect(
            url_for("index")
        )

    print(form.errors)

    return render_template(
        "add_medication.html",
        form=form
    )

@app.route("/edit-medication/<int:id>", methods=["GET", "POST"])
def edit_medication(id):

    medication = Medication.query.get_or_404(
        id
    )

    form = EditMedicationForm(
        obj=medication
    )

    if request.method == "GET":
        form.active.data = medication.active

    if form.validate_on_submit():

        medication.name = form.name.data
        medication.last_issued = form.last_issued.data
        medication.duration_days = form.duration_days.data
        medication.active = form.active.data

        db.session.commit()

        flash(
            "Medication updated successfully.",
            "success"
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "edit_medication.html",
        form=form,
        medication=medication
    )

@app.route("/deactivate-medication/<id>", methods=["POST"])
def deactivate_medication(id):

    medication = Medication.query.get_or_404(
        id
    )

    medication.active = False

    db.session.commit()

    flash(
        f"{medication.name} deactivated.",
        "success"
    )

    return redirect(
        url_for("medications")
    ) 

@app.route(
    "/reactivate-medication/<int:id>",
    methods=["POST"]
)
def reactivate_medication(id):

    medication = Medication.query.get_or_404(
        id
    )

    medication.active = True

    db.session.commit()

    flash(
        f"{medication.name} reactivated.",
        "success"
    )

    return redirect(
        url_for("medications")
    )

@app.route(
    "/delete-medication/<int:id>",
    methods=["POST"]
)
def delete_medication(id):

    medication = Medication.query.get_or_404(
        id
    )

    medication_name = medication.name

    db.session.delete(
        medication
    )

    db.session.commit()

    flash(
        f"{medication_name} deleted.",
        "success"
    )

    return redirect(
        url_for("medications")
    )