"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
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



