from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class QuoteForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=50)])
    pickup = StringField("Pickup location", validators=[DataRequired(), Length(max=255)])
    dropoff = StringField("Dropoff location", validators=[DataRequired(), Length(max=255)])
    date_needed = StringField("Date needed (optional)")
    vehicle_type = SelectField("Vehicle type",
                               choices=[("truck", "Truck"), ("container","Container"),
                                        ("tempo","Tempo"), ("van","Van"), ("other","Other")])
    message = TextAreaField("Details", validators=[Length(max=2000)])
    submit = SubmitField("Request Quote")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[Length(max=50)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send Message")
