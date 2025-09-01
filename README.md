# Bank_Management_System_App
Gemini Bank ♊
A full-stack, AI-powered web application for a modern banking system. This project demonstrates core banking functionalities, from user authentication to transaction handling, and features an interactive financial assistant powered by the Google Gemini API.

📸 Screenshots
A quick look at the Gemini Bank application dashboard and the AI Assistant in action.
(Here you would add screenshots of your application. A GIF of the workflow is also a great idea!)

Dashboard
AI Financial Assistant

✨ Key Features
User Authentication: Secure user registration and login system with password hashing.
Account Dashboard: A central hub for users to view their account number and current balance.
Transaction Management: Functionality for users to deposit, withdraw, and transfer funds.
Statement History: View a complete history of all transactions for an account.
Loan Application System: Users can apply for loans.
AI Financial Assistant: An interactive chatbot powered by Google Gemini that provides financial advice based on the user's account data.
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

git clone https://github.com/your-username/gemini-bank.git
cd gemini-bank
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
Password Hashing: User passwords are never stored in plain text. We use werkzeug.security to hash passwords upon registration and verify them at login.
Email Validation: Emails are validated for correct formatting during registration.
Session Management: User sessions are handled securely by Flask-Login, which uses cryptographically signed cookies to prevent session tampering.
CSRF Protection: All forms are protected against Cross-Site Request Forgery attacks automatically by Flask-WTF.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.
Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
