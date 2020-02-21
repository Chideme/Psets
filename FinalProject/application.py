import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from helpers import apology, login_required, usd

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
db = SQL("sqlite:///driveway.db")

@app.route("/")
@login_required
def index():
    """Show current product prices"""
    result = db.execute("SELECT username FROM users WHERE UserID = :UserID",UserID = session["user_id"])
    User = result[0]["username"].capitalize()

    return render_template("index.html",User=User)

@app.route("/pricechange",methods =["GET","POST"])
@login_required
def pricechange():
    """Update product prices"""
    if request.method == "POST":
        date = request.form.get("date")
        product = request.form.get("PriceUpdates")
        sellingPrice = float(request.form.get("SellingPrice"))
        costPrice = sellingPrice - float(request.form.get("Margin"))
        result = db.execute("INSERT INTO price_updates (date,product,selling_price,cost_price) VALUES (:date,:product,:sellingPrice,:costPrice)",date=date,product=product,sellingPrice=sellingPrice,costPrice=costPrice)
        #return "{}".format(result) test
        return redirect("/")
    else:
         return render_template("pricechange.html")


@app.route("/tankdips", methods=["GET", "POST"])
@login_required
def tankdips():
    """Enter tank dips"""
    #If user request using POST
    if request.method == "POST":
        date = request.form.get("date")
        tankID = request.form.get("tankid")
        dip = request.form.get("dip")
        result = db.execute("INSERT INTO TankDips (date, tankID, dip) VALUES (:date, :tankID, :dip)",date=date,tankID=tankID,dip=dip)

        return redirect("/")

    else:
        return render_template("tankdips.html")

@app.route("/pumpreading", methods=["GET", "POST"])
@login_required
def pumpreading():
    """Enter pump readings"""
    # User reached via POST
    if request.method == "POST":
        date = request.form.get("date")
        pumpID = request.form.get("pumpid").upper()
        reading = request.form.get("reading")
        result = db.execute("INSERT INTO pumpReadings (date, pumpID, reading) VALUES (:date, :pumpID, :reading)",date=date,pumpID=pumpID,reading=reading)

        return redirect("/")

    return render_template("pumpreading.html")



@app.route("/delivery", methods=["GET", "POST"])
@login_required
def delivery():
    """Enter delivery"""
    #If user request using POST
    if request.method == "POST":
        date = request.form.get("date")
        tankID = request.form.get("tankid")
        qty = request.form.get("delivery")
        result = db.execute("INSERT INTO deliveries (date, tankID, quantity) VALUES (:date, :tankID, :quantity)",date=date,tankID=tankID,quantity=qty)


        return redirect("/")
    #User access via GET
    else:
        return render_template("delivery.html")

@app.route("/getdriveway",methods= ["GET","POST"])
@login_required
def getdriveway():
    """Show driveway"""
    if request.method == "POST":
        #pick opening date
        cldate = request.form.get("date") #requested day closing dip
        opdate = datetime.strptime(request.form.get("date"),'%Y-%m-%d').date()
        opdate = opdate - timedelta(days = 1) #previous day closing dip
        opening_stock_tank = db.execute("SELECT a.date as date, a.tankID as tankID,a.dip as dip,b.pumpID as pumpID FROM TankDips a JOIN pumps b ON a.tankID= b.tankID WHERE date = :opdate", opdate=opdate)
        closing_stock_tank = db.execute("SELECT a.date,a.tankID, b.quantity AS delivery ,a.dip AS closing_dip FROM TankDips a JOIN deliveries b ON a.tankID = b.tankID  WHERE a.date = :cldate",cldate=cldate)
        #match TankID from the two list
        for i in opening_stock_tank:
           for j in closing_stock_tank:
               if i["tankID"] == j["tankID"]:
                    j["sales"] = i["dip"]+j["delivery"]  - j["closing_dip"]
                    j["opening_dip"] = i["dip"]
                    j["pumpID"] = i["pumpID"]
        #query pumps table
        opening_stock_pump = db.execute("SELECT * FROM pumpReadings WHERE date = :opdate",opdate=opdate)
        closing_stock_pump = db.execute("SELECT a.date, a.pumpID as pumpID, a.reading,b.product FROM pumpReadings a JOIN pumps b ON a.pumpID = b.pumpID  WHERE a.date = :cldate",cldate=cldate)
        # match pumpID from the pump queries
        for i in opening_stock_pump:
            for j in closing_stock_pump:
                if i["pumpID"] == j["pumpID"]:
                    j["litres_sold"] = j["reading"] - i["reading"]
                    j["opening_reading"] = i["reading"]
        # find the litres attrbuted to th cashAcoounts
        cash_account = db.execute("SELECT IFNULL(c.pumpID,0) AS pumpID, IFNULL(c.litres,0) AS cash, IFNULL(e.litres,0) AS ecocash, IFNULL(s.litres,0) as swipe FROM cash_debit c LEFT JOIN ecocash_debit e ON c.pumpID = e.pumpID LEFT JOIN swipe_debit s ON e.pumpID = s.pumpID WHERE c.date = :cldate",cldate=cldate)
        #ecocash = db.execute("SELECT IFNULL(*,0) FROM ecocash_debits WHERE date = :cldate",cldate)
        #swipe = db.execute("SELECT IFNULL(*,0) FROM swipe_debits WHERE date = :cldate",cldate)
        #return "{}".format(cash_account) test
        dieselprice = db.execute("SELECT * FROM price_updates WHERE date =:cldate AND product = :d",cldate=cldate,d="Diesel")
        petrolprice = db.execute("SELECT * FROM price_updates WHERE date  = :cldate  AND product = :p ",cldate=cldate,p="Petrol")
        #return "{}".format(petrolprice) test
        for i in closing_stock_pump:
            for j in cash_account:
                if i["pumpID"] == j["pumpID"]:
                    i["cash"] = j["cash"]
                    i["ecocash"] = j["ecocash"]
                    i["swipe"] = j["swipe"]
        total_prdct_sales = {"Diesel":0,"Petrol":0}
        for i in closing_stock_pump:
            if i["product"] == "Diesel":
                total_prdct_sales["Diesel"] += i["litres_sold"]
            else:
                total_prdct_sales["Petrol"] +=i["litres_sold"]
        for i in closing_stock_tank:
            i["pumpsales"] = 0
        for i in closing_stock_tank:
            for j in closing_stock_pump:
                if i["pumpID"] == j["pumpID"]:
                    i["pumpsales"] += j["litres_sold"]


        return render_template("driveway.html",cldate=cldate,tanks=closing_stock_tank,pumps=closing_stock_pump,total_prdct_sales = total_prdct_sales,dieselprice =dieselprice,petrolprice=petrolprice)

    else:
        return render_template("getdriveway.html")

@app.route("/cashsales", methods = ["GET","POST"])
@login_required
def cashsales():
    """ Enter cash sales """
    # SELECT pumps to use in template
    pumps = db.execute("SELECT * from pumps")
   # method is POST
    if request.method == "POST":
        date = request.form.get("date")
        pumpID = request.form.get("pumpID")
        CashAccount = request.form.get("CashAccount")
        # return "{}".format(pumpID) test
        litres = request.form.get("litres")
        if CashAccount == "Cash":
            result = db.execute("INSERT INTO cash_debit (date,pumpID,litres) VALUES (:date,:pumpID,:litres)",date=date,pumpID=pumpID,litres=litres)
        if CashAccount == "Ecocash":
            result = db.execute("INSERT INTO ecocash_debit (date,pumpID,litres) VALUES (:date,:pumpID,:litres)",date=date,pumpID=pumpID,litres=litres)
        elif CashAccount == "Swipe":
            result = db.execute("INSERT INTO swipe_debit (date,pumpID,litres) VALUES (:date,:pumpID,:litres)",date=date,pumpID=pumpID,litres=litres)

        else:
            return redirect("/")


    else: #method is GET
        return render_template("cashsales.html",pumps=pumps)



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
        session["user_id"] = rows[0]["UserID"]

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

        # Check if passwords entered are the Same
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
        session["user_id"] = rows[0]["UserID"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
