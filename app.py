from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)

    # make current_year available in all templates
    @app.context_processor
    def inject_year():
        return {"current_year": lambda: datetime.now().year}

    app.secret_key = os.getenv("SECRET_KEY")

    # ========================
    #      EMAIL SETTINGS
    # ========================
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)

    # ========================
    #       ROUTES
    # ========================
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/services')
    def services():
        return render_template('services.html')

    @app.route('/clients')
    def clients():
        return render_template('clients.html')

    # ------------------------
    # CONTACT FORM FIXED
    # ------------------------

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get("name")
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")

            send_email(
                subject=f"New Contact Message: {subject}",
                sender=email,
                recipients=['yourmail@yourdomain.com'],
                body=f"""
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject}
Message:
{message}
"""
                )
            return render_template("success.html", msg="Your message has been sent!")
        return render_template("contact.html")

    # ------------------------
    # QUOTE FORM FIXED
    # ------------------------

    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        if request.method == 'POST':
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            vehicle_type = request.form.get("vehicle_type")
            date_needed = request.form.get("date_needed")
            message = request.form.get("message")

            send_email(
                subject="New Quote Request",
                sender=email,
                recipients=['yourmail@yourdomain.com'],
                body=f"""
New quote request:

Name: {name}
Email: {email}
Phone: {phone}
Vehicle: {vehicle_type}
Date Needed: {date_needed}
Message:
{message}
"""
                )
            return render_template("success.html", msg="Your quote request has been submitted!")

        return render_template("quote.html")

    # Only for local development
    if __name__ == "__main__":
        app = create_app()
        app.run(debug=True)
