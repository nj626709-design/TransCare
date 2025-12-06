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

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        return render_template('contact.html')
        if request.method == 'POST':
            try:
                name = request.form.get('name')
                email = request.form.get('email')
                subject = request.form.get('subject')
                message = request.form.get('message')

                msg = Message(
                    subject=f"New Contact Message: {subject}",
                    sender=os.getenv("MAIL_DEFAULT_SENDER"),
                    recipients=[os.getenv("MAIL_USERNAME")]
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

        # Render contact page (no Flask-WTF form needed)
        return render_template('contact.html')

    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        return render_template('quote.html')
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
                    sender=os.getenv("MAIL_DEFAULT_SENDER"),
                    recipients=[os.getenv("MAIL_USERNAME")]
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

        # Render quote page (no Flask-WTF form needed)
        return render_template('quote.html')

    return app


# Only for local development
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
