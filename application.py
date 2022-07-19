from operator import le
from flask import Flask, request, redirect, url_for, render_template, session
import pymongo
import os
import json
from auth import auth
from bson.json_util import dumps

client = pymongo.MongoClient("mongodb+srv://serban:serban@cluster0.oi6hu.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('medic')
records = db.patients

app = Flask(__name__)
app.secret_key = "super secret key"
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=2)
app.register_blueprint(auth)

@app.route("/")
def index():
    if "email" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("auth.login"))

@app.route("/patients")
def patients():
    if "email" in session:
        return render_template("patients.html")
    else:
        return redirect(url_for("auth.login"))

@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.get_json(force=True)
    #needs check for duplicates
    data["medic"] = session["email"]
    records.insert_one(data)
    return "asdasd"

@app.route("/get_patient", methods=["GET"])
def get_patient():
    print(list(records.find({},{ "medic": session["email"] })))
    
    data = dumps(list(records.find({ "medic": session["email"] })))
    return data


