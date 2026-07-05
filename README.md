# PhishGuard - AI Phishing Email Detector

A beginner-friendly full-stack web application that detects phishing emails
using **keyword-based analysis** (no machine learning). Built with Flask,
SQLite, HTML, CSS, JavaScript, and Bootstrap 5.

---

## Features

- Home Page with hero section and feature highlights
- About Page explaining how detection works
- User Registration (with form validation)
- User Login (session-based authentication)
- Dashboard with statistics (total checks, phishing count, safe count)
- Email Detection Page (paste email text to analyze)
- Prediction Result Page (prediction, confidence, risk level, keywords, recommendation)
- Prediction History Page (view and delete past results)
- Logout

---

## Detection Logic (Keyword-Based)

The app scans submitted email text for these common phishing keywords:

```
verify, password, urgent, click here, login, bank, gift, winner,
account suspended, free
```

Based on how many keywords are found, the app calculates:

| Keywords Found | Prediction | Risk Level | Confidence |
|----------------|------------|------------|------------|
| 0              | Safe       | Low        | ~95%       |
| 1 - 2          | Phishing   | Medium     | 55% - 75%  |
| 3 - 4          | Phishing   | High       | 76% - 92%  |
| 5+             | Phishing   | High       | 93% - 99%  |

See `detector.py` for the full logic.

---

## Folder Structure

```
phishing-detector/
│
├── app.py                     # Main Flask application entry point
├── database.py                # SQLite connection & initialization logic
├── models.py                  # User & Prediction CRUD operations
├── routes.py                  # All Flask routes (Blueprint)
├── detector.py                # Keyword-based phishing detection logic
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── database/
│   ├── schema.sql              # SQL script to create tables
│   └── phishing_detector.db    # SQLite database file (auto-created on first run)
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom CSS styling
│   └── js/
│       └── script.js           # Custom JavaScript
│
└── templates/
    ├── base.html                # Shared layout (navbar + footer)
    ├── home.html                # Home page
    ├── about.html               # About page
    ├── register.html            # Registration page
    ├── login.html                # Login page
    ├── dashboard.html            # User dashboard
    ├── detect.html               # Email detection form
    ├── result.html               # Prediction result page
    └── history.html              # Prediction history page
```

---

## Technology Stack

| Layer          | Technology                     |
|----------------|---------------------------------|
| Backend        | Python 3, Flask                |
| Database       | SQLite                         |
| Frontend       | HTML5, CSS3, JavaScript         |
| UI Framework   | Bootstrap 5 + Bootstrap Icons  |
| Auth           | Flask Sessions + Werkzeug password hashing |

---

## Setup & Run Instructions

### 1. Prerequisites
Make sure you have **Python 3.8+** installed. Check with:
```bash
python --version
```

### 2. Extract / Navigate to the Project Folder
```bash
cd phishing-detector
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **macOS / Linux:** `source venv/bin/activate`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

The first time you run it, the SQLite database (`database/phishing_detector.db`)
will be created automatically from `database/schema.sql`.

### 6. Open in Browser
Go to:
```
http://127.0.0.1:5000
```

---

## Usage Walkthrough

1. **Register** a new account from the Register page.
2. **Login** with your username and password.
3. From the **Dashboard**, click "Analyze New Email".
4. **Paste** a suspicious email's text into the box and click "Analyze Email".
5. View the **Result Page** showing Prediction, Confidence %, Risk Level,
   Detected Keywords, and a Recommendation.
6. Visit **History** anytime to review or delete past predictions.
7. Click **Logout** when done.

---

## Sample Test Emails

**Try this (should be flagged as Phishing):**
```
Subject: Urgent - Verify Your Account Now!
Dear Customer, your account has been suspended. Click here to verify your
password and bank details immediately or you will lose access. You are a
winner of a free gift!
```

**Try this (should be flagged as Safe):**
```
Subject: Team Meeting Tomorrow
Hi team, just a reminder that we have our weekly sync meeting tomorrow at
10 AM. Please review the attached agenda before joining. Thanks!
```

---

## Resetting the Database

If you want to start fresh (delete all users and history), simply delete
the database file and restart the app:

```bash
rm database/phishing_detector.db      # macOS / Linux
del database\phishing_detector.db     # Windows
python app.py
```

---

## Notes for Students

- This project uses **no machine learning** -- detection is purely rule-based
  (simple keyword matching), which makes the logic easy to read and extend.
- Passwords are never stored in plain text; they are hashed using Werkzeug's
  `generate_password_hash`.
- All database queries use parameterized SQL (`?` placeholders) to prevent
  SQL injection.
- Feel free to add more keywords to the `PHISHING_KEYWORDS` list in
  `detector.py` to experiment with the detection logic.

---

## License

This project is created for educational purposes and is free to use, modify,
and extend for learning.
