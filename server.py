"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=['GET'])
def login_form():
    """Go to login_form.html"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login():
    """Log in to session if user is in the database."""

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No identical user found.")
        return redirect("/login")
    elif user.password != password:
        flash("Password is incorrect.")
        return redirect("/login")

    session["user_id"] = user.user_id
    flash("You are now logged in!")

    return redirect("/")


@app.route('/logout')
def logout():
    """Log out of session."""

    del session["user_id"]
    flash("You are now logged out!")

    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()