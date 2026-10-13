# from flask import Flask, render_template, request, redirect, flash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# app.config["SECRET_KEY"] = "anju"

# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     location = db.Column(db.String(200))
#     mobile = db.Column(db.String(20))
#     service = db.Column(db.String(100))
#     date = db.Column(db.String(20))


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/book", methods=["GET", "POST"])
# def book():

#     if request.method == "POST":

#         name = request.form.get("name")
#         email = request.form.get("email")
#         location = request.form.get("location")
#         mobile = request.form.get("mobile")
#         service = request.form.get("service")
#         date = request.form.get("date")

#         new_user = User(
#             name=name,
#             email=email,
#             location=location,
#             mobile=mobile,
#             service=service,
#             date=date
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         flash("Booking submitted successfully!")

#         return redirect("/book")

#     return render_template("index.html")


# with app.app_context():
#     db.create_all()


# if __name__ == "__main__":
#     app.run(debug=True)


import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "anju")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
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
    users = User.query.order_by(User.id.desc()).all()
    return render_template("index.html", users=users)


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            location=request.form.get("location"),
            mobile=request.form.get("mobile"),
            service=request.form.get("service"),
            date=request.form.get("date")
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Booking submitted successfully!", "success")
        except Exception:
            db.session.rollback()
            app.logger.exception("Booking could not be saved")
            flash("Booking save nahi hui. Please try again.", "error")

        return redirect("/")

    return redirect("/")

@app.route("/bookings")
def bookings():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("bookings.html", users=users)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
