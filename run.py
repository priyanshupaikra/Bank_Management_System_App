from app import create_app, db
from sqlalchemy import inspect

# Create the Flask app instance
app = create_app()

# This block of code will run before starting the server
with app.app_context():
    # Create an inspector to check the database
    inspector = inspect(db.engine)
    
    # Check if the 'user' table exists. We use one table as a proxy for all of them.
    if not inspector.has_table("user"):
        print("Database tables not found, creating them now...")
        db.create_all()
        print("Database tables created successfully!")
    else:
        print("Database tables already exist.")


if __name__ == '__main__':
    app.run(debug=True)