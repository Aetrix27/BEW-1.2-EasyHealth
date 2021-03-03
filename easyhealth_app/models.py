"""Create database models to represent tables."""
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from easyhealth_app import db
from datetime import datetime
from sqlalchemy.orm import backref
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.hash import sha256_crypt

from flask import session


class User(db.Model, UserMixin):
    #login_type = db.Column(db.String(20))

    is_doctor = db.Column(db.Boolean, nullable=False, default=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))

    #credentials = db.Column(db.String(80), nullable=False)
    #users = db.relationship("User", secondary = 'patient_doctor', back_populates='users')

class Patient(db.Model):
    #login_type = db.Column(db.String(20))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

  
class Doctor(db.Model):
    #login_type = db.Column(db.String(20))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    patients = db.relationship('Patient', backref='doctor', lazy=True)


#patient_doctor_table = db.Table('patient_doctor',
 #   db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
 #   db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'))
#)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    file_url = db.Column(db.String(80), nullable=False)

    #patient_table_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    #doctor_table_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    
#medical_docs_table = db.Table('medical_docs_table',
 #   db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
 #   db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
   # db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
#)
