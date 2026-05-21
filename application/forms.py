from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

# add medication form
class AddMedicationForm(FlaskForm):
    name = StringField(
        "Medication Name",
        validators=[
            DataRequired(),
            Length(min=2, max=200)
        ]
    )
    last_issued = DateField(
        "Last Issued",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )
    duration_days = IntegerField(
        "Duration (Days)",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=365,
                message="Duration must be between 1 and 365 days."
            )
        ]
    )
    active = SelectField(
        "Medication Status",
        choices=[
            ("True", "Active"),
            ("False", "Inactive")
        ],
        coerce=lambda x: x == "True"
    )

    submit = SubmitField(
        "Submit Medication"
    )

# edit medication form
class EditMedicationForm(FlaskForm):
    name = StringField(
        "Medication Name",
        validators=[
            DataRequired(),
            Length(min=2, max=200)
        ]
    )
    last_issued = DateField(
        "Last Issued",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )
    duration_days = IntegerField(
        "Duration (Days)",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=365,
                message="Duration must be between 1 and 365 days."
            )
        ]
    )
    active = SelectField(
        "Medication Status",
        choices=[
            ("True", "Active"),
            ("False", "Inactive")
        ],
        coerce=lambda x: x == "True"
    )

    submit = SubmitField(
        "Submit Medication"
    )