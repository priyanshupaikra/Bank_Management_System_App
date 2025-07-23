from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db
from app.forms import LoginForm, RegistrationForm, TransactionForm, TransferForm, LoanApplicationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Account, Transaction, Loan
from app.services import get_personalized_offers, get_financial_advice
from decimal import Decimal
import io
import pandas as pd
from flask import Response

# 1. Create a Blueprint object named 'main'
main = Blueprint('main', __name__)

# 2. Change all decorators from @app.route() to @main.route()
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # 3. Update url_for() to use the blueprint name (e.g., 'main.dashboard')
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        account = Account(owner=user, account_type='Savings', balance=100.00)
        db.session.add(account)
        db.session.commit()
        flash('Congratulations, you are now a registered user! A savings account has been created for you.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    accounts = current_user.accounts.all()
    return render_template('dashboard.html', title='Dashboard', accounts=accounts)

@main.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    transaction_form = TransactionForm()
    transfer_form = TransferForm()
    # Assuming one account per user for simplicity
    account = current_user.accounts.first()

    if 'submit_deposit' in request.form and transaction_form.validate_on_submit():
        amount = transaction_form.amount.data
        account.balance += amount
        new_transaction = Transaction(account_id=account.id, type='Deposit', amount=amount, description=f'Deposited ${amount}')
        db.session.add(new_transaction)
        db.session.commit()
        flash(f'Successfully deposited ${amount}.', 'success')
        return redirect(url_for('main.transaction'))

    if 'submit_withdraw' in request.form and transaction_form.validate_on_submit():
        amount = transaction_form.amount.data
        if account.balance < amount:
            flash('Insufficient funds.', 'danger')
        else:
            account.balance -= amount
            new_transaction = Transaction(account_id=account.id, type='Withdrawal', amount=amount, description=f'Withdrew ${amount}')
            db.session.add(new_transaction)
            db.session.commit()
            flash(f'Successfully withdrew ${amount}.', 'success')
        return redirect(url_for('main.transaction'))

    if 'submit_transfer' in request.form and transfer_form.validate_on_submit():
        amount = transfer_form.amount.data
        recipient_acc_num = transfer_form.recipient_account.data
        sender_account = account

        if sender_account.balance < amount:
            flash('Insufficient funds for transfer.', 'danger')
        else:
            recipient_account = Account.query.filter_by(account_number=recipient_acc_num).first()
            if not recipient_account:
                flash('Recipient account not found.', 'danger')
            elif recipient_account.id == sender_account.id:
                flash('Cannot transfer to your own account.', 'danger')
            else:
                # Perform transfer
                sender_account.balance -= amount
                recipient_account.balance += amount

                # Record transactions for both accounts
                t_sender = Transaction(account_id=sender_account.id, type='Transfer', amount=-amount, description=f'Transfer to {recipient_acc_num}')
                t_recipient = Transaction(account_id=recipient_account.id, type='Transfer', amount=amount, description=f'Transfer from {sender_account.account_number}')

                db.session.add(t_sender)
                db.session.add(t_recipient)
                db.session.commit()
                flash(f'Successfully transferred ${amount} to account {recipient_acc_num}.', 'success')
        return redirect(url_for('main.transaction'))

    return render_template('transaction.html', title='Transactions', transaction_form=transaction_form, transfer_form=transfer_form)

@main.route('/statement')
@login_required
def statement():
    account = current_user.accounts.first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('statement.html', title='Account Statement', transactions=transactions)

@main.route('/apply_loan', methods=['GET', 'POST'])
@login_required
def apply_loan():
    form = LoanApplicationForm()
    if form.validate_on_submit():
        loan = Loan(
            borrower=current_user,
            amount=form.amount.data,
            term_months=form.term_months.data
        )
        db.session.add(loan)
        db.session.commit()
        flash('Your loan application has been submitted for review.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('apply_loan.html', title='Apply for a Loan', form=form)


# Add 'POST' to the methods list for this route
@main.route('/offers', methods=['GET', 'POST'])
@login_required
def offers():
    # Initialize variables for the response
    form_question = ""
    gemini_answer = ""

    if request.method == 'POST':
        # Get the question from the form submitted by the user
        form_question = request.form.get('question')
        if form_question:
            try:
                # Call the new service function with the user's question
                gemini_answer = get_financial_advice(current_user, form_question)
            except Exception as e:
                gemini_answer = f"Could not retrieve a response at this time. Error: {e}"
                flash("There was an issue connecting to the AI service.", "danger")
    
    # Render the template, passing the question and answer to be displayed
    return render_template(
        'offers.html',
        title='Financial Assistant',
        form_question=form_question,
        gemini_answer=gemini_answer
    )

@main.route('/export/<format>')
@login_required
def export(format):
    # 1. Fetch the user's transaction data
    account = current_user.accounts.first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.timestamp.desc()).all()

    # Create a list of dictionaries from the transaction objects
    data = [
        {
            "Date": t.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "Description": t.description,
            "Type": t.type,
            "Amount": t.amount
        } for t in transactions
    ]

    # 2. Use pandas to create a DataFrame
    df = pd.DataFrame(data)

    # 3. Generate the file based on the requested format
    if format == 'csv':
        # Create a string buffer to hold the CSV data in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0) # Go to the beginning of the buffer

        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=statement.csv"}
        )
    elif format == 'excel':
        # Create a byte buffer to hold the Excel data in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Statement')
        output.seek(0) # Go to the beginning of the buffer

        return Response(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment;filename=statement.xlsx"}
        )

    return redirect(url_for('main.statement'))

# NOTE: You will need to continue this pattern for your other routes
# (transaction, apply_loan, etc.) if they are not already updated.