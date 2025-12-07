from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)

# Secret key
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Make current year available
@app.context_processor
def inject_year():
    return {"current_year": lambda: datetime.now().year}

# Mail configuration
app.config["MAIL_SERVER"] = "smtp.hostinger.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        try:
            msg = Message(
                subject=f"New Contact Form: {subject}",
                recipients=[app.config["MAIL_USERNAME"]],
                body=f"""
New Contact Message:

Name: {name}
Email: {email}
Subject: {subject}
Message: {message}
                """
            )
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print("Mail error:", e)
            flash("Error sending message.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        vehicle = request.form.get("vehicle_type")
        date_needed = request.form.get("date_needed")
        message = request.form.get("message")

        try:
            msg = Message(
                subject="New Quote Request",
                recipients=[app.config["MAIL_USERNAME"]],
                body=f"""
New Quote / Booking Request:

Name: {name}
Email: {email}
Phone: {phone}
Vehicle Type: {vehicle}
Date Needed: {date_needed}
Message: {message}
                """
            )
            mail.send(msg)
            flash("Your quote request has been submitted!", "success")
        except Exception as e:
            print("Mail error:", e)
            flash("Error sending quote request.", "danger")

        return redirect(url_for("quote"))

    return render_template("quote.html")

# Run
if __name__ == "__main__":
    app.run()
