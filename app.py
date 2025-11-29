from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, QuoteRequest
from forms import QuoteForm, ContactForm
from flask_mail import Mail, Message
from datetime import datetime
import os

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Ensure instance folder exists
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

    db.init_app(app)
    mail = Mail(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/services')
    def services():
        return render_template('services.html')

    @app.route('/fleet')
    def fleet():
        vehicles = [
            {"name": "20 Ton Truck", "desc": "Ideal for long-haul freight"},
            {"name": "Container Truck", "desc": "For secured container shipments"},
            {"name": "Cargo Van", "desc": "Small shipments and express deliveries"},
            {"name": "Tempo", "desc": "Short-distance & local deliveries"},
        ]
        return render_template('fleet.html', vehicles=vehicles)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            try:
                msg = Message(
                    subject=f"Transcare Contact from {form.name.data}",
                    recipients=[app.config.get("MAIL_DEFAULT_SENDER")]
                )
                msg.body = f"Name: {form.name.data}\nEmail: {form.email.data}\nPhone: {form.phone.data}\n\nMessage:\n{form.message.data}"
                mail.send(msg)
            except Exception:
                flash("Message recorded. (Email sending failed)", "warning")

            flash("Thanks — we received your message.", "success")
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    @app.route('/quote', methods=['GET', 'POST'])
    def quote():
        form = QuoteForm()
        if form.validate_on_submit():
            qr = QuoteRequest(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                pickup=form.pickup.data,
                dropoff=form.dropoff.data,
                date_needed=form.date_needed.data,
                vehicle_type=form.vehicle_type.data,
                message=form.message.data,
            )
            db.session.add(qr)
            db.session.commit()

            try:
                msg = Message(
                    subject=f"New Quote Request from {qr.name}",
                    recipients=[app.config.get("MAIL_DEFAULT_SENDER")]
                )
                msg.body = f"""
New Quote Request
Name: {qr.name}
Email: {qr.email}
Phone: {qr.phone}
Pickup: {qr.pickup}
Dropoff: {qr.dropoff}
Date Needed: {qr.date_needed}
Vehicle: {qr.vehicle_type}
Message: {qr.message}
"""
                mail.send(msg)
            except Exception:
                flash("Quote saved. Email sending failed.", "warning")
            else:
                flash("Quote submitted successfully!", "success")

            return redirect(url_for('quote'))

        return render_template('quote.html', form=form)

    @app.route('/admin/quotes')
    def admin_quotes():
        quotes = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
        return render_template('admin_quotes.html', quotes=quotes)

    @app.context_processor
    def inject_globals():
        return {
            'current_year': lambda: datetime.now().year,
            'config': {'SITE_NAME': 'TransCare'}
        }

    return app


# 🔥 THIS IS IMPORTANT FOR RENDER (GLOBAL app variable)
app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
