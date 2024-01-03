from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, ValidationError, Length, Email, EqualTo
from mypython.models import User
from flask_login import current_user


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=2, max=200), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("That email is already registered, please Login or Use a different email address.")

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=200)])
    remember = BooleanField('Remember')
    login = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Update')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            existing_email = User.query.filter_by(email=email.data).first()

            if existing_email:
                raise ValidationError(
                    "That email is already registered. Please use a different email address."
                )

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with this email.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=2, max=200), EqualTo('password')])
    submit = SubmitField('Reset Password')