import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
#0782

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #Query Database for stocks
    rows = db.execute("SELECT  stock_name,symbol,SUM(shares) AS total FROM portifolio WHERE user_id  = :user_id GROUP BY stock_name HAVING SUM(shares) > 0",
    user_id = session["user_id"])
    # add the total and price for each stock
    for row in rows:
        stock_symbol = lookup(row["symbol"])
        row["price"] = stock_symbol["price"]
        row["amount"] = row["price"] * row["total"]
    #Query database for user cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",user_id = session["user_id"])
    moola = cash[0]["cash"]
    # find the total value of stocks
    total_amount = 0
    # iterate over individual stocks to amount
    for row in rows:
        total_amount += row["amount"]
    #add cash and total stock value to find total value of portfolio
    total = total_amount + moola


    return render_template("index.html",rows = rows,moola = moola,total = total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock_symbol = lookup(request.form.get("symbol"))
        number = int(request.form.get("shares"))
        #Ensure symbol is submitted
        if not stock_symbol:
            return apology("Please enter symbol",403)
        #Ensure number of shares is submitted
        elif not request.form.get("shares") or number < 0:
            return apology("Please enter valid number of shares",403)

        else:
             # see if user has enough cash
            rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
            amount = stock_symbol["price"] * number
            if rows[0]["cash"] <  amount:
                return apology("Not enough cash",403)
            else:
                # execute sql statements to update tables
                db.execute("INSERT INTO portifolio (user_id,symbol, stock_name,shares,date,action,price) VALUES (:user_id, :symbol,:stock_name,:shares, datetime('now'),'Buy',:price)",
                user_id = session["user_id"], stock_name = stock_symbol["name"], shares = number, symbol = stock_symbol["symbol"], price = stock_symbol["price"])
                db.execute("UPDATE users SET cash = cash - :amount", amount = amount)
                #redirect to index page
                return redirect("/")
    # Acess by GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #query portifolio table
    rows = db.execute("SELECT date,symbol,action,price,shares FROM portifolio")
    for row in rows:
        row["amount"] = row["price"] * row["shares"]

    return render_template("history.html",rows = rows)

@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """Allow user to top up cash to amount"""
    # User reached via POST
    if request.method == "POST":
        amount = int(request.form.get("amount"))
        # Check if user enters amount
        if not amount:
            return apology("Please enter amount",403)
        else:
            db.execute("UPDATE users SET cash = cash + :amount", amount = amount)
            return redirect("/")
    #User reached via GET
    else:
        return render_template("topup.html")

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
     # user reached via POST
    if request.method == "POST":
        stock_symbol = lookup(request.form.get("symbol"))
        # check if symbol is valid
        if not stock_symbol:
            return apology("enter valid symbol")
        # Display quoted stock
        else:
            return render_template("quoted.html",name = stock_symbol["name"],
            symbol = stock_symbol["symbol"], price = stock_symbol["price"])
    # user reached via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure user confirms password
        elif not request.form.get("confirmation"):
            return apology("must confirm password",403)

        # Check if passwords entered are the Ssame
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match",403)

        # hash password
        hash =  generate_password_hash(request.form.get("password"))

        # Insert user into database
        result = db.execute(" INSERT INTO users (username,hash) VALUES (:username, :hash)",username =request.form.get("username"),hash=hash)

        if not result:
            return apology("user already exists!",403)

        # query user

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # log in user automatically
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        stock_symbol = lookup(request.form.get("symbol"))
        number = int(request.form.get("shares"))
        #Ensure symbol is submitted
        if not stock_symbol:
            return apology("Please enter symbol",403)
        #Ensure number of shares is submitted
        elif not request.form.get("shares") or number < 0:
            return apology("Please enter valid number of shares",403)

        else:
             # see if user has stock entered
            rows = db.execute("SELECT symbol,SUM(shares) AS total FROM portifolio WHERE user_id = :user_id AND symbol = :symbol", user_id = session["user_id"],symbol = stock_symbol["symbol"])
            if not rows[0]["symbol"]:
                return apology("No stock in portifolio",403)
            else:
                # execute sql statements to update tables
                amount = stock_symbol["price"] * number
                number = number * -1
                db.execute("INSERT INTO portifolio (user_id,symbol, stock_name,shares,date,action,price) VALUES (:user_id, :symbol,:stock_name,:shares,datetime('now'),'Sell',:price)",
                user_id = session["user_id"], stock_name = stock_symbol["name"], shares = number, symbol = stock_symbol["symbol"], price = stock_symbol["price"])
                db.execute("UPDATE users SET cash = cash + :amount", amount = amount)
                #redirect to index page
                return redirect("/")
    # Acess by GET
    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
