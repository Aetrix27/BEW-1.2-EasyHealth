from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField, FloatField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from easyhealth_app.models import User, Document, Patient, Doctor

class DocumentForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=1, max=40)])
    #pts_created = QuerySelectMultipleField('Patient:', query_factory=lambda: Patient.query, get_label='username')
    #drs_created = QuerySelectMultipleField('Doctor:', query_factory=lambda: Doctor.query, get_label='username')
    pts_created= FloatField('Patient:')
    drs_created = FloatField('Doctor:')
    
    submit = SubmitField('Submit')

class AddDoctorForm(FlaskForm):
   
    doctor = FloatField('Doctor:')
    
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    username = StringField('User Name:',validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=1, max=40)])
    email = StringField('Email:', validators=[DataRequired(), Length(min=1, max=40)])
    phone = StringField('Phone:', validators=[DataRequired(), Length(min=1, max=30)])
    care_service = StringField('Healthcare Service:', validators=[DataRequired(), Length(min=1, max=40)])
    is_doctor = BooleanField('Are you a Doctor?')
    #credentials = StringField('Doctor Credentials:', validators=[DataRequired(), Length(min=1, max=40)])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
