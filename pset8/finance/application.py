import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    # Query infos from database
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user", user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']

    total = cash
    stocks = []

    if request.method == "POST":
        if request.form.get("buy"):

            for index, row in enumerate(rows):
                stock_info = lookup(row['symbol'])

                if request.form["buy"] == stock_info['symbol']:

                    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']
                    symbol = stock_info['symbol']
                    price = lookup(symbol)['price']
                    cash_after = cash - price
                    amount = 1

                    # Check if current cash is enough for transaction
                    if cash_after < 0:
                        return apology("You don't have enough money for this transaction")

                    # Check if user already has one or more stocks from the same company
                    stock = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

                    # Insert new row into the stock table
                    if not stock:
                        db.execute("INSERT INTO stocks(user_id, symbol, amount) VALUES (:user, :symbol, :amount)", user=session["user_id"], symbol=symbol, amount=amount)

                    # update row into the stock table
                    else:
                        amount += stock[0]['amount']

                    db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol, amount=amount)

                    # update user's cash
                    db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=cash_after, user=session["user_id"])

                    # Update history table
                    db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)", user=session["user_id"], symbol=symbol, amount=amount, value=round(price * float(amount), 2))

                    flash("Bought!")
                    return redirect("/")


        else:

            for index, row in enumerate(rows):
                stock_info = lookup(row['symbol'])

                if request.form["sell"] == stock_info['symbol']:

                    # collect relevant informations
                    amount = 1
                    symbol = stock_info['symbol']
                    price = lookup(symbol)['price']
                    value=round(price*float(amount))

                    # Update stocks table
                    amount_before = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol", symbol=symbol, user=session["user_id"])[0]['amount']
                    amount_after = amount_before - amount

                    # delete stock from table if we sold every unit we had
                    if amount_after == 0:
                        db.execute("DELETE FROM stocks WHERE user_id = :user AND symbol = :symbol", symbol=symbol, user=session["user_id"])

                    # stop the transaction if the user does not have enough stocks
                    elif amount_after < 0:
                        return apology("That's more than the stocks you own")

                    # otherwise update with new value
                    else:
                        db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol", symbol=symbol, user=session["user_id"], amount=amount_after)

                    # calculate and update user's cash
                    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']
                    cash_after = cash + price * float(amount)

                    db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=cash_after, user=session["user_id"])

                    # Update history table
                    db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)", user=session["user_id"], symbol=symbol, amount=-amount, value=value)

                    flash("Sold!")
                    return redirect("/")


    else:
        # pass a list of lists to the template page, template is going to iterate it to extract the data into a table

        for index, row in enumerate(rows):
            stock_info = lookup(row['symbol'])

            # create a list with all the info about the stock and append it to a list of every stock owned by the user
            stocks.append(list((stock_info['symbol'], stock_info['name'], row['amount'], lookup(stock_info['symbol'])['price'], round(stock_info['price'] * row['amount'], 2),)))
            total += stocks[index][4]

        # get the username to access profile menu
        name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

        return render_template("index.html", stocks=stocks, cash=round(cash, 2), total=round(total, 2), name=name)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Obtain the data necessary for the transaction
        amount=int(request.form.get("amount"))
        symbol=lookup(request.form.get("symbol"))['symbol']

        # Control if the stock symbol is valid
        if not lookup(symbol):
            return apology("Could not find the stock")

        # Calculate total value of the transaction
        price=lookup(symbol)['price']
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash - price * float(amount)

        # Check if current cash is enough for transaction
        if cash_after < 0:
            return apology("You don't have enough money for this transaction")

        # Check if user already has one or more stocks from the same company
        stock = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                          user=session["user_id"], symbol=symbol)

        # Insert new row into the stock table
        if not stock:
            db.execute("INSERT INTO stocks(user_id, symbol, amount) VALUES (:user, :symbol, :amount)",
                user=session["user_id"], symbol=symbol, amount=amount)

        # update row into the stock table
        else:
            amount += stock[0]['amount']

            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                user=session["user_id"], symbol=symbol, amount=amount)

        # update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                user=session["user_id"], symbol=symbol, amount=amount, value=round(price * float(amount), 2))

        # Redirect user to index page with a success message
        flash("Bought!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # get the username to access profile menu
        name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

        return render_template("buy.html", name=name)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # query database with the transactions history
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user",
                            user=session["user_id"])

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    transactions = []
    for row in rows:
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the transaction and append it to a list of every stock transaction
        transactions.append(list((stock_info['symbol'], stock_info['name'], row['amount'], row['value'], row['date'])))

    # get the username to access profile menu
    name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

    # redirect user to index page
    return render_template("history.html", transactions=transactions, name=name)


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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Could not find the stock")

        return render_template("quote.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # get the username to access profile menu
        name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

        return render_template("quote.html", stock="", name=name)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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

        # Ensure confirm password is correct
        elif request.form.get("password") != request.form.get("confirm-password"):
            return apology("The passwords don't match", 403)

        # Query database for username if already exists
        elif db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username")):
            return apology("Username already taken", 403)

        # Insert user and hash of the password into the table
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # collect relevant informations
        amount=int(request.form.get("amount"))
        symbol=request.form.get("symbol")
        price=lookup(symbol)["price"]
        value=round(price*float(amount))

        # Update stocks table
        amount_before = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"])[0]['amount']
        amount_after = amount_before - amount

        # delete stock from table if we sold every unit we had
        if amount_after == 0:
            db.execute("DELETE FROM stocks WHERE user_id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"])

        # stop the transaction if the user does not have enough stocks
        elif amount_after < 0:
            return apology("That's more than the stocks you own")

        # otherwise update with new value
        else:
            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"], amount=amount_after)

        # calculate and update user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash + price * float(amount)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                user=session["user_id"], symbol=symbol, amount=-amount, value=value)

        # Redirect user to home page with success message
        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # query database with the transactions history
        rows = db.execute("SELECT symbol, amount FROM stocks WHERE user_id = :user", user=session["user_id"])

        # get the username to access profile menu
        name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

        # create a dictionary with the availability of the stocks
        stocks = {}
        for row in rows:
            stocks[row['symbol']] = row['amount']

        return render_template("sell.html", stocks=stocks, name=name)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    # get the username to access profile menu
    name = db.execute("SELECT username FROM users WHERE id = :user ", user=session["user_id"])[0]['username']

    return render_template("profile.html", name=name)


@app.route("/bank", methods=["GET", "POST"])
@login_required
def bank():
    
    # get the info from banks table
    rows = db.execute("SELECT * FROM banks WHERE user_id = :user", user=session["user_id"])
    
    # get the username to access profile menu
    name = db.execute("SELECT username FROM users WHERE id = :user", user=session["user_id"])[0]['username']
    
    # get cash from db
    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']
    
    banks = []
        
    if request.method == "POST":
        
        amount = request.form.get("amount")

        cash_after = int(cash) + int(amount)
        
        # update cash to db
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=cash_after, user=session["user_id"])
        
        # insert loan to banks
        db.execute("INSERT INTO banks(user_id, amount) VALUES (:user, :amount)", user=session["user_id"], amount=amount)

        flash("Borrowed!")

        return redirect("/bank")

    else:
        # get the cash from db
        cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']
        
        for index, row in enumerate(rows):
    
            # create a list with all the info about the transaction and append it to a list of every stock transaction
            banks.append(list((name, row['amount'], row['date'])))

        return render_template("bank.html", name=name, cash=round(cash, 2), banks=banks)


@app.route("/username", methods=["GET", "POST"])
@login_required
def updateUserName():
    """Edit your credentials"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Query database for username if already exists
        elif db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username")):
            return apology("Username already taken", 403)

        # Insert user into the table
        db.execute("UPDATE users SET username = :username WHERE id = :user",
            username=request.form.get("username"), user=session["user_id"])

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("username.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def updatePassword():
    """Edit your credentials"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirm password is correct
        elif request.form.get("password") != request.form.get("confirm-password"):
            return apology("The passwords don't match", 403)

        # Insert hash of the password into the table
        db.execute("UPDATE users SET hash = :hash WHERE id = :user",
            hash=generate_password_hash(request.form.get("password")), user=session["user_id"])

        # Redirect user to home page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
