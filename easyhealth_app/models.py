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
    is_doctor = db.Column(db.Boolean, nullable=False, default=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))

    #credentials = db.Column(db.String(80), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    doctor = db.relationship('Doctor', back_populates='patients')
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    #doctors = db.relationship('Genre', secondary='book_genre', back_populates='books')
  
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    patients = db.relationship('Patient', back_populates='doctor')
    #patients = db.relationship('Genre', secondary='book_genre', back_populates='books')


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
