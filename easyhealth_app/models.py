"""Create database models to represent tables."""
from easyhealth_app import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))

    doctors = db.relationship("Doctor", secondary = 'patient_doctor', back_populates='patients')
    pts_created = db.relationship("Document", back_populates='patient_docs')

    def __str__(self):
        return f'<Patient Name: {self.name}>'

    def __repr__(self):
        return f'<Patient Name: {self.name}>'


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    credentials = db.Column(db.String(80), nullable=False)

    patients = db.relationship("Patient", secondary = 'patient_doctor', back_populates='doctors')
    drs_created = db.relationship("Document", back_populates='doctor_docs')

    def __str__(self):
        return f'<Doctor Name: {self.name}>'

    def __repr__(self):
        return f'<Doctor Name: {self.name}>'

patient_doctor_table = db.Table('patient_doctor',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'))

)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    file_url = db.Column(db.String(80), nullable=False)

    patient_table_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_table_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    
    patient_docs = db.relationship("Patient", back_populates='pts_created')
    doctor_docs = db.relationship("Doctor", back_populates='drs_created')
    
medical_docs_table = db.Table('medical_docs_table',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
)
