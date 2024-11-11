from flask_wtf import FlaskForm  # Base form class from Flask-WTF
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, DateField  # Form field types
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError  # Validators
from models import User  # Import User model for validation
from datetime import date

class SignupForm(FlaskForm):
    # Username field
    # DataRequired() ensures field isn't empty
    # Length() sets minimum and maximum characters allowed
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80)
    ])

    # Email field
    # Email() validator ensures proper email format
    email = EmailField('Email', validators=[
        DataRequired(), 
        Email()
    ])

    # Password field
    # Length(min=6) requires at least 6 characters
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long")
    ])

    # Confirm password field
    # EqualTo validator ensures it matches the password field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    # Gender field
    gender = SelectField('Gender', 
        choices=[
            ('', 'Select Gender'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say')
        ],
        validators=[DataRequired(message="Please select your gender")]
    )

    # Birthday field
    birthday = DateField('Birthday', 
        validators=[DataRequired(message="Please enter your birthday")],
        format='%Y-%m-%d'
    )

    # Submit button
    submit = SubmitField('Sign Up')

    # Custom validators
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one.')

    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another one.')

    def validate_birthday(self, birthday):
        if birthday.data:
            today = date.today()
            age = today.year - birthday.data.year - ((today.month, today.day) < (birthday.data.month, birthday.data.day))
            if age < 13:
                raise ValidationError('You must be at least 13 years old to register.')


class LoginForm(FlaskForm):
    # Email field for login
    email = EmailField('Email', validators=[
        DataRequired(), 
        Email()
    ])

    # Password field for login
    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    # Submit button
    submit = SubmitField('Log In') 