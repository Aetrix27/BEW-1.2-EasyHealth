import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from easyhealth_app.models import Doctor, Patient, Document
from easyhealth_app.forms import DocumentForm, SignUpPatientForm, SignUpDoctorForm, LoginDoctorForm, LoginPatientForm
from easyhealth_app import bcrypt

# Import app and db from events_app package so that we can run app
from easyhealth_app import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_doctors = Doctor.query.all()
    all_patients = Patient.query.all()

    return render_template('home.html', all_doctors=all_doctors, all_patients=all_patients)

@auth.route('/signup_patient', methods=['GET', 'POST'])
def signup_patient():
    print('in signup')
    form = SignUpPatientForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient = Patient(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            email=form.email.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login_patient'))
    print(form.errors)
    return render_template('patient_signup.html', form=form)

@auth.route('/login_patient', methods=['GET', 'POST'])
def login_patient():
    form = LoginPatientForm()
    if form.validate_on_submit():
        user = Patient.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

@auth.route('/signup_doctor', methods=['GET', 'POST'])
def signup_doctor():
    print('in signup')
    form = SignUpDoctorForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doctor = Doctor(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            care_service=form.care_service.data,
            credentials=form.credentials.data

        )
        db.session.add(doctor)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login_doctor'))
    print(form.errors)
    return render_template('doctor_signup.html', form=form)    

@auth.route('/login_doctor', methods=['GET', 'POST'])
def login_doctor():
    form = LoginDoctorForm()
    if form.validate_on_submit():
        user = Doctor.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)



