"""Create database models to represent tables."""
from easyhealth_app import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    pts_doctors = db.relationship('Doctor', secondary = 'patient_doctor')
    patients = db.relationship("Patient", back_populates='doctor_docs')

    def __str__(self):
        return f'<Patient Name: {self.name}>'

    def __repr__(self):
        return f'<Patient Name: {self.name}>'


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    care_service = db.Column(db.String(80))
    credentials = db.Column(db.String(80), nullable=False)

    drs_patients = db.relationship('Patient', secondary = 'patient_doctor')
    doctors = db.relationship("Patient", back_populates='patient_docs')

    def __str__(self):
        return f'<Doctor Name: {self.name}>'

    def __repr__(self):
        return f'<Doctor Name: {self.name}>'

patient_doctor_table = db.Table('patient_doctor',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'))

)

patient_doctor_table = None

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    file_url = db.Column(db.String(80), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created_by = db.relationship('Patient') 
    
    patient_docs = db.relationship("Document", back_populates='patients')
    doctor_docs = db.relationship("Document", back_populates='doctors')
    

medical_docs_table = db.Table('medical_docs_table',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
)
