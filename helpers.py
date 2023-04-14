from functools import wraps
from flask import g, request, redirect, url_for
from flask import redirect, render_template, request, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Added this validation bc it showed me the key didnt exist in the session dictionary (error)
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        
        if session['user_id'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code