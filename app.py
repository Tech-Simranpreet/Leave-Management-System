# COMP639 2023 S1 Project2
# PO Elizabeth Venz
# Group 8: Jessica Zhao, Patrick Yeung, Peter Liu, SimranpreeKaur. S, Xiaowei Li

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from jessica import jessica
from peter import peter
from patrick import patrick
from sim import sim
from xiaowei import xiaowei
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Flask, render_template, redirect, request, session
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

app.register_blueprint(jessica)
app.register_blueprint(peter)
app.register_blueprint(patrick)
app.register_blueprint(sim)
app.register_blueprint(xiaowei)

@app.route("/", methods=["POST", "GET"])
def home():
    if "email" in session:
        if session["roletypeid"] == 1:
            return render_template("employee/edashboard.html")
        elif session["roletypeid"] == 2:
            return render_template("manager/mdashboard.html")
        elif session["roletypeid"] == 3:
            return render_template("admin/mdashboard.html")
    else:    
        return render_template("signin.html")

if __name__ == "__main__":
    app.run()