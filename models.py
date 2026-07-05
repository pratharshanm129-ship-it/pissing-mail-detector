"""
models.py
----------
Data access layer (CRUD operations) for the AI Phishing Email Detector.
Contains two "models": User and Prediction.
Each function opens its own short-lived database connection, which
is the simplest and safest pattern for a small Flask app like this.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection


# ==========================================================
# USER MODEL
# ==========================================================

class User:
    """Handles all database operations related to users."""

    @staticmethod
    def create(username, email, password):
        """
        Creates a new user with a securely hashed password.
        Returns the new user's id, or None if username/email
        already exists.
        """
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception:
            return None
        finally:
            conn.close()

    @staticmethod
    def find_by_username(username):
        """Returns a user row matching the given username, or None."""
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return user

    @staticmethod
    def find_by_email(email):
        """Returns a user row matching the given email, or None."""
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        return user

    @staticmethod
    def find_by_id(user_id):
        """Returns a user row matching the given id, or None."""
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        return user

    @staticmethod
    def verify_password(stored_password_hash, password_attempt):
        """Checks a plaintext password attempt against the stored hash."""
        return check_password_hash(stored_password_hash, password_attempt)


# ==========================================================
# PREDICTION MODEL
# ==========================================================

class Prediction:
    """Handles all database operations related to prediction history."""

    @staticmethod
    def create(user_id, email_text, prediction, confidence, risk_level,
               keywords_found, recommendation):
        """Inserts a new prediction record and returns its new id."""
        conn = get_db_connection()
        cursor = conn.execute(
            """INSERT INTO predictions
               (user_id, email_text, prediction, confidence, risk_level,
                keywords_found, recommendation)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, email_text, prediction, confidence, risk_level,
             keywords_found, recommendation),
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def find_by_id(prediction_id):
        """Returns a single prediction row by its id."""
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM predictions WHERE id = ?", (prediction_id,)
        ).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_history_for_user(user_id):
        """Returns all predictions made by a specific user, newest first."""
        conn = get_db_connection()
        rows = conn.execute(
            """SELECT * FROM predictions
               WHERE user_id = ?
               ORDER BY created_at DESC""",
            (user_id,),
        ).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_stats_for_user(user_id):
        """
        Returns simple aggregate statistics for a user's dashboard:
        total checks, phishing count, and safe count.
        """
        conn = get_db_connection()
        total = conn.execute(
            "SELECT COUNT(*) AS c FROM predictions WHERE user_id = ?",
            (user_id,),
        ).fetchone()["c"]
        phishing = conn.execute(
            """SELECT COUNT(*) AS c FROM predictions
               WHERE user_id = ? AND prediction = 'Phishing'""",
            (user_id,),
        ).fetchone()["c"]
        safe = conn.execute(
            """SELECT COUNT(*) AS c FROM predictions
               WHERE user_id = ? AND prediction = 'Safe'""",
            (user_id,),
        ).fetchone()["c"]
        conn.close()
        return {"total": total, "phishing": phishing, "safe": safe}

    @staticmethod
    def delete(prediction_id, user_id):
        """Deletes a prediction record, only if it belongs to the user."""
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM predictions WHERE id = ? AND user_id = ?",
            (prediction_id, user_id),
        )
        conn.commit()
        conn.close()
