from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField, FloatField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from easyhealth_app.models import User, Document

class DocumentForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=1, max=40)])
    file_url = StringField('Photo URL:', validators=[DataRequired(), URL()])
    
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
