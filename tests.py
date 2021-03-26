import os
from unittest import TestCase

from datetime import date
 
from easyhealth_app import app, db, bcrypt
from easyhealth_app.models import Doctor, Patient, User, Document

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def create_documents():

    d1 = Document(
        title='Heart',
        pts_create=1,
        drs_created=1
    )
    db.session.add(d1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

def create_patient():
    p1 = Patient(
        username="david",
        password=123,
        name="David",
        email="dafda@gmail.com"
    )

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        create_user()

        post_data = {
            "username": "me1",
            "password" : "incorrect_password"
        }     

        self.app.post("/signup", data=post_data)
        user = User.query.filter_by(username="me1").one()
        
        self.assertEqual(user.username, "me1")

    def test_signup_existing_user(self):
        create_user()

        post_data = {
            "username": "me1",
            "password" : "password"
        }        
        response = self.app.post("/signup", data=post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Sign Up", response_text)
        self.assertIn("That username is taken. Please choose a different one.", response_text)

    def test_login_correct_password(self):
        create_user()
        
        self.app.post("/login")
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertNotIn("Login", response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            "username": "another_user",
            "password" : "password66"
        }        
        
        response = self.app.post("/login", data=post_data)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("No user with that username. Please try again.", response_text)

    def test_login_incorrect_password(self):
        create_user()

        post_data = {
            "username": "me1",
            "password" : "incorrect_password"
        }     

        self.app.post("/signup", data=post_data)
        user = User.query.filter_by(username="me1").one()
        
        self.assertEqual(user.username, "me1")


    def test_logout(self):
        create_user()

        post_data = {
            "username": "me1",
            "password": "password",
        }
        self.app.post("/login", data=post_data)

        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Log In", response_text)
        self.assertNotIn("Log Out", response_text)
