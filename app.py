import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///progressions.db")


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    #TODO show progressions and let user pick one to edit
    data = db.execute("SELECT id, name, last_modified FROM progressions WHERE user_id = ?")
    return render_template("index.html", rows=[{"id": "g31yuy31yg", "name": "TeST", "last_modified": "2/5/43"}, ])


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """create new project"""
    #TODO
    if request.method == "POST":
        if not request.form.get("name"):
            return apology("must provide progression name", 403)

        elif (not request.form.get("time_signature")) or (not is_int(request.form.get("time_signature"))) or (int(request.form.get("time_signature")) < 1):
            return apology("must provide a time signature (_/4)", 403)

        elif db.execute("SELECT id FROM progressions WHERE user_id = ? AND name = ?", session.get("user_id"), request.form.get("name")):
            return apology("There is already a progression whith that name", 403)

        db.execute("INSERT INTO progressions (user_id, name, time_signature) VALUES (?,?,?)", session.get("user_id"), request.form.get("name"), request.form.get("time_signature"))
        id = db.execute("SELECT id FROM progressions WHERE user_id = ? AND name = ? AND time_signature = ?", session.get("user_id"), request.form.get("name"), request.form.get("time_signature"))

        return redirect(url_for('.edit', id=id))
    else:
        return render_template("new.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """edit existing project"""
    #TODO
    if request.method == "POST":
        return redirect("/edit")
    else:
        progression_id = request.args['id']
        return render_template("edit.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return apology("that username is already taken", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password must be the same as the password confirmation", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        return login()

    else:
        return render_template("register.html")


