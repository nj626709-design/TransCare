from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mail config (ensure .env values are correct)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# Context processor for footer
@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# Helper function to send emails asynchronously
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Services route
@app.route('/services')
def services():
    return render_template('services.html')

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not (name and email and subject and message):
            flash("Please fill all fields.", "warning")
            return redirect(url_for('contact'))

        # Save contact info to a text file (optional)
        with open("contact_submissions.txt", "a") as f:
            f.write(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}\n{'-'*50}\n")

        # Send email asynchronously
        try:
            msg = Message(
                subject=f"New Contact Form: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],  # your email
                body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            )
            threading.Thread(target=send_async_email, args=(app, msg)).start()
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send message: {str(e)}", "danger")

        return redirect(url_for('contact'))

    return render_template("contact.html")

# Quote route
@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "vehicle_type": request.form.get("vehicle_type"),
            "vehicle_subtype": request.form.get("vehicle_subtype"),
            "date_needed": request.form.get("date_needed"),
            "message": request.form.get("message"),
        }

        # LOG ONLY (safe)
        print("QUOTE RECEIVED:", data)

        flash("Your quote request has been submitted successfully!", "success")
        return redirect(url_for("quote"))

    return render_template("quote.html")

# Happy Clients route
@app.route('/clients')
def clients():
    return render_template('clients.html')

if __name__ == "__main__":
    app.run(debug=True)
