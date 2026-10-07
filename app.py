from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "anju"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(200))
    mobile = db.Column(db.String(20))
    service = db.Column(db.String(100))
    date = db.Column(db.String(20))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["GET", "POST"])
def book():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        location = request.form.get("location")
        mobile = request.form.get("mobile")
        service = request.form.get("service")
        date = request.form.get("date")

        new_user = User(
            name=name,
            email=email,
            location=location,
            mobile=mobile,
            service=service,
            date=date
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Booking submitted successfully!")

        return redirect("/book")

    return render_template("index.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)