from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret123")


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
    success = False
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        try:
            msg = Message(
                subject=f"Contact Form: {subject}",
                recipients=[app.config.get("MAIL_USERNAME")],
                body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            )
            mail.send(msg)
            success = True
        except Exception as e:
            print("Mail error:", e)
    return render_template("contact.html", success=success)

#Quote route
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

#Happy Clients route
@app.route('/clients')
def clients():
    return render_template('clients.html')

if __name__ == "__main__":
    app.run(debug=True)
