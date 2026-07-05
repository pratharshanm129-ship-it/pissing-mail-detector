"""
detector.py
------------
Simple KEYWORD-BASED phishing email detector.
No machine learning is used here on purpose, so a 2nd-year IT
student can easily read, understand, and modify the logic.

How it works:
1. We keep a list of common "red flag" words/phrases seen in
   real phishing emails.
2. We search the submitted email text (case-insensitive) for
   each keyword.
3. Based on HOW MANY keywords were found, we decide:
      - Prediction   -> Safe or Phishing
      - Confidence   -> a percentage score
      - Risk Level   -> Low / Medium / High
      - Recommendation -> advice text for the user
"""

# The list of phishing "red flag" keywords/phrases to search for.
PHISHING_KEYWORDS = [
    "verify",
    "password",
    "urgent",
    "click here",
    "login",
    "bank",
    "gift",
    "winner",
    "account suspended",
    "free",
]


def detect_phishing(email_text):
    """
    Analyzes the given email text and returns a dictionary with:
        prediction, confidence, risk_level, keywords_found, recommendation

    Parameters
    ----------
    email_text : str
        The raw email content (subject + body) submitted by the user.

    Returns
    -------
    dict
    """
    if email_text is None:
        email_text = ""

    text_lower = email_text.lower()

    # Find which keywords appear in the email text
    keywords_found = [kw for kw in PHISHING_KEYWORDS if kw in text_lower]
    keyword_count = len(keywords_found)
    total_keywords = len(PHISHING_KEYWORDS)

    # ------------------------------------------------------------
    # Decide prediction, confidence and risk level based on the
    # number of matched keywords.
    # ------------------------------------------------------------
    if keyword_count == 0:
        prediction = "Safe"
        confidence = 95
        risk_level = "Low"
        recommendation = (
            "No suspicious keywords were detected. This email looks safe, "
            "but always stay alert -- never share your password or personal "
            "details unless you are 100% sure of the sender's identity."
        )

    elif keyword_count <= 2:
        prediction = "Phishing"
        confidence = min(55 + (keyword_count * 10), 75)
        risk_level = "Medium"
        recommendation = (
            "A few suspicious keywords were found. Be cautious: do not click "
            "any links or download attachments. Verify the sender's email "
            "address carefully before taking any action."
        )

    elif keyword_count <= 4:
        prediction = "Phishing"
        confidence = min(76 + (keyword_count * 4), 92)
        risk_level = "High"
        recommendation = (
            "Multiple phishing indicators were detected. This email is very "
            "likely a scam. Do NOT click any links, do NOT reply, and do NOT "
            "enter any personal or banking information. Report and delete it."
        )

    else:
        prediction = "Phishing"
        confidence = min(93 + keyword_count, 99)
        risk_level = "High"
        recommendation = (
            "This email contains many classic phishing red flags (urgency, "
            "requests for credentials, fake rewards, etc.). Treat this as a "
            "confirmed phishing attempt. Delete it and never respond."
        )

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_level": risk_level,
        "keywords_found": keywords_found,
        "keyword_count": keyword_count,
        "total_keywords": total_keywords,
        "recommendation": recommendation,
    }
