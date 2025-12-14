from flask import Flask, render_template, request
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# Mail config (ensure .env values are correct)
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USERNAME='your@email.com',
    MAIL_PASSWORD='yourpassword',
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False
)
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

# Quote route
@app.route("/quote", methods=["GET", "POST"])
def quote():
    success = False
    if request.method == "POST":
        client_name = request.form.get("name")
        client_email = request.form.get("email")
        service = request.form.get("service")
        details = request.form.get("details")
        try:
            msg = Message(
                subject=f"Quote Request: {service}",
                recipients=[app.config.get("MAIL_USERNAME")],
                body=f"Name: {client_name}\nEmail: {client_email}\nDetails:\n{details}"
            )
            mail.send(msg)
            success = True
        except Exception as e:
            print("Mail error:", e)
    return render_template("quote.html", success=success)

#Happy Clients route
@app.route('/clients')
def clients():
    return render_template('clients.html')

if __name__ == "__main__":
    app.run(debug=True)
