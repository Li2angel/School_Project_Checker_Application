from flask_wtf import Form
from wtforms import TextAreaField,PasswordField,SubmitField,TelField
from wtforms.validators import ValidationError, DataRequired

class SchoolResulCheckerForm(Form):
    name = TelField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Send")

class ProjectRegistration(Form):
    title = TelField(label="Project Title")
    sName = TelField(label="Student Name")
    regNumber = TelField(label="Registration Number")
    description = TextAreaField(label="Project Description")
    submit = SubmitField("Send")