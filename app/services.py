import google.generativeai as genai
from flask_login import current_user
from app.models import Transaction

def get_personalized_offers(user):
    """
    Generates personalized financial offers for a user based on their data.
    """
    account = user.accounts.first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.timestamp.desc()).limit(5).all()

    # Format recent transactions for the prompt
    transaction_summary = "\n".join([f"- {t.type} of ${t.amount} on {t.timestamp.strftime('%Y-%m-%d')}" for t in transactions])

    prompt = f"""
    You are a helpful and friendly AI financial advisor for our bank.
    A customer is asking for personalized offers. Based on their financial data below, generate 2-3 brief, actionable financial tips or product offers.
    Address the customer directly as 'you'. For example, say 'You could consider...' instead of 'The customer could consider...'.
    Format the response as a single block of text with each tip starting with a dash '-'. Do not use markdown like bolding.

    Customer Data:
    - Account Type: {account.account_type}
    - Current Balance: ${account.balance:.2f}
    - Recent Transactions:
    {transaction_summary if transaction_summary else "No recent transactions."}

    Generate the personalized offers now.
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Handle cases where the API might fail
        print(f"Gemini API call failed: {e}")
        return "We are currently unable to generate personalized offers. Please check our standard products page."


# filename: app/services.py

def get_financial_advice(user, question):
    """
    Generates a response to a user's financial question using their data as context.
    """
    account = user.accounts.first()
    transactions = Transaction.query.filter_by(account_id=account.id).order_by(Transaction.timestamp.desc()).limit(10).all()

    # Format recent transactions for the prompt
    transaction_summary = "\n".join([f"- {t.type} of ${t.amount} on {t.timestamp.strftime('%Y-%m-%d')}" for t in transactions])

    # This prompt provides context, the user's question, and a security guardrail.
    prompt = f"""
    You are a helpful and professional AI financial assistant for Gemini Bank.
    Your role is to answer the customer's question based on the financial data provided below.

    **Important:** Only answer questions related to personal finance or the provided customer data. If the question is unrelated (e.g., about history, science, or other non-financial topics), you must politely decline to answer.

    ---
    Customer Financial Data:
    - Account Balance: ${account.balance:.2f}
    - Recent Transactions:
    {transaction_summary if transaction_summary else "No recent transactions."}
    ---

    Customer's Question:
    "{question}"

    Your Answer:
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return "Sorry, I am unable to process your request at this time."