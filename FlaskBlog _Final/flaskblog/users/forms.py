#All user forms

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

#create registration form class
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                validators=[DataRequired(), Length(min=2, max=20)])     #makes sure field is not blank and length
    email = StringField('Email',
                validators=[DataRequired(),Email()]) #makes sure field is not blank and is valid email
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #does the username already exist?
        if user:    #if user is other than null:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first() #does the username already exist?
            if user:    #if user is other than null:
                raise ValidationError('That email is taken. Please choose a different one')


    #validate username field
    # def validate_field(self, field):
    #     if True:
    #         reaise ValidationError('Validation Message')


#create LoginForm form class
class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(),Email()]) #makes sure field is not blank and is valid email
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')       #Will use a cookie to remember for relogin
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                validators=[DataRequired(), Length(min=2, max=20)])     #makes sure field is not blank and length
    email = StringField('Email',
                validators=[DataRequired(),Email()]) #makes sure field is not blank and is valid email
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:      #perform check if username is different from current name
            user = User.query.filter_by(username=username.data).first() #does the username already exist?
            if user:    #if user is other than null:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() #does the username already exist?
            if user:    #if user is other than null:
                raise ValidationError('That email is taken. Please choose a different one')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #does the username already exist?
        if user is None:    #if user is other than null:
            raise ValidationError('Please register before logging in')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
