import os

from flask import Flask, session, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
import requests #para hacer peticiones a la api de goodreads

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
        
        return redirect(url_for("login"))

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html", esBusqueda="false")
    
    elif request.method == "POST":
        text1 = request.form.get("text")
        search_param = request.form.get("search_param")
        
        if not text1 or not search_param:
            return apology("Llena todos los campos para la búsqueda please")
        
        query = """
                SELECT books.book_id, books.ISBN as isbn, books.book_title,
                string_agg(authors.author_name, ', ') AS authors
                FROM books 
                INNER JOIN book_authors ON books.book_id = book_authors.id_book
                INNER JOIN authors ON book_authors.id_author = authors.author_id
                WHERE(
                """
                
        # Using lower function bc it makes the search case insensitive
        if search_param == "ISBN":
            query += """
                     (LOWER(books.ISBN) LIKE :ISBN)
                     """
        elif search_param == "book":
            query += """
                     (LOWER(books.book_title) LIKE :book_title)
                     """
        elif search_param == "author":
            query += """
                     (LOWER(authors.author_name) LIKE :author_name)
                     """
                     
        query += """
                 )
                 GROUP BY books.book_id
                 ORDER BY books.book_title
                 """
                    
        query = text(query)
        
        resultado = db.execute(query,{"ISBN": ("%"+text1.lower()+"%"), "book_title": ("%"+text1.lower()+"%"), 
                            "author_name": ("%"+text1.lower()+"%")})     
        
        # This is a list of lists(a list of the rows)
        librosObtenidos = resultado.fetchall()
        
        # Kristin Hannah is repeated through the authors
        # The Mask has two authors
        
        db.commit()
        
        return render_template("index.html", libros=librosObtenidos, esBusqueda="true", text1=text1)
    

@app.route('/book/<int:book_id>', methods=["GET"])
@login_required
def show_book(book_id):
    # if not os.getenv("BOOKS_API_KEY"):
    #     raise RuntimeError("BOOKS_API_KEY is not set")
    
    
    # Obtain general info of the book in the db
    query = """
            SELECT books.book_title, books.ISBN as isbn, books.book_year,
            string_agg(authors.author_name, ', ') AS authors
            FROM books 
            INNER JOIN book_authors ON books.book_id = book_authors.id_book
            INNER JOIN authors ON book_authors.id_author = authors.author_id
            WHERE(books.book_id = :book_id)
            GROUP BY books.book_id
            """
    query = text(query)
    datos_libro = db.execute(query,{"book_id": book_id}) 
    datos_libro = datos_libro.fetchone()
    
    # Obtain the avg rating and ratings quantity from api
    api_response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+datos_libro.isbn)
    
    if api_response.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    else:
        api_response = api_response.json()
    
    if api_response["totalItems"] != 0:
        datos_api = {
            "description": api_response["items"][0]["volumeInfo"]["description"] if "description" in api_response["items"][0]["volumeInfo"] else "none",
            "image_url": api_response["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in api_response["items"][0]["volumeInfo"] else "none",
            "avg_rating": api_response["items"][0]["volumeInfo"]["averageRating"] if "averageRating" in api_response["items"][0]["volumeInfo"] else "none",
            "ratings_quantity": api_response["items"][0]["volumeInfo"]["ratingsCount"] if "ratingsCount" in api_response["items"][0]["volumeInfo"] else "none"
        }
    else:
        datos_api = False
    
    
    # Obtain the current user review if it exists
    query = """
            SELECT review_points, review_content, created_at as review_date
            FROM book_reviews 
            WHERE(
                review_user = :review_user AND
                review_book = :book_id
                )
            """
    query = text(query)
    user_review = db.execute(query,{"book_id": book_id, "review_user": session["user_id"]})
    if  user_review is None:
        user_review = False
    else:
        user_review = user_review.fetchone()
        
    # Obtain the reviews from other users
    query = """
            SELECT review_points, review_content, 
            to_char(book_reviews.created_at, 'DD-MM-YYYY HH:MI:SS') as review_date,
            review_user, users.username
            FROM book_reviews 
            INNER JOIN users ON book_reviews.review_user = users.user_id
            WHERE(
                review_user != :review_user AND
                review_book = :book_id
                )
            """
    query = text(query)
    reviews = db.execute(query,{"book_id": book_id, "review_user": session["user_id"]})
    if  reviews is None:
        reviews = False
    else:
        reviews = reviews.fetchall()
        
    return render_template("book.html", book_id=book_id, datos_libro=datos_libro, datos_api=datos_api, user_review=user_review, reviews=reviews)


@app.route('/saveReview', methods=["POST"])
@login_required
def saveReview():
    book_id = request.form.get("book_id")
    star_count = request.form.get("star_count")
    review_content = request.form.get("review_content")
    print(book_id, star_count, review_content)
    
    if not book_id or not star_count or not review_content:
        return apology("Llena todos los campos para guardar la reseña please")
    
    if star_count not in ["1", "2", "3", "4", "5"]:
        return apology("Selecciona una cantidad de estrellas válida please")
    
    query = """
            INSERT INTO book_reviews
            (review_book, review_user, review_points, review_content)
            VALUES (:review_book, :review_user, :review_points, :review_content)
            """
    query = text(query)
    
    db.execute(query,{"review_book": book_id, "review_user": session["user_id"], 
                        "review_points": star_count, "review_content": review_content})     
    
    db.commit()
    
    return redirect("/book/"+book_id)

@app.route("/api/<string:isbn>")
def book_api(isbn):
    """Return api response from data in the database of books"""
    
    # Make sure book exists.
    query = """
            SELECT books.book_title, books.ISBN as isbn, books.book_year,
            string_agg(authors.author_name, ', ') AS authors,
            COUNT(book_reviews.review_id) as review_count, AVG(book_reviews.review_points) as review_points
            FROM books
            INNER JOIN book_authors ON books.book_id = book_authors.id_book
            INNER JOIN authors ON book_authors.id_author = authors.author_id
            INNER JOIN book_reviews ON books.book_id = book_reviews.review_book
            WHERE(books.ISBN = :ISBN)
            GROUP BY books.book_id
            """
    query = text(query)
    
    book = db.execute(query,{"ISBN": isbn})
    
    db.commit()
    
    print(book)
    if book.rowcount > 0:
        book = book.fetchone()
        
        return jsonify({
                "title": book.book_title,
                "author": book.authors,
                "year": book.book_year,
                "isbn": book.isbn,
                "review_count": book.review_count,
                "average_score": book.review_points
            })
    else:
        return jsonify({"error": "Invalid ISBN"}), 404