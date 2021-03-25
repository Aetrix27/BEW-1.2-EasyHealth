import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from easyhealth_app.models import User, Document, Doctor, Patient
from easyhealth_app.forms import DocumentForm, SignUpForm, LoginForm, AddDoctorForm
from easyhealth_app import bcrypt
from easyhealth_app.utils import patient_required, doctor_required
from easyhealth_app import app, db

auth = Blueprint("auth", __name__)
patients = Blueprint("patients", __name__)
doctors = Blueprint("doctors", __name__)

##########################################
#           Routes                       #
##########################################

@auth.route('/')
def homepage():
    documents = Document.query.all()
    return render_template('home.html', documents=documents)

@patients.route('/new_patient_document', methods=['GET', 'POST'])
@login_required
@patient_required
def new_patient_document():
    form = DocumentForm()

    if form.validate_on_submit(): 
    
        document = Document(
            title=form.title.data,
            pts_created=Patient.query.get(current_user.patient_ids),
            drs_created=Doctor.query.get(round(form.drs_created.data))

        )
        print(current_user.patient_ids)
        print(round(form.drs_created.data))

        db.session.add(document)
        db.session.commit()
        
        flash('New Document was successfully created')
        return redirect(url_for('patients.patient_document_detail', document_id=document.id))

    return render_template('new_patient_document.html', form=form)

@patients.route('/add_patient_doctor', methods=['GET', 'POST'])
@login_required
@patient_required
def add_patient_doctor():
    patient = Patient.query.get(current_user.patient_ids)
        #current_user.patients_ids
    form = AddDoctorForm(obj=patient)

    if form.validate_on_submit(): 
        patient.doctors_id = ([Doctor.query.get(form.doctor.data)])
    
    db.session.add(patient)
    db.session.commit()
        
    flash('A new Doctor was succesfully added.')

    return render_template('add_patient_doctor.html', patient=patient, form=form)

@doctors.route('/new_doctor_document', methods=['GET', 'POST'])
@login_required
@doctor_required
def new_doctor_document():
    form = DocumentForm()

    if form.validate_on_submit(): 
    
        document = Document(
            title=form.title.data,
            pts_created=Patient.query.get(current_user.doctor_ids),
            drs_created=Doctor.query.get(form.drs_created.data)
        )

        db.session.add(document)
        db.session.commit()
        
        flash('New Document was successfully created')
        return redirect(url_for('doctors.doctor_document_detail', document_id=document.id))

    return render_template('new_doctor_document.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            care_service=form.care_service.data,
            is_doctor=form.is_doctor.data,
            doctor_ids = -1,
            patient_ids = -1
        )

        db.session.add(user)
        db.session.commit()

        if user.is_doctor == True:
            doctor = Doctor(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                care_service=form.care_service.data
            )

            db.session.add(doctor)
            db.session.commit()
            user.doctor_ids=doctor.id

            db.session.add(user)
            db.session.commit()

        elif user.is_doctor == False:
            patient = Patient(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                care_service=form.care_service.data
            )

            db.session.add(patient)
            db.session.commit()

            user.patient_ids = patient.id
            db.session.add(user)
            db.session.commit()
        
        flash('Account Created.')

        db.session.commit()

        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

@doctors.route('/doctor_document_detail/<document_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def doctor_document_detail(document_id):
    document = Document.query.get(document_id)
    form = DocumentForm(obj=document)

    if form.validate_on_submit():
        document.title=(form.title.data)
        document.pts_created=(Patient.query.get(form.pts_created.data))
        document.drs_created=(Doctor.query.get(current_user.doctor_id))

    db.session.add(document)
    db.session.commit()
    flash('A new Doctor Document was successfully updated')

    document = Document.query.get(document_id)
    return render_template('doctor_document_detail.html', document=document, form=form)

@patients.route('/patient_document_detail/<document_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def patient_document_detail(document_id):
    document = Document.query.filter_by(id=document_id).one()
    form = DocumentForm(obj=document)

    if form.validate_on_submit():
        document.title=(form.title.data)
        document.pts_created=(Patient.query.get(current_user.patient_ids))
        document.drs_created=(Doctor.query.get(form.drs_created.data))

    db.session.add(document)
    db.session.commit()
    flash('A new Patient Document was successfully updated')

    document = Document.query.get(document_id)
    return render_template('patient_document_detail.html', document=document, form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('auth.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.homepage'))


