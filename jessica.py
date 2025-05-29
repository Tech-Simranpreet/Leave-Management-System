import json
import math
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Blueprint
import os
from dateutil.relativedelta import relativedelta

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

jessica = Blueprint('jessica', __name__)

#G8P2 - jessica part
#code start
# XL modified the User Story - employee view details, the commented code down below now is redundant.
# @jessica.route('/employee/details', methods=["GET", "POST"])
# def edetails():
#         Email = session["email"]
#         Emailup = [Email,]
#         connection = getCursor()
#         connection.execute( """SELECT 
#                     e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
#                     CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
#                     CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
#                 FROM employee e
#                 JOIN department d ON e.dept_id = d.dept_id
#                 LEFT JOIN employee r ON e.report_to_name = r.emp_id
#                 LEFT JOIN employee a ON e.approved_manager_name = a.emp_id where e.email=%s;""", (Emailup))      
#         employees = connection.fetchall()
#         return render_template("employee/edetails.html", employees=employees)

@jessica.route('/employee/dashboard/default', methods=["GET", "POST"])
def edashboardgeneral():
    Email = session["email"]
    Emailtup = [Email,]
    connection = getCursor()
    connection.execute ("""
        SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, lr.leave_end_date, lr.additional_info, lr.hrs_req, lr.leave_status, e.emp_id
        FROM leave_request lr
        JOIN employee e ON lr.emp_id = e.emp_id
        JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
        WHERE e.email=%s ;""",(Emailtup))
    result = connection.fetchall()

    myunapproved_requests = []
    myapproved_requests = []
    for row in result:
        leave_request = {
            "leave_request_id": row[0],
            "emp_fname": row[1],
            "emp_lname": row[2],
            "leave_type": row[3],
            "leave_start_date": row[4].strftime("%Y-%m-%d"),
            "leave_end_date": row[5].strftime("%Y-%m-%d"),
            "additional_info": row[6],
            "hrs_req": "{} ({:} days)".format(row[7], math.floor(float(row[7]) / 7.5)),
            "leave_status": row[8],
            "emp_id": row[9]           
        }
        if row[8] == "Pending":
            myunapproved_requests.append(leave_request)
        elif row[8] == "Rejected":
            myunapproved_requests.append(leave_request)
        elif row[8] == "Approved":
            myapproved_requests.append(leave_request)
        elif row[8] == "Paid":
            myapproved_requests.append(leave_request)               

    return render_template("employee/edashboard.html", Return=[myunapproved_requests, myapproved_requests])
       
@jessica.route('/employee/eleavebalance', methods=["GET", "POST"])
def eviewbalance(): 
    Email = session["email"]
    Emailtup = [Email,]
    connection = getCursor()
    sql = """
    SELECT 
        e.emp_fname, 
        e.emp_lname, 
        lb.annual_leave_bal, 
        COALESCE(SUM(CASE WHEN lr.leave_type_id = 1 AND lr.leave_status = 'Pending' THEN lr.hrs_req ELSE 0 END), 0) AS pending_annual_leave,
        COALESCE(SUM(CASE WHEN lr.leave_type_id = 1 AND lr.leave_status = 'Approved' AND la.action_taken = 'approve' THEN lr.hrs_req ELSE 0 END), 0) AS approved_annual_leave,
        lb.sick_leave_bal, 
        COALESCE(SUM(CASE WHEN lr.leave_type_id = 5 AND lr.leave_status = 'Pending' THEN lr.hrs_req ELSE 0 END), 0) AS pending_sick_leave,       
        COALESCE(SUM(CASE WHEN lr.leave_type_id = 5 AND lr.leave_status = 'Approved' AND la.action_taken = 'approve' THEN lr.hrs_req ELSE 0 END), 0) AS approved_sick_leave
    FROM 
        leave_balance lb
        JOIN employee e ON lb.emp_id = e.emp_id
        LEFT JOIN leave_request lr ON lr.emp_id = e.emp_id
        LEFT JOIN leave_action la ON la.leave_req_id = lr.leave_req_id
    WHERE 
        e.email = %s
    GROUP BY 
        e.emp_fname, e.emp_lname, lb.sick_leave_bal, lb.annual_leave_bal;
    """

    connection.execute(sql, Emailtup)
    leave_balance = connection.fetchall()
    leave_balances = []
    for balance in leave_balance:
        leave_balances.append({
            "emp_fname": balance[0],
            "emp_lname": balance[1],
            "annual_leave_bal": "{} ({:} days)".format(balance[2], math.floor(float(balance[2]) / 7.5)),
            "pending_annual_leave": "{} ({:} days)".format(balance[3], math.floor(float(balance[3]) / 7.5)),
            "approved_annual_leave": "{} ({:} days)".format(balance[4], math.floor(float(balance[4]) / 7.5)),
            "sick_leave_bal": "{} ({:} days)".format(balance[5], math.floor(float(balance[5]) / 7.5)),
            "pending_sick_leave": "{} ({:} days)".format(balance[6], math.floor(float(balance[6]) / 7.5)),
            "approved_sick_leave": "{} ({:} days)".format(balance[7], math.floor(float(balance[7]) / 7.5)),
        })
        
    return render_template("employee/eleavebalance.html", leave_balances=leave_balances)
            
@jessica.route('/leaveexceptionreport', methods=["GET", "POST"])
def mler():
        Email = session["email"]
        Emailtup = [Email,]
        connection = getCursor()
        connection.execute( """SELECT 
                    e.emp_id, e.emp_fname, e.emp_lname, e.position_title, d.dept_name,lb.annual_leave_bal bal,floor(lb.annual_leave_bal/7.5),CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                FROM employee e
                JOIN department d ON e.dept_id = d.dept_id
                LEFT JOIN employee a ON e.approved_manager_name = a.emp_id and a.email=%s
                LEFT JOIN leave_balance lb ON lb.emp_id =e.emp_id
                where lb.annual_leave_bal >=225 Order by lb.annual_leave_bal DESC;""", (Emailtup))      
        employees = connection.fetchall()
        return render_template("manager/mleaveexceptionreport.html", employees=employees)

@jessica.route('/annualleaveliabilityreport', methods=["GET", "POST"])
def malr():
        Email = session["email"]
        Emailtup = [Email,]
        print(Email)
        connection = getCursor()
        connection.execute( """SELECT 
                    e.emp_id, e.emp_fname, e.emp_lname, e.position_title, d.dept_name,lb.annual_leave_bal bal,floor(lb.annual_leave_bal/7.5),CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                FROM employee e
                JOIN department d ON e.dept_id = d.dept_id
                LEFT JOIN employee a ON e.approved_manager_name = a.emp_id 
                LEFT JOIN leave_balance lb ON lb.emp_id =e.emp_id
                where a.email=%s ORDER BY e.emp_fname, e.emp_lname;""", (Emailtup))      
        employees = connection.fetchall()
        return render_template("manager/mannualleaveliabilityreport.html", employees=employees)

