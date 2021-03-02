from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from easyhealth_app.config import Config
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import Patient

@login_manager.user_loader
def load_patient(patient_id):
    return Patient.query.get(patient_id)

from .models import Doctor

@login_manager.user_loader
def load_doctor(doctor_id):
    return Doctor.query.get(doctor_id)

from easyhealth_app.routes import main, auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

