from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit_deposit = SubmitField('Deposit')
    submit_withdraw = SubmitField('Withdraw')

class TransferForm(FlaskForm):
    recipient_account = StringField('Recipient Account Number', validators=[DataRequired(), Length(min=12, max=12)])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit_transfer = SubmitField('Transfer')
    
class LoanApplicationForm(FlaskForm):
    amount = DecimalField('Loan Amount', validators=[DataRequired(), NumberRange(min=100)])
    term_months = IntegerField('Loan Term (Months)', validators=[DataRequired(), NumberRange(min=6, max=120)])
    submit = SubmitField('Apply for Loan')