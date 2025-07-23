# Bank_Management_System_App
Gemini Bank ♊
A full-stack, AI-powered web application for a modern banking system. This project demonstrates core banking functionalities, from user authentication to transaction handling, and features an interactive financial assistant powered by the Google Gemini API.

✨ Key Features
User Authentication: Secure user registration and login system.

Account Dashboard: A central hub for users to view their account number and current balance.

Transaction Management: Functionality for users to deposit, withdraw, and transfer funds between accounts.

Statement History: View a complete, paginated history of all transactions for an account.

Loan Application System: Users can apply for loans, which can be reviewed.

AI Financial Assistant: An interactive chatbot, powered by the Google Gemini API, that provides financial advice based on the user's account data.

Data Export: Users can export their account statements to CSV or Excel files.

🛠️ Tech Stack & Libraries
This project is built with the following technologies and Python libraries:

Backend: Python with the Flask web framework.

Database: MySQL with Flask-SQLAlchemy as the ORM.

Frontend: HTML with the Jinja2 templating engine and basic CSS.

Forms & Security: Flask-WTF for secure web forms and CSRF protection.

Authentication: Flask-Login for managing user sessions.

AI Integration: Google Generative AI (google-generativeai) to connect with the Gemini API.

Data Export: Pandas and Openpyxl for generating CSV and Excel files.

Email Validation: email-validator for robust email validation in forms.

Environment Management: python-dotenv for managing secret keys and configuration.

🚀 Setup and Installation
Follow these steps to get the application running on your local machine.

1. Prerequisites
Python 3.8+

MySQL Server

2. Clone the Repository
Bash

git clone <your-repository-url>
cd <your-repository-name>
3. Install Python Libraries
Install all the necessary packages using pip:

Bash

pip install flask flask-sqlalchemy flask-login flask-wtf mysql-connector-python python-dotenv google-generativeai pandas openpyxl email-validator
4. Database Setup
Log in to your MySQL server.

Create a new database for the project.

SQL

CREATE DATABASE banking_db;
5. Environment Variables
In the root directory of the project, create a file named .env.

Copy the content from the example below into your .env file and replace the placeholder values with your actual credentials.

Code snippet

# .env file

# Generate a random string for this (e.g., by running: python -c 'import secrets; print(secrets.token_hex(16))')
SECRET_KEY='your_super_secret_and_random_key_here'

# Your MySQL connection string.
# IMPORTANT: If your password contains special characters like @, #, $, use a URL encoder on the password.
DATABASE_URI='mysql+mysqlconnector://your_mysql_user:your_mysql_password@localhost/banking_db'

# Your API key from Google AI Studio
GEMINI_API_KEY='your_google_gemini_api_key_here'
6. Run the Application
The application is configured to automatically create the database tables the first time you run it.

Bash

python run.py
The application will be available at http://127.0.0.1:5000.

🔒 Security Features
Security is a key consideration in this application.

Password Hashing: User passwords are never stored in plain text. We use the werkzeug.security library (included with Flask) to generate a secure hash of the user's password during registration. At login, the provided password is a hashed and compared to the stored hash for verification.

Email Validation: During registration, user-provided emails are validated to ensure they are in a correct format using the email-validator library via WTForms.

Session Management: User sessions are handled securely by Flask-Login, which uses cryptographically signed cookies to prevent users from modifying their session information (like their user ID).

CSRF Protection: All forms are protected against Cross-Site Request Forgery (CSRF) attacks automatically by Flask-WTF.

🔮 Future Work
Potential features to be added:

Admin Panel: A secure dashboard for bank employees to approve/reject loans and manage users.

Multiple User Accounts: Allow users to open and manage more than one type of account (e.g., Savings, Checking).
