from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from easyhealth_app.models import Patient, Doctor, Document

class DocumentForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=1, max=40)])
    file_url = StringField('Photo URL:', validators=[DataRequired(), URL()])
    
    submit = SubmitField('Submit')

class SignUpPatientForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Name:', validators=[DataRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Length(min=1, max=40)])
    phone = StringField('Phone:', validators=[DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        patient = Patient.query.filter_by(username=username.data).first()
        if patient:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginPatientForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In')

class SignUpDoctorForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Name:', validators=[DataRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Length(min=1, max=40)])
    phone = StringField('Phone:', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email:', validators=[DataRequired(), Length(min=1, max=40)])
    care_service = StringField('Healthcare Service:', validators=[DataRequired(), Length(min=1, max=40)])
    credentials = StringField('Doctor Credentials:', validators=[DataRequired(), Length(min=1, max=40)])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        doctor = Doctor.query.filter_by(username=username.data).first()
        if doctor:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginDoctorForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')