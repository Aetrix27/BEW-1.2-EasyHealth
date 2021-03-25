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
    is_doctor = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    doctor_ids = db.Column(db.String(80))
    patient_ids = db.Column(db.String(80))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))

    doctors_id = db.relationship('Doctor', secondary = 'patient_doctor', back_populates='patients_id')
    patient = db.relationship('Document', back_populates='pts_created')


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))

    patients_id = db.relationship('Patient', secondary = 'patient_doctor', back_populates='doctors_id')
    doctor = db.relationship('Document', back_populates='drs_created')

patient_doctor_table = db.Table('patient_doctor',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'))

)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

    patient_id_col = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id_col = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    
    pts_created = db.relationship("Patient", back_populates='patient')
    drs_created = db.relationship("Doctor", back_populates='doctor')

    
#documents_table = db.Table('documents_table',
 #   db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
 #   db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
 #   db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
#)

