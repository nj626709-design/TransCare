from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)

    # -----------------------------
    # General Config
    # -----------------------------
    app.secret_key = os.getenv("SECRET_KEY") or "supersecretkey"

    # Make current year available in all templates
    @app.context_processor
    def inject_year():
        return {"current_year": lambda: datetime.now().year}

    # -----------------------------
    # Mail Config
    # -----------------------------
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", app.config['MAIL_USERNAME'])

    mail.init_app(app)

    # -----------------------------
    # Routes
    # -----------------------------
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

    # -----------------------------
    # Contact Form
    # -----------------------------
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            try:
                name = request.form.get('name')
                email = request.form.get('email')
                subject = request.form.get('subject')
                message = request.form.get('message')

                msg = Message(
                    subject=f"New Contact Message: {subject}",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[app.config['MAIL_USERNAME']]
                )

                msg.body = f"""
New Contact Message from TransCare Website

Name: {name}
Email: {email}
Subject: {subject}
Message:
{message}
"""

                mail.send(msg)
                flash("Your message has been sent successfully!", "success")
                return redirect(url_for('home'))

            except Exception as e:
                print("Error sending email:", e)
                flash("Something went wrong. Please try again.", "danger")
                return redirect(url_for('home'))

        return render_template('contact.html')

    # -----------------------------
    # Quote Form
    # -----------------------------
    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        if request.method == 'POST':
            try:
                name = request.form.get('name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                pickup = request.form.get('pickup')
                drop = request.form.get('drop')
                goods = request.form.get('goods')
                weight = request.form.get('weight')

                msg = Message(
                    subject="New Quote Request",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[app.config['MAIL_USERNAME']]
                )

                msg.body = f"""
New Quote Request from TransCare Website

Name: {name}
Email: {email}
Phone: {phone}

Pickup Location: {pickup}
Drop Location: {drop}

Type of Goods: {goods}
Weight: {weight} kg
"""

                mail.send(msg)
                flash("Quote request sent successfully!", "success")
                return redirect(url_for('home'))

            except Exception as e:
                print("Error sending quote:", e)
                flash("Failed to send quote. Please try again.", "danger")
                return redirect(url_for('home'))

        return render_template('quote.html')

    # -----------------------------
    # Favicon (optional)
    # -----------------------------
    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))

    return app


# -----------------------------
# Run locally only
# -----------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
