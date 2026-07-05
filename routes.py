"""
routes.py
----------
All the URL routes (pages) for the AI Phishing Email Detector app.
Organized using a Flask Blueprint called "main", which is registered
inside app.py.
"""

import re
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)

from models import User, Prediction
from detector import detect_phishing

main = Blueprint("main", __name__)

# Simple regex used to validate email format during registration
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ==========================================================
# HELPER: Login-required decorator
# ==========================================================
def login_required(view_func):
    """Redirects to the login page if the user is not logged in."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access that page.", "warning")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)
    return wrapped_view


# ==========================================================
# HOME PAGE
# ==========================================================
@main.route("/")
def home():
    return render_template("home.html")


# ==========================================================
# ABOUT PAGE
# ==========================================================
@main.route("/about")
def about():
    return render_template("about.html")


# ==========================================================
# USER REGISTRATION
# ==========================================================
@main.route("/register", methods=["GET", "POST"])
def register():
    # If already logged in, no need to register again
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors = []

        # ---------- Form validation ----------
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long.")

        if not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email address.")

        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        if User.find_by_username(username):
            errors.append("That username is already taken.")

        if User.find_by_email(email):
            errors.append("An account with that email already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "register.html", username=username, email=email
            )

        # ---------- Create the user ----------
        new_user_id = User.create(username, email, password)
        if new_user_id:
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("main.login"))
        else:
            flash("Something went wrong while creating your account.", "danger")
            return render_template(
                "register.html", username=username, email=email
            )

    return render_template("register.html", username="", email="")


# ==========================================================
# USER LOGIN
# ==========================================================
@main.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please fill in both username and password.", "danger")
            return render_template("login.html", username=username)

        user = User.find_by_username(username)

        if user is None or not User.verify_password(user["password_hash"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html", username=username)

        # ---------- Login success: create session ----------
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("login.html", username="")


# ==========================================================
# LOGOUT
# ==========================================================
@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("main.home"))


# ==========================================================
# DASHBOARD
# ==========================================================
@main.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    stats = Prediction.get_stats_for_user(user_id)
    recent_history = Prediction.get_history_for_user(user_id)[:5]
    return render_template(
        "dashboard.html",
        username=session["username"],
        stats=stats,
        recent_history=recent_history,
    )


# ==========================================================
# EMAIL DETECTION PAGE
# ==========================================================
@main.route("/detect", methods=["GET", "POST"])
@login_required
def detect():
    if request.method == "POST":
        email_text = request.form.get("email_text", "").strip()

        if not email_text:
            flash("Please paste or type an email to analyze.", "danger")
            return render_template("detect.html")

        # ---------- Run keyword-based detection ----------
        result = detect_phishing(email_text)

        # ---------- Save result to history ----------
        keywords_str = ", ".join(result["keywords_found"]) if result["keywords_found"] else "None"
        prediction_id = Prediction.create(
            user_id=session["user_id"],
            email_text=email_text,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            keywords_found=keywords_str,
            recommendation=result["recommendation"],
        )

        return redirect(url_for("main.result", prediction_id=prediction_id))

    return render_template("detect.html")


# ==========================================================
# PREDICTION RESULT PAGE
# ==========================================================
@main.route("/result/<int:prediction_id>")
@login_required
def result(prediction_id):
    record = Prediction.find_by_id(prediction_id)

    if record is None or record["user_id"] != session["user_id"]:
        flash("That prediction result could not be found.", "danger")
        return redirect(url_for("main.dashboard"))

    return render_template("result.html", record=record)


# ==========================================================
# PREDICTION HISTORY PAGE
# ==========================================================
@main.route("/history")
@login_required
def history():
    records = Prediction.get_history_for_user(session["user_id"])
    return render_template("history.html", records=records)


# ==========================================================
# DELETE A HISTORY RECORD
# ==========================================================
@main.route("/history/delete/<int:prediction_id>", methods=["POST"])
@login_required
def delete_history(prediction_id):
    Prediction.delete(prediction_id, session["user_id"])
    flash("Prediction record deleted.", "info")
    return redirect(url_for("main.history"))
