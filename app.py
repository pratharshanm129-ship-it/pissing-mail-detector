"""
app.py
-------
Main entry point for the AI Phishing Email Detector Flask application.

Run this file to start the app:
    python app.py

Then open your browser at:
    http://127.0.0.1:5000
"""

from flask import Flask
from database import init_db, database_exists
from routes import main


def create_app():
    app = Flask(__name__)

    # Secret key used to sign session cookies and flash messages.
    # In a real production app, load this from an environment variable.
    app.config["SECRET_KEY"] = "phishing-detector-secret-key-2024"

    # Register the blueprint that contains all our routes
    app.register_blueprint(main)

    return app


app = create_app()


if __name__ == "__main__":
    # Initialize the database only if it does not already exist,
    # so we don't wipe out existing users/history on every restart.
    if not database_exists():
        init_db()
    else:
        print("Database already exists. Skipping initialization.")

    app.run(debug=True)
