from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong secret in production

# -----------------------------
# Mail Configuration
# -----------------------------
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.hostinger.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# -----------------------------
# Context processor for footer
# -----------------------------
@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# -----------------------------
# Async Email Helper
# -----------------------------
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

# -----------------------------
# Contact Route
# -----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not all([name, email, subject, message]):
            flash("Please fill all fields.", "warning")
            return redirect(url_for("contact"))

        # Optional: Save to text file
        with open("contact_submissions.txt", "a") as f:
            f.write(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}\n{'-'*50}\n")

        # Send email asynchronously
        msg = Message(
            subject=f"New Contact Form: {subject}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        )
        threading.Thread(target=send_async_email, args=(app, msg)).start()

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# -----------------------------
# Quote Route
# -----------------------------
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

        # Optional: Save to text file
        with open("quote_submissions.txt", "a") as f:
            f.write(f"{data}\n{'-'*50}\n")

        # Send email asynchronously
        msg = Message(
            subject=f"New Quote Request: {data['vehicle_type']} {data['vehicle_subtype']}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"""
Quote Request Details:

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Vehicle Type: {data['vehicle_type']}
Vehicle Subtype: {data['vehicle_subtype']}
Date Needed: {data['date_needed']}
Message: {data['message']}
"""
        )
        threading.Thread(target=send_async_email, args=(app, msg)).start()

        print("QUOTE RECEIVED:", data)
        flash("Your quote request has been submitted successfully!", "success")
        return redirect(url_for("quote"))

    return render_template("quote.html")

# -----------------------------
# Happy Clients
# -----------------------------
@app.route("/clients")
def clients():
    return render_template("clients.html")

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
