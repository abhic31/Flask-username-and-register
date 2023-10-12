from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField
from wtforms.validators import DataRequired, Email

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class EmployeeForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[DataRequired()])
    date_of_joining = DateField('Date of Joining', validators=[DataRequired()])

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)