import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import json

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
    data = db.execute("SELECT id, name, last_modified FROM progressions WHERE user_id = ? ORDER BY last_modified DESC", session.get("user_id"))
    return render_template("index.html", rows=data)


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """create new project"""
    if request.method == "POST":
        if not request.form.get("name"):
            return apology("must provide progression name", "/new")

        elif (not request.form.get("time_signature")) or (not is_int(request.form.get("time_signature"))) or (int(request.form.get("time_signature")) < 1):
            return apology("must provide a time signature (_/4)", "/new")

        elif (not request.form.get("tempo")) or (not is_int(request.form.get("tempo"))) or (int(request.form.get("tempo")) < 1):
            return apology("must provide a tempo (beats per minute)", "/new")

        elif db.execute("SELECT id FROM progressions WHERE user_id = ? AND name = ?", session.get("user_id"), request.form.get("name")):
            return apology("There is already a progression with that name", "/new")

        db.execute("INSERT INTO progressions (user_id, name, time_signature, tempo) VALUES (?,?,?,?)", session.get("user_id"), request.form.get("name"), request.form.get("time_signature"), request.form.get("tempo"))
        data = db.execute("SELECT id FROM progressions WHERE user_id = ? AND name = ?", session.get("user_id"), request.form.get("name"))

        return redirect(url_for('.edit', id=data[0]["id"]))
    else:
        return render_template("new.html")

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """delete project"""
    db.execute("DELETE FROM progressions WHERE id = ? AND user_id = ?", request.form.get("id"), session.get("user_id"))
    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """edit existing project"""
    def encode(data):
        chords = db.execute("SELECT id, time, length, name FROM chords WHERE progression_id = ? ORDER BY time", data["id"])
        for chord in chords:
            notes = db.execute("SELECT note FROM notes WHERE chord_id = ?", chord.pop("id"))
            chord.update({"notes":[x["note"] for x in notes]})
        data.update({"chords":chords})
        return data

    if request.method == "POST":
        #TODO save the progression (remember to update last modified)
        data = json.loads(request.form.get("data"))
        db.execute("DELETE FROM progressions WHERE id = ? AND user_id = ?", data["id"], session.get("user_id"))
        db.execute()
        print(data)
        return redirect("/")
    else:
        progression_id = request.args['id']

        #TODO let the user edit the progression
        progression = db.execute("SELECT id, name, time_signature, tempo FROM progressions WHERE id = ? AND user_id = ?", progression_id, session.get("user_id"))

        if not progression:
            return apology("could not find this progression", "/")
        encode(progression[0])
        return render_template("edit.html", progression=progression[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", "/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", "/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", "/login")

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
            return apology("must provide username", "/register")

        if len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return apology("that username is already taken", "/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", "/register")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", "/register")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password must be the same as the password confirmation", "/register")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        return login()

    else:
        return render_template("register.html")


