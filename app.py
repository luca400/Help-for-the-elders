from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

import sqlalchemy

#   Set up engine
engine = create_engine(
    "postgres://kbyvjxpiuszlty:e55a897409928fd51a36d3bded23f451881fe4e9777068562dac156675a48b24@ec2-52-202-146-43.compute-1.amazonaws.com:5432/d1stlaqtjbucj")
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.secret_key = "hpskfj2848nkhuhh19ebc72b7cubdh"
logged_in = False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/order', methods=["POST", "GET"])
def order():
    # Orders something
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        city = request.form["city"]
        addres = request.form["address"]
        products = request.form["product"]

        db.execute("INSERT INTO users(firstName, lastName, city, addres, products) VALUES(:firstName, :lastName, :city, :addres,  :products)", {
                   "firstName": firstName, "lastName": lastName, "city": city, "addres": addres, "products": products})
        db.commit()
    return render_template("order.html")


@app.route('/orders', methods=["GET", "POST"])
def orders():
    global logged_in
    if logged_in:
        orders = db.execute("SELECT * FROM users;")
        if request.method == "POST":
            city = request.form["search_city"]
            orders = db.execute(
                "SELECT * FROM users WHERE city=:city ", {"city": city}).fetchall()

        return render_template("orders.html", orders=orders)
    else:
        return render_template("errors/not_loggedin.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form["deliver_firstName"]
        lastName = request.form["deliver_lastName"]
        email = request.form["deliver_email"]
        phone = request.form["deliver_phone"]
        passw = request.form["passw"]

        db.execute("INSERT INTO deliveries(firstName, lastName, email, phone, passw) VALUES(:firstName, :lastName,  :email,  :phone, :passw)", {
                   "firstName": firstName, "lastName": lastName,  "email": email, "phone": phone, "passw": passw})
        db.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    global logged_in
    if request.method == "POST" and logged_in == False:
        email = request.form["deliver_check_email"]
        passw = request.form["deliver_check_passw"]

        check_email = db.execute("SELECT email FROM deliveries WHERE email=:email", {
                                 "email": email}).fetchall()

        if check_email:

            check_passw = db.execute("SELECT passw FROM deliveries WHERE email=:email AND passw=:passw", {
                "email": email, "passw": passw}).fetchall()

            if check_passw:
                logged_in = True
                return redirect(url_for('dashboard'))

            else:
                return redirect(url_for('passw_error'))

        else:
            return redirect(url_for('email_error'))
    if logged_in:
        return redirect(url_for('dashboard'))

    return render_template("login.html")


@app.route('/email_error')
def email_error():
    return render_template("errors/email.html")


@app.route('/passw_error')
def passw_error():
    return render_template("errors/passw.html")


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    global logged_in
    if logged_in:
        return render_template("dashboard.html")
    else:
        return render_template("errors/not_loggedin.html")


@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return render_template("logout.html")
