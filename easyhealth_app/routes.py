"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from easyhealth_app.models import Doctor, Patient

# Import app and db from events_app package so that we can run app
from easyhealth_app import app, db


main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():

    context = {

    }

    return render_template('index.html', **context)

