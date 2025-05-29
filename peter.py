from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Blueprint

app = Flask(__name__)

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

peter = Blueprint('peter', __name__)


#G8P2 - peter part
#code start

@peter.route('/search_leave_requests', methods=["GET", "POST"])
def search_leave_requests():
    cur = getCursor()
    if request.method == "POST":
        search_query = request.form['search_query']
        if not search_query:
            query = """SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, lr.leave_end_date, lr.additional_info, lr.hrs_req, lr.leave_status
                       FROM leave_request lr
                       JOIN employee e ON lr.emp_id = e.emp_id
                       JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id"""
            cur.execute(query)
        else:
            query = """SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, lr.leave_end_date, lr.additional_info, lr.hrs_req, lr.leave_status
                       FROM leave_request lr
                       JOIN employee e ON lr.emp_id = e.emp_id
                       JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
                       WHERE e.emp_fname LIKE %s OR e.emp_lname LIKE %s OR lr.leave_status = %s"""
            val = ('%' + search_query + '%', '%' + search_query + '%', search_query)
            cur.execute(query, val)
        results = cur.fetchall()
        return render_template("search_leave_request.html", results=results)
    return render_template("search_leave_request.html")

@peter.route('/change_password', methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        cur = getCursor()
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        email = session.get('email')
        print(email)
        # Ensure that the user has inputted
        if (not new_password) or (not confirm_password):
            flash("Please fill all of the provided fields!")
            return render_template("changepassword.html")

        # Check to see if password confirmation were the same or not
        if new_password != confirm_password:
            flash("New password did not match")
            return render_template("changepassword.html")

        else:
            password = confirm_password

        query = "UPDATE users SET password = %s WHERE email = %s"
        values = (password, email)
        cur.execute(query, values)

        flash("Password successfully changed", "success")
        return render_template("changepassword.html")

    else:
        return render_template("changepassword.html")



#code end
