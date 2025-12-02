import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "transcare.sqlite"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail (optional - configure to enable email notifications)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # your smtp username
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # your smtp password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "no-reply@transcare.com")
