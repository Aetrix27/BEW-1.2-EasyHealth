import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from easyhealth_app.models import User, Document, Doctor, Patient
from easyhealth_app.forms import DocumentForm, SignUpForm, LoginForm
from easyhealth_app import bcrypt

# Import app and db from events_app package so that we can run app
from easyhealth_app import app, db

auth = Blueprint("auth", __name__)
patients = Blueprint("patients", __name__)
doctors = Blueprint("doctors", __name__)


##########################################
#           Routes                       #
##########################################

@auth.route('/')
def homepage():

    return render_template('home.html')

@patients.route('/new_document', methods=['GET', 'POST'])
@login_required
def new_document():
    form = DocumentForm()

    if form.validate_on_submit(): 
    
        document = Document(
            title=form.title.data,
            patient_table_id=form.pts_created.data,
            doctor_table_id=form.drs_created.data

        )
        print(form.pts_created.data)
        db.session.add(document)
        db.session.commit()
        
        flash('New Document was successfully created')
        return redirect(url_for('patients.document_detail', document_id=document.id))

    return render_template('new_document.html', form=form)

@patients.route('/document/<document_id>', methods=['GET', 'POST'])
@login_required
def document_detail(document_id):
    document = Document.query.get(document_id)
    form = DocumentForm(obj=document)

    if form.validate_on_submit():
        document.title = (form.title.data,)
        document.patient_table_id=(form.pts_created.data)
        document.doctor_table_id=(form.drs_created.data)

    db.session.add(document)
    db.session.commit()
    flash('A new Grocery Item was successfully updated')

    document = Document.query.get(document_id)
    return render_template('document_detail.html', document=document, form=form)

#@doctors.route('/document/<document_id>', methods=['GET', 'POST'])
#@login_required

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    patient_check = 0
    doctor_check = 0
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            care_service=form.care_service.data,
            is_doctor=form.is_doctor.data
        )

        db.session.add(user)
        db.session.commit()

        get_user = User.query.filter_by(username=form.username.data).first()

        if get_user.is_doctor == True:
            patient_check = None
            doctor = Doctor(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                care_service=form.care_service.data,
            )

            #db.session.add(user)
            db.session.add(doctor)
            db.session.commit()

            print(patient_check)
            print(doctor_check)
        elif get_user.is_doctor == False:
            doctor_check = None
            patient = Patient(
                username=form.username.data,
                password=hashed_password,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                care_service=form.care_service.data,
            )

            db.session.add(patient)
            db.session.commit()
        
        flash('Account Created.')
        print('created')

        db.session.commit()

        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

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


