from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime

# -------------------- Load Environment Variables --------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# -------------------- Mail Configuration --------------------
app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('HOSTINGER_EMAIL')       # Your Hostinger email
app.config['MAIL_PASSWORD'] = os.getenv('HOSTINGER_PASSWORD')    # Your email password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('HOSTINGER_EMAIL') # Sender email

mail = Mail(app)

# -------------------- Helper Function to Log Submissions --------------------
def log_submission(filename, data):
    with open(filename, "a") as f:
        f.write(f"{datetime.now()} - {data}\n{'-'*50}\n")

# -------------------- Home Route --------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------- Contact Form --------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Compose email
        msg = Message(
            subject=f"New Contact Form Submission: {subject}",
            recipients=[app.config['MAIL_USERNAME']],  # Send to yourself
            body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        )

        # Try sending email
        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

        # Log submission as backup
        log_submission("contact.txt", f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage:\n{message}")

        return redirect(url_for('contact'))

    return render_template("contact.html")

# -------------------- Quote Form --------------------
@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Compose email
        msg = Message(
            subject=f"New Quote Request from {name}",
            recipients=[app.config['MAIL_USERNAME']],  # Send to yourself
            body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}"
        )

        # Try sending email
        try:
            mail.send(msg)
            flash("Quote request sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending email: {str(e)}", "danger")

        # Log submission as backup
        log_submission("quote.txt", f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}")

        return redirect(url_for('quote'))

    return render_template("quote.html")

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True)
