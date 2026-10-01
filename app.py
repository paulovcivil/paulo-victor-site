import json
import os
import urllib.error
import urllib.request
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False") == "True"

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MAIL_TO = os.getenv("MAIL_TO")


def send_contact_notification(submitted):
    if not RESEND_API_KEY or not MAIL_TO:
        app.logger.warning("RESEND_API_KEY/MAIL_TO not set — skipping contact notification email.")
        return

    payload = {
        "from": "Structural Simulation <onboarding@resend.dev>",
        "to": [MAIL_TO],
        "reply_to": submitted["email"],
        "subject": f"New contact form submission from {submitted['name']}",
        "text": (
            "New message from the structsim.com contact form:\n\n"
            f"Name: {submitted['name']}\n"
            f"Phone: {submitted['phone']}\n"
            f"Email: {submitted['email']}\n"
        ),
    }

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "structsim.com-contact-form",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except (urllib.error.URLError, OSError):
        app.logger.exception("Failed to send contact notification email.")


@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(app.static_folder, "sitemap.xml", mimetype="application/xml")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", name="Paulo Victor")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        submitted = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
        }

        send_contact_notification(submitted)

        session["submitted"] = submitted
        return redirect(url_for("contact"))

    submitted = session.pop("submitted", None)
    return render_template("contact.html", submitted=submitted)


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
