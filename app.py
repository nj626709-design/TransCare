# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.hostinger.com'  # or your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # your email password/app password

mail = Mail(app)

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

        # Send email
        try:
            msg = Message(
                subject=f"New Contact Form: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],  # your email
                body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send message: {str(e)}", "danger")

        return redirect(url_for('contact'))

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
