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
    app.secret_key = "supersecretkey"

    # Make current year available in all templates
    @app.context_processor
    def inject_year():
        return {"current_year": lambda: datetime.now().year}

    # -----------------------------
    # Mail Config
    # -----------------------------
    app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
    app.config['MAIL_PORT'] = 587        # Use 465 for SSL
    app.config['MAIL_USE_TLS'] = True   # False if using SSL on 465
    app.config['MAIL_USE_SSL'] = False  # True if using SSL on 465
    app.config['MAIL_USERNAME'] = 'info@transcaretransport.in'
    app.config['MAIL_PASSWORD'] = 'Cady@123'


    mail = Mail(app)

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
        return render_template('contact.html')

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

            try:
                msg = Message(
                    subject=f"New Contact Message: {subject}",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[app.config['info@transcaretransport.in']]
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
                
            except Exception as e:
                print("Error sending email:", e)
                flash("Something went wrong. Please try again.", "danger")
                return redirect(url_for('contact'))

        # GET request
        return render_template('contact.html')

    # -----------------------------
    # Quote Form
    # -----------------------------
    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        return render_template('quote.html')
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            pickup = request.form.get('pickup')
            drop = request.form.get('drop')
            goods = request.form.get('goods')
            weight = request.form.get('weight')

            try:
                msg = Message(
                subject="New Quote Request",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['info@transcaretransport.in']]
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
                
            except Exception as e:
                print("Error sending quote:", e)
                flash("Failed to send quote. Please try again.", "danger")
                return redirect(url_for('quote'))

        return render_template('quote.html')

    return app


# -----------------------------
# WSGI / Local development
# -----------------------------
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
