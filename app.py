import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DEBUG_MODE = os.getenv("FLASK_DEBUG", "False") == "True"


@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}


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

        session["submitted"] = submitted
        return redirect(url_for("contact"))

    submitted = session.pop("submitted", None)
    return render_template("contact.html", submitted=submitted)


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
