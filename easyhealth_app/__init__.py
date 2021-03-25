from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from easyhealth_app.config import Config
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy()
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "patients.login"

from .models import User

@login_manager.user_loader
def load_user(patient_id):
    return User.query.get(patient_id)

def create_app(config_class=Config):
    #app = Flask(__name__)
    #app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from easyhealth_app.routes import auth, patients, doctors

    app.register_blueprint(auth)
    app.register_blueprint(patients)
    app.register_blueprint(doctors)

    with app.app_context():
        db.create_all()

    return app