import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""

    # Get user's current cash
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Get user holdings (grouped by symbol)
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id,
    )

    holdings = []
    total = cash

    for row in rows:
        quote = lookup(row["symbol"])
        total_value = quote["price"] * row["total_shares"]
        holdings.append(
            {
                "symbol": row["symbol"],
                "name": quote["name"],
                "shares": row["total_shares"],
                "price": quote["price"],
                "total": total_value,
            }
        )
        total += total_value

    return render_template("index.html", holdings=holdings, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate input
        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer")

        shares = int(shares)
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol")

        price = quote["price"]
        cost = price * shares

        # Check user cash
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        if cash < cost:
            return apology("can't afford")

        # Deduct cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
            user_id,
            quote["symbol"],
            shares,
            price,
            "BUY",
        )

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, shares, price, type, timestamp FROM transactions WHERE user_id = ? ORDER BY time DESC",
        user_id,
    )
    return render_template("history.html", transactions=rows)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol")

        return render_template(
            "quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"]
        )

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords do not match")

        # Insert new user
        hash_pw = generate_password_hash(password)
        try:
            new_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash_pw,
            )
        except ValueError:
            return apology("username already exists")

        # Log the user in
        session["user_id"] = new_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be positive integer")

        shares = int(shares)

        # Check if user has enough shares
        owned = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )[0]["total_shares"]

        if owned is None or shares > owned:
            return apology("not enough shares")

        # Lookup stock price
        quote = lookup(symbol)
        price = quote["price"]
        value = price * shares

        # Update cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", value, user_id)

        # Record transaction (negative shares or type='sell')
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
            user_id,
            symbol,
            -shares,
            price,
            "SELL",
        )

        flash("Sold!")
        return redirect("/")

    else:
        # List symbols user owns
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id,
        )
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols])
