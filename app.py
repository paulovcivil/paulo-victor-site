import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False") == "True"

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO", MAIL_USERNAME)


def send_contact_notification(submitted):
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        app.logger.warning("MAIL_USERNAME/MAIL_PASSWORD not set — skipping contact notification email.")
        return

    message = EmailMessage()
    message["Subject"] = f"New contact form submission from {submitted['name']}"
    message["From"] = MAIL_USERNAME
    message["To"] = MAIL_TO
    message["Reply-To"] = submitted["email"]
    message.set_content(
        "New message from the structsim.com contact form:\n\n"
        f"Name: {submitted['name']}\n"
        f"Phone: {submitted['phone']}\n"
        f"Email: {submitted['email']}\n"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(message)
    except smtplib.SMTPException:
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
