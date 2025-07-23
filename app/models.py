from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    accounts = db.relationship('Account', backref='owner', lazy='dynamic')
    loans = db.relationship('Loan', backref='borrower', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False, default=''.join(random.choices(string.digits, k=12)))
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    account_type = db.Column(db.String(50), nullable=False) # 'Savings', 'Checking'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False) # 'Deposit', 'Withdrawal', 'Transfer'
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), default=5.00)
    term_months = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Approved', 'Rejected'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)