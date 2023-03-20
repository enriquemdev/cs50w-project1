import os

from flask import Flask, session, redirect, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # TODO: Add the user's entry into the database
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        if not username or not password or not confirmation:
            return "bad register" #apology("Llena todos los campos")

        if password != confirmation:
            return "bad register" #apology("La contraseña debe ser igual a su confirmacion")
        
        query = text("SELECT username from users WHERE (username = :username)")
        verfUsuarioExistente = db.execute(query, {"username": username}).fetchall()
        db.commit()

        if len(verfUsuarioExistente) != 0:
            return "bad register" #apology("El nombre de usuario ya existe! :(")
        
        query = text("INSERT INTO users (username, hashed_pass) VALUES(:username, :hashed_pass)")
        db.execute(query, {"username": username, "hashed_pass": generate_password_hash(password)})
        db.commit()
        
        return redirect(url_for("register"))

    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form["username"]:
            return "BAD USER" #apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form["password"]:
            return "bad ps" #apology("must provide password", 403)

        # Query database for username
        query = text("SELECT user_id, username, hashed_pass FROM users WHERE username = :username")
        user = db.execute(query, {"username":request.form["username"]}).fetchone()
        #db.commit()
        
        # print(rows)
        # for flight in rows:
        #      print(f"{flight.user_id} to {flight.username}, {flight.hashed_pass} minutes.")
        # print(type(rows[0]))

        # Ensure username exists and password is correct 
        if user == None or not check_password_hash(user.hashed_pass, request.form["password"]): #row 0 col 2
            return "bad login" #apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.user_id

        # Redirect user to home page
        return redirect(url_for("index"))

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


@app.route("/")
@login_required
def index():
    return render_template("index.html")


