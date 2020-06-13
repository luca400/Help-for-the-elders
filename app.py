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


@app.route('/', methods=["POST", "GET"])
def home():
    # Orders something
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        addres = request.form["address"]
        products = request.form["product"]

        db.execute("INSERT INTO users(firstName, lastName, addres, products) VALUES(:firstName, :lastName, :addres, :products)", {
                   "firstName": firstName, "lastName": lastName, "addres": addres, "products": products})
        db.commit()
    return render_template("index.html")


@app.route('/orders')
def order():
    orders = db.execute(
        "SELECT firstName, lastName, addres, products FROM users").fetchall()
    return render_template("orders.html", orders=orders)
