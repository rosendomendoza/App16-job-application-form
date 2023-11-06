from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import os

# Create a Flask app object
app = Flask(__name__)

# Parameters to configure access to the database.
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Parameters to configure flask email function
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "profesor.rosendo@gmail.com"
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

# SQL object to communication between flash app and sqlite database
db = SQLAlchemy(app)

# Mail object to communication between flash app and mail server
mail = Mail(app)


class Form(db.Model):

    # Class that provides capturing post messages from the website
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Capture the message post
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name, last_name, email, date_obj, occupation)

        # Set the engine database
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)

        # Insert the data into the database
        db.session.add(form)
        db.session.commit()

        # Set up the parts of the email and send it
        message_body = (f"Thank for your submission, {first_name}\n"
                        f"This data was submitted for you:\n"
                        f"{first_name}\n"
                        f"{last_name}\n"
                        f"{date}")
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        # Send confirmation message to the user through the website
        flash(f"{first_name} your data was submitted successfully ")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        # if database don't exit, then create it.
        db.create_all()

        # Execute de app Object
        app.run(debug=True, port=5001)
