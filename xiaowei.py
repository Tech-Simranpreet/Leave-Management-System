from flask import Flask,flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime, timedelta, date
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Blueprint
from flask import session
from functions import *
import json
import math
from flask import jsonify
import os
import numpy as np

from flask import Flask, flash, render_template, redirect, request, session

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

xiaowei = Blueprint('xiaowei', __name__)

#G8P2 - xiaowei part

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

# the function to detect the role type and render the default dashboard page for different role after login.
@xiaowei.route("/user", methods=["POST", "GET"])
def user():
    Email = request.form.get('email')
    Pword = request.form.get('password')
    session["email"] = Email
    session["password"] = Pword
    PSWD = Pword
    Emailtup = [Email,]
    connection = getCursor()
    connection.execute("SELECT email, role_type_id FROM users where email like %s AND password like %s", (Email, PSWD))
    Queryresults = connection.fetchall()
    if len(Queryresults) == 1:

        Item = list(Queryresults[0])
        Role_type_id = Item[1]
        print(Role_type_id)

        session["roletypeid"] = Role_type_id 
        
        connection = getCursor()
        connection.execute( "SELECT emp_id FROM employee where email=%s;", (Emailtup))
        Queryresults = connection.fetchall()
        Item = list(Queryresults[0])
        Emp_id = Item[0]
        print(Emp_id)
        session["emp_id"] = Emp_id
        Emp_idtup = [Emp_id,]

        connection = getCursor()
        connection.execute( "SELECT CONCAT(emp_fname,' ',emp_lname) AS fullname FROM employee where emp_id=%s;", (Emp_idtup))
        Queryresults = connection.fetchall()
        Item = list(Queryresults[0])
        Fullname = Item[0]
        print(Fullname)
    
        session["fullname"] = Fullname

        if Role_type_id == 1:
            connection = getCursor()
            connection.execute( "SELECT * FROM leave_balance where emp_id=%s;", (Emp_id,))
            Queryresults = connection.fetchall()
            item1 = list(Queryresults[0])
            entry1 = item1[0]
            print(entry1)

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
     
        elif Role_type_id == 2:

            connection = getCursor()
            connection.execute ("""
                SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, lr.leave_end_date, lr.additional_info, lr.hrs_req, lr.leave_status, e.emp_id
                FROM leave_request lr
                JOIN employee e ON lr.emp_id = e.emp_id
                JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
                WHERE e.email=%s ;""",(Emailtup))
            result = connection.fetchall()
            print(result)

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
              
            employee_id = session["emp_id"]
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {myunapproved_requests}")  
            print(f"Approved requests: {myapproved_requests}")  
            return render_template(
                'manager/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )

        elif Role_type_id == 3:
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
                
            employee_id = session["emp_id"]  
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {pending_requests}")  
            print(f"Approved requests: {approved_requests}")  
            return render_template(
                'admin/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )
    else:
        session.pop("email", None)
        session.pop("password", None)
        flash('Invalid email or password. ','danger')
        return redirect (url_for('home'))
    
############# shared funcs ####################################   

# the function displays users profile.
@xiaowei.route("/profile")
def profile():
    if "email" in session:

        Email = session["email"]
        Emailup = [Email,]
        connection = getCursor()
        connection.execute( """SELECT 
                    e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
                    CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
                    CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                FROM employee e
                JOIN department d ON e.dept_id = d.dept_id
                LEFT JOIN employee r ON e.report_to_name = r.emp_id
                LEFT JOIN employee a ON e.approved_manager_name = a.emp_id where e.email=%s;""", (Emailup))      
        Employeedetails = connection.fetchall()

        return render_template("common/profile.html", employeedetails = Employeedetails)
    else:
        return redirect('/')

# render change password page
@xiaowei.route("/changepassword")
def changepassword():
    if "email" in session:
        return render_template("common/changepassword.html")
    else:
        return redirect('/')

# sign out button for user to sign out.
@xiaowei.route("/signout")
def signout():
    session.pop("email", None)
    session.pop("password", None)
    return redirect (url_for('home')) 

# apply button in the top nav-bar, render a default page for apply a new request, 
# there are few more other functions (tabs - sub navbar) - view your own balances and requests, project your balances. 
@xiaowei.route("/apply/default")
def apply():
    if "email" in session:
        Fullname = session["fullname"]
        leave_types = get_leave_types()
        return render_template("common/requestleave.html", fullname = Fullname, leave_types=leave_types)
    else:
        return redirect('/')


# @xiaowei.route("/apply/view")
# def view():
#     if "email" in session:
#         return render_template("common/viewrequest.html")
#     else:
#         return redirect('/')

# @xiaowei.route("/apply/projected")
# def project():
#     if "email" in session:
#         return render_template("common/projectleave.html")
#     else:
#         return redirect('/')    

# it is for the dashboard button in the top navigation bar. the function is partially come from user function.
@xiaowei.route("/dashboard/default")
def dashboard():
    if "email" in session:
        Email = session["email"]
        Emailtup = [Email,]
        connection = getCursor()
        connection.execute( "SELECT emp_id FROM employee where email=%s;", (Emailtup))
        Queryresults = connection.fetchall()
        Item = list(Queryresults[0])
        Emp_id = Item[0]
        print(Emp_id)
        session["emp_id"] = Emp_id

        if session["roletypeid"] == 1:        
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
        elif session["roletypeid"] == 2:          
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
                
            employee_id = session["emp_id"]  
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {pending_requests}")  
            print(f"Approved requests: {approved_requests}")  
            return render_template(
                'manager/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )

        elif session["roletypeid"] == 3:          
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
                
            employee_id = session["emp_id"]   
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {pending_requests}")  
            print(f"Approved requests: {approved_requests}")  
            return render_template(
                'admin/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )
            # return render_template("admin/mdashboard.html")       
        else:
            return redirect('/')
    else:
        return redirect('/')     
    
################### move from patrick.py ##############################################  
# for getting the leave balance with the specific employee id 
@xiaowei.route('/get_leave_balance/<emp_id>', methods=["GET", "POST"])
def get_leave_requests(employee_id):
    cur = getCursor()
    sql = """
        SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, lr.leave_end_date, lr.additional_info, lr.hrs_req, e.emp_id, lr.leave_status
        FROM leave_request lr
        JOIN employee e ON lr.emp_id = e.emp_id
        JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
        WHERE e.approved_manager_name = %s;
    """
    val = (employee_id,)
    cur.execute(sql, val)
    result = cur.fetchall()

    pending_requests = []
    approved_requests = []
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
            "emp_id": row[8],
            "leave_status": row[9]
        }
        if row[9] == "Pending":
            pending_requests.append(leave_request)
        elif row[9] == "Approved":
            approved_requests.append(leave_request)
        elif row[9] == "Paid":
            approved_requests.append(leave_request)        

    return pending_requests, approved_requests
    
############# manager funcs ####################################
# for manager role. the sub navbar has general button which displays the same page that user function renders. 
@xiaowei.route("/manager/dashboard/general")
def mdashboardgeneral():
    
    flash_message = session.pop('flash', None)
    if flash_message is not None:
        flash(flash_message['message'], flash_message['category'])
    
    if "email" in session:
        Email = session["email"]
        Emailtup = [Email,]
        connection = getCursor()
        connection.execute( "SELECT emp_id FROM employee where email=%s;", (Emailtup))
        Queryresults = connection.fetchall()
        Item = list(Queryresults[0])
        Emp_id = Item[0]
        print(Emp_id)
        session["emp_id"] = Emp_id

        if session["roletypeid"] == 2:          
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
                
            employee_id = session["emp_id"]  
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {pending_requests}")  
            print(f"Approved requests: {approved_requests}")  
            return render_template(
                'manager/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )
        else:
            return redirect('/')
    else:
        return redirect('/')  
# to render manager's employee tab.    
@xiaowei.route("/manager/dashboard/employee")
def mdashboardemployee():
    if "email" in session:
        if session["roletypeid"] == 2:
            return render_template("manager/mdashboardemployee.html")
        else:
            return redirect('/')
    else:
        return redirect('/')  

############# admin funcs ####################################
# for admin role. the sub navbar has general button which displays the same page that user function renders. 
@xiaowei.route("/admin/dashboard/default")
def adashboardgeneral():
    
    flash_message = session.pop('flash', None)
    if flash_message is not None:
        flash(flash_message['message'], flash_message['category'])
    
    if "email" in session:
        Email = session["email"]
        Emailtup = [Email,]
        connection = getCursor()
        connection.execute( "SELECT emp_id FROM employee where email=%s;", (Emailtup))
        Queryresults = connection.fetchall()
        Item = list(Queryresults[0])
        Emp_id = Item[0]
        print(Emp_id)
        session["emp_id"] = Emp_id

        if session["roletypeid"] == 3:  
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
                
            employee_id = session["emp_id"]
            pending_requests, approved_requests = get_leave_requests(employee_id)
            print(f"Pending requests: {pending_requests}")  
            print(f"Approved requests: {approved_requests}")  
            return render_template(
                'admin/mdashboard.html', 
                pending_requests=pending_requests,
                approved_requests=approved_requests,
                Return=[myunapproved_requests, myapproved_requests]
            )                  
        else:
            return redirect('/')
    else:
        return redirect('/')
    
#    to render admin's employee tab
@xiaowei.route("/admin/dashboard/employee")
def adashboardemployee():
    if "email" in session:
        if session["roletypeid"] == 3:
            return render_template("admin/adashboardemployee.html")
        else:
            return redirect('/')
    else:
        return redirect('/')
# search employee function for admin    
@xiaowei.route("/admin/dashboard/searchemployee", methods=["GET", "POST"])
def adashboardsearchemployee():
    if "email" in session:
        if session["roletypeid"] == 3:  
            if request.method == "POST":
                search_query = request.form['search_query']
                cur = getCursor()
                if search_query.strip() == "":
                    connection = getCursor()
                    connection.execute(" SELECT e.emp_id, u.role_type_id, lb.annual_leave_bal, lb.sick_leave_bal, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username, CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name, CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name FROM employee e JOIN department d ON e.dept_id = d.dept_id LEFT JOIN employee r ON e.report_to_name = r.emp_id LEFT JOIN employee a ON e.approved_manager_name = a.emp_id LEFT JOIN users u ON e.email = u.email LEFT JOIN leave_balance lb on lb.emp_id = e.emp_id; ")      
                    Employeedetails = connection.fetchall()  
                    return render_template("admin/adashboardsearchemployee.html", employeedetails=Employeedetails)
                else:
                    sql = """ SELECT e.emp_id, u.role_type_id, lb.annual_leave_bal, lb.sick_leave_bal, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username, CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name, CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name FROM employee e JOIN department d ON e.dept_id = d.dept_id LEFT JOIN employee r ON e.report_to_name = r.emp_id LEFT JOIN employee a ON e.approved_manager_name = a.emp_id LEFT JOIN users u ON e.email = u.email LEFT JOIN leave_balance lb on lb.emp_id = e.emp_id WHERE e.emp_fname LIKE %s OR e.emp_lname LIKE %s OR CONVERT(e.emp_id, CHAR) LIKE %s;"""
                    query = '%' + search_query + '%'
                    val = (query, query, query)
                    cur.execute(sql, val)
                    Employeedetails = cur.fetchall()  
                    return render_template("admin/adashboardsearchemployee.html", employeedetails=Employeedetails)
            return render_template("admin/adashboardemployee.html")
        else:
            return redirect('/')
    else:
        return redirect('/')
#change role type
@xiaowei.route("/admin/dashboard/changeroletype", methods=["GET", "POST"])
def adashboardchangeroletypeemployee(): 
    if "email" in session:
        if session["roletypeid"] == 3:    

            Employeeid = request.form.get('employee_id')
            Employeeidtup = [Employeeid,]
            connection = getCursor()
            connection.execute(" SELECT e.emp_id, u.role_type_id, lb.annual_leave_bal, lb.sick_leave_bal, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username, CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name, CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name FROM employee e JOIN department d ON e.dept_id = d.dept_id LEFT JOIN employee r ON e.report_to_name = r.emp_id LEFT JOIN employee a ON e.approved_manager_name = a.emp_id LEFT JOIN users u ON e.email = u.email LEFT JOIN leave_balance lb on lb.emp_id = e.emp_id WHERE e.emp_id=%s;", Employeeidtup)  
            Employee = connection.fetchall()

            return render_template("admin/adashboardchangeroletype.html", employee=Employee)
        else:
            return redirect('/')
    else:
        return redirect('/')    

# change button to update the role type change
@xiaowei.route("/admin/dashboard/changeroletype/change", methods=["GET", "POST"])
def adashboardchangeroletypeemployeechange(): 
    if "email" in session:
        if session["roletypeid"] == 3:    

            Newtype = request.form.get('newtype')
            Employeeemail = request.form.get('employeeemail')
            Employeeid = request.form.get('employeeid')
            Employeeidtup = [Employeeid,]

            connection = getCursor()
            connection.execute("UPDATE users SET role_type_id =%s WHERE email=%s;", (Newtype, Employeeemail))  

            connection = getCursor()
            connection.execute(" SELECT e.emp_id, u.role_type_id, lb.annual_leave_bal, lb.sick_leave_bal, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username, CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name, CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name FROM employee e JOIN department d ON e.dept_id = d.dept_id LEFT JOIN employee r ON e.report_to_name = r.emp_id LEFT JOIN employee a ON e.approved_manager_name = a.emp_id LEFT JOIN users u ON e.email = u.email LEFT JOIN leave_balance lb on lb.emp_id = e.emp_id WHERE e.emp_id=%s;", Employeeidtup)  
            Employee = connection.fetchall()

            return render_template("admin/adashboardchangeroletyperesult.html", employee=Employee)
        else:
            return redirect('/')
    else:
        return redirect('/')   
# Display Leave Exception Report
@xiaowei.route("/admin/dashboard/report1")
def adashboardreport1():
    if "email" in session:
        if session["roletypeid"] == 3:
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
            return render_template("admin/mleaveexceptionreport.html", employees=employees)
        else:
            return redirect('/')
    else:
        return redirect('/')  
#Display Annual Leave Liability Report
@xiaowei.route("/admin/dashboard/report2")
def adashboardreport2():
    if "email" in session:
        if session["roletypeid"] == 3:
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
            return render_template("admin/mannualleaveliabilityreport.html", employees=employees)
        else:
            return redirect('/')
    else:
        return redirect('/')  
# render leave type page which includes a list of all the existing leave types    
@xiaowei.route("/admin/dashboard/leavetype")
def adashboardleavetype():
    if "email" in session:
        if session["roletypeid"] == 3:    

            cur = getCursor()
            cur.execute(" SELECT * FROM leave_type;")
            Leavetypelist = cur.fetchall()
            print(Leavetypelist)
            return render_template("admin/adashboardleavetype.html", leavetypelist = Leavetypelist)
        else:
            return redirect('/')
    else:
        return redirect('/')
#add new leave type page    
@xiaowei.route("/admin/dashboard/addleavetype")
def adashboardaddleavetype():
    if "email" in session:
        if session["roletypeid"] == 3:    
            return render_template("admin/adashboardaddleavetype.html")
        else:
            return redirect('/')
    else:
        return redirect('/')
#add button    
@xiaowei.route("/admin/dashboard/addleavetype/add", methods=["GET", "POST"])
def adashboardaddleavetypeadd():
    if "email" in session:
        if session["roletypeid"] == 3:    

            Type = request.form.get('type')
            Description = request.form.get('description')
            Status = request.form.get('status')

            connection = getCursor()
            connection.execute("SELECT type FROM leave_type;")
            results = connection.fetchall()
            leave_types=[]
            for result in results:
                leave_types.append(result[0])
            print(leave_types)

            if Type in leave_types:
                flash('The new type already exists, please use a new type name. ','danger')
                return redirect ("/admin/dashboard/addleavetype") 
            else:   
                connection = getCursor()
                connection.execute("INSERT INTO leave_type (type, status, leave_desc) VALUES(%s, %s, %s);", (Type, Status, Description))
                return redirect("/admin/dashboard/leavetype")
        else:
            return redirect('/')
    else:
        return redirect('/')
# edit leave type page    
@xiaowei.route("/admin/dashboard/editleavetype", methods=["GET", "POST"])
def adashboardeditleavetype():
    if "email" in session:
        if session["roletypeid"] == 3:
            if (request.form.get('type')):
                Type = request.form.get('type')
                Description = request.form.get('description')
                Status = request.form.get('status')
                Leavetypeid = request.form.get('leavetypeid')
                session["leavetype"] = Type
                session["leavetypedescription"] = Description
                session["leavetypestatus"] = Status
                session["leavetypeid"] = Leavetypeid
            else:
                Type = session["leavetype"]
                Description = session["leavetypedescription"]
                Status = session["leavetypestatus"]
                Leavetypeid = session["leavetypeid"]

            return render_template("admin/adashboardeditleavetype.html", type=Type, description=Description, status=Status, leavetypeid=Leavetypeid)
        else:
            return redirect('/')
    else:
        return redirect('/')
#update button    
@xiaowei.route("/admin/dashboard/editleavetype/edit", methods=["GET", "POST"])
def adashboardeditleavetypeedit():
    if "email" in session:
        if session["roletypeid"] == 3:    

            Type = request.form.get('type')
            Description = request.form.get('description')
            Status = request.form.get('status')
            Leavetypeid = request.form.get('leavetypeid')
            
            connection = getCursor()
            connection.execute("SELECT type FROM leave_type;")
            results = connection.fetchall()
            leave_types=[]
            for result in results:
                leave_types.append(result[0])
            print(leave_types)

            if Type == session["leavetype"]:
                connection = getCursor()
                connection.execute("UPDATE leave_type SET type=%s, leave_desc=%s, status=%s WHERE leave_type_id=%s;", (Type, Description, Status, Leavetypeid))                
            elif Type in leave_types:
                flash('The new type already exists, please use a new type name. ','danger')
                return redirect ("/admin/dashboard/editleavetype") 
            else:    
                connection = getCursor()
                connection.execute("UPDATE leave_type SET type=%s, leave_desc=%s, status=%s WHERE leave_type_id=%s;", (Type, Description, Status, Leavetypeid))                
            return redirect("/admin/dashboard/leavetype")
        else:
            return redirect('/')
    else:
        return redirect('/')
#display all the existing holidays    
@xiaowei.route("/admin/dashboard/holiday")
def adashboardholiday():
    if "email" in session:
        if session["roletypeid"] == 3:    

            cur = getCursor()
            cur.execute(" SELECT * FROM public_holiday;")
            Holidaylist = cur.fetchall()

            return render_template("admin/adashboardholiday.html", holidaylist = Holidaylist)
        else:
            return redirect('/')
    else:
        return redirect('/')
#add new holiday    
@xiaowei.route("/admin/dashboard/addholiday")
def adashboardaddholiday():
    if "email" in session:
        if session["roletypeid"] == 3:    
            return render_template("admin/adashboardaddholiday.html")
        else:
            return redirect('/')
    else:
        return redirect('/')
#add button    
@xiaowei.route("/admin/dashboard/addholiday/add", methods=["GET", "POST"])
def adashboardaddholidayadd():
    if "email" in session:
        if session["roletypeid"] == 3:    

            Date = request.form.get('date')
            Name = request.form.get('name')
            Roletype = request.form.get('roletype')
            connection = getCursor()
            connection.execute("INSERT INTO public_holiday (holi_date, holi_name, emp_id) VALUES(%s, %s, %s);", (Date, Name, Roletype))
            return redirect("/admin/dashboard/holiday")
        else:
            return redirect('/')
    else:
        return redirect('/')
#edit holiday page    
@xiaowei.route("/admin/dashboard/editholiday", methods=["GET", "POST"])
def adashboardeditholiday():
    if "email" in session:
        if session["roletypeid"] == 3:

            Date = request.form.get('date')
            Name = request.form.get('name')
            Roletype = request.form.get('roletype')
            Holidayid = request.form.get('holidayid')

            return render_template("admin/adashboardeditholiday.html", date=Date, name=Name, roletype=Roletype, holidayid=Holidayid)
        else:
            return redirect('/')
    else:
        return redirect('/')
#update button    
@xiaowei.route("/admin/dashboard/editholiday/edit", methods=["GET", "POST"])
def adashboardeditholidayedit():
    if "email" in session:
        if session["roletypeid"] == 3:    

            Date = request.form.get('date')
            Name = request.form.get('name')
            Roletype = request.form.get('roletype')
            Holidayid = request.form.get('holidayid')
            connection = getCursor()
            connection.execute("UPDATE public_holiday SET holi_date=%s, holi_name=%s, emp_id=%s WHERE pub_holi_id=%s;", (Date, Name, Roletype, Holidayid))
            return redirect("/admin/dashboard/holiday")
        else:
            return redirect('/')
    else:
        return redirect('/')
#delete holiday button    
@xiaowei.route("/admin/dashboard/deleteholiday/delete", methods=["GET", "POST"])
def adashboarddeleteholidaydelete():
    if "email" in session:
        if session["roletypeid"] == 3:    

            Holidayid = request.form.get('holidayid')
            Holidayidtup = [Holidayid,]
            connection = getCursor()
            connection.execute("DELETE FROM public_holiday WHERE pub_holi_id=%s;", (Holidayidtup))
            return redirect("/admin/dashboard/holiday")
        else:
            return redirect('/')
    else:
        return redirect('/')
#update all staff leave balance page    
@xiaowei.route("/admin/dashboard/balanceupdate")
def adashboardbalanceupdate():
    if "email" in session:
        if session["roletypeid"] == 3:   
            connection = getCursor()
            connection.execute("select distinct(updated_date) FROM leave_balance")
            queryresult = connection.fetchall()
            item = list(queryresult[0])
            lastpaydate = item[0]
            nextpaydate = lastpaydate + timedelta(days=13)
            todaydate = date.today()
            
            session["nextpaydate"] = nextpaydate

            print(lastpaydate, nextpaydate, todaydate)

            return render_template("admin/adashboardbalanceupdate.html", lastpaydate=lastpaydate, nextpaydate=nextpaydate, todaydate=todaydate)
        else:
            return redirect('/')
    else:
        return redirect('/')
#update button    
@xiaowei.route("/admin/dashboard/balanceupdate/update")
def adashboardbalanceupdate2():
    if "email" in session:
        if session["roletypeid"] == 3: 
            todaydate = date.today()
            # date1 = date(2023, 6, 23)

            connection = getCursor()
            connection.execute("select distinct(updated_date) FROM leave_balance")
            queryresult = connection.fetchall()
            item = list(queryresult[0])
            lastpaydate = item[0]
            nextpaydate = lastpaydate + timedelta(days=13)
            print(nextpaydate)

            if (nextpaydate == todaydate):      
                connection = getCursor()
                connection.execute("UPDATE leave_balance SET annual_leave_bal = annual_leave_bal + 5.77;")

                connection = getCursor()
                connection.execute("UPDATE employee e JOIN leave_balance l USING(emp_id) SET l.sick_leave_bal = 37.5 WHERE DATEDIFF(CURDATE(), start_date) >= 365 AND MOD(DATEDIFF(CURDATE(), start_date), 365)>=0 AND MOD(DATEDIFF(CURDATE(), start_date), 365)<=13;")

                connection = getCursor()
                connection.execute("""UPDATE leave_balance lb join leave_request lr using(emp_id) SET lb.annual_leave_bal = lb.annual_leave_bal - lr.hrs_req, lr.leave_status = "Paid" where leave_status = "Approved" AND leave_end_date <=curdate() AND (lr.leave_type_id = 1 OR lr.leave_type_id = 2 OR lr.leave_type_id = 3 OR lr.leave_type_id = 7);""")

                connection = getCursor()
                connection.execute("""UPDATE leave_balance lb join leave_request lr using(emp_id) SET lb.sick_leave_bal = lb.sick_leave_bal - lr.hrs_req, lr.leave_status = "Paid" where leave_status = "Approved" AND leave_end_date <=curdate() AND (lr.leave_type_id = 4 OR lr.leave_type_id = 5);""")

                connection = getCursor()
                connection.execute("""update leave_balance set updated_date = CURDATE();""")

                connection = getCursor()
                connection.execute("""Update leave_action join leave_request using(leave_req_id) set action_taken = 'paid', action_date = curdate() where leave_status = 'Paid';""")                

                flash('All the balances have been updated. ','success')
                return redirect ("/admin/dashboard/balanceupdate")    
            else: 
                flash("You can not update the balance today, please check 'The next payroll date' and update the balance on that date.",'danger')
                return redirect ("/admin/dashboard/balanceupdate")
        else:
            return redirect('/')
    else:
        return redirect('/')
#edit request page for all roles
@xiaowei.route("/editrequest", methods=["GET", "POST"])
def editrequest():
    if "email" in session:
        if session["roletypeid"] == 1 or session["roletypeid"] == 2 or session["roletypeid"] == 3: 

            leave_request_id = request.form.get('leave_request_id')
            emp_fname = request.form.get('emp_fname')
            emp_lname = request.form.get('emp_lname')
            leave_type = request.form.get('leave_type')
            leave_start_date = request.form.get('leave_start_date')
            leave_end_date = request.form.get('leave_end_date')
            additional_info = request.form.get('additional_info')
            hrs_req = request.form.get('hrs_req')
            print(leave_request_id)
            leave_types = get_leave_types()
            print(leave_type)
            if session["roletypeid"] == 3:
                return render_template("admin/editrequest.html", leave_request_id=leave_request_id,emp_fname=emp_fname,emp_lname=emp_lname,leave_type=leave_type,leave_start_date=leave_start_date,leave_end_date=leave_end_date,additional_info=additional_info,hrs_req=hrs_req, leave_types=leave_types)
            elif session["roletypeid"] == 2:
                return render_template("manager/editrequest.html", leave_request_id=leave_request_id,emp_fname=emp_fname,emp_lname=emp_lname,leave_type=leave_type,leave_start_date=leave_start_date,leave_end_date=leave_end_date,additional_info=additional_info,hrs_req=hrs_req, leave_types=leave_types)
            elif session["roletypeid"] == 1:
                return render_template("employee/editrequest.html", leave_request_id=leave_request_id,emp_fname=emp_fname,emp_lname=emp_lname,leave_type=leave_type,leave_start_date=leave_start_date,leave_end_date=leave_end_date,additional_info=additional_info,hrs_req=hrs_req, leave_types=leave_types)
    else:
        return redirect('/')   
#edit request button for all roles    
@xiaowei.route("/editrequestupdate", methods=["GET", "POST"])
def editrequestupdate():
    if "email" in session:
        if session["roletypeid"] == 1 or session["roletypeid"] == 2 or session["roletypeid"] == 3: 

            leave_request_id = request.form.get('leave_request_id')
            leave_type = request.form.get('leave_type')
            print(leave_type)
            leave_start_date = request.form.get('leave_start_date')
            leave_end_date = request.form.get('leave_end_date')
            additional_info = request.form.get('additional_info')

            print(leave_type)

            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(leave_start_date, date_format).date()
            end_date = datetime.strptime(leave_end_date, date_format).date()
            daydiff = end_date-start_date   
            days = daydiff.days + 1
            hrs_req = days*7.5
            print(leave_type, leave_start_date, leave_end_date, additional_info, hrs_req, leave_request_id)

            connection = getCursor()
            connection.execute("UPDATE leave_request SET leave_type_id = %s, leave_start_date = %s, leave_end_date = %s, additional_info = %s, hrs_req = %s, leave_status = 'Pending' where leave_req_id = %s;", (leave_type, leave_start_date, leave_end_date, additional_info, hrs_req, leave_request_id))

            if session["roletypeid"] == 3:
                return redirect ("/admin/dashboard/default")
            elif session["roletypeid"] == 2:
                return redirect ("/manager/dashboard/general")
            elif session["roletypeid"] == 1:
                return redirect (url_for('jessica.edashboardgeneral'))            
        else:
            return redirect('/')
    else:
        return redirect('/')

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#the project balance page under admin's employee tab
@xiaowei.route("/admin/employee/projected", methods=["POST"])
def mviewemployeeproject():
    emp_id = request.form.get('employee_id')
    leave_balances = fetch_employee_leave_balances(emp_id)
    return render_template("admin/mviewemployeeproject.html", emp_id=emp_id, leave_balances=leave_balances)
# get holidays
@xiaowei.route('/get_holidays')
def get_holidays():

    cur = getCursor()
    query = "SELECT holi_date FROM public_holiday"
    cur.execute(query)

    dates = [datetime.strftime(date, '%Y-%m-%d') for (date,) in cur]

    cur.close()

    return jsonify(dates)
#project action button function
@xiaowei.route("/admin/employee/projected/<emp_id>", methods=["POST"])
def calculate_projected_balance(emp_id):

    date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
    today = datetime.today().date()
    print(date)
    print(today)

    leave_balances = fetch_employee_leave_balances(emp_id)
    print(leave_balances)
    
    annual_leave_hours = 30 * 7.5 
    work_hours = 7.5 * 5 * 52 
    accrual_rate = annual_leave_hours / work_hours
    
    num_work_days = np.busday_count(today, date)
    
    annual_leave_balance = leave_balances[0]["annual_leave_bal"]
    leave_applied_not_paid = leave_balances[0]["pending_annual_leave"]
    leave_applied_not_approved = leave_balances[0]["approved_annual_leave"]
    projected_accrual_cal = num_work_days * accrual_rate
    projected_accrual = f"{round(projected_accrual_cal, 2)} ({round(projected_accrual_cal / 7.5)} days)"
    estimated_projected_balance_cal = extract_number(leave_balances[0]["annual_leave_bal"]) + projected_accrual_cal - extract_number(leave_balances[0]["pending_annual_leave"]) - extract_number(leave_balances[0]["approved_annual_leave"])
    estimated_projected_balance = f"{round(estimated_projected_balance_cal, 2)} ({round(estimated_projected_balance_cal / 7.5)} days)"

    return jsonify({
        'date': date,
        'annual_leave_balance': annual_leave_balance,
        'leave_applied_not_paid': leave_applied_not_paid,
        'leave_applied_not_approved': leave_applied_not_approved,
        'projected_accrual': projected_accrual,
        'estimated_projected_balance': estimated_projected_balance
    })
# admin's employee tab
@xiaowei.route('/admin/employee', methods=["GET", "POST"])
def mviewemployee():
    
    flash_message = session.pop('flash', None)
    if flash_message is not None:
        flash(flash_message['message'], flash_message['category'])
    
    emp_id = session["emp_id"]
    print("Emp_id from session:", emp_id)
     
    cur = getCursor()
    
    if request.method == "POST":
        if 'search_query' in request.form:
            search_query = request.form['search_query']
        
            if search_query.strip() == "":
                sql = """SELECT 
                        e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
                        CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
                        CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                    FROM employee e
                    JOIN department d ON e.dept_id = d.dept_id
                    LEFT JOIN employee r ON e.report_to_name = r.emp_id
                    LEFT JOIN employee a ON e.approved_manager_name = a.emp_id;"""
                print("Executing SQL query:", sql)

                cur.execute(sql)
                employees = cur.fetchall()

                session['search_results'] = employees
                
                return render_template("admin/adashboardemployee.html", employees=employees)
            else:
                sql = """SELECT 
                        e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
                        CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
                        CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                    FROM employee e
                    JOIN department d ON e.dept_id = d.dept_id
                    LEFT JOIN employee r ON e.report_to_name = r.emp_id
                    LEFT JOIN employee a ON e.approved_manager_name = a.emp_id
                    WHERE e.emp_fname LIKE %s OR e.emp_lname LIKE %s OR CONVERT(e.emp_id, CHAR) LIKE %s;"""
                query = '%' + search_query + '%'
                val = (query, query, query)
                print("Executing SQL query:", sql)
                cur.execute(sql, val)
                employees = cur.fetchall()
                
                session['search_results'] = employees
                
                return render_template("admin/adashboardemployee.html", employees=employees)
        else:
            employees = session.get('search_results', None)
            return render_template("admin/adashboardemployee.html", employees=employees)

    employees = session.get('search_results', None)
    return render_template("admin/adashboardemployee.html")
#amdin view employee's leave requests under employee tab
@xiaowei.route("/admin/employee/viewrequests", methods=["POST"])
def mviewrequest():
    
    flash_message = session.pop('flash', None)
    if flash_message is not None:
        flash(flash_message['message'], flash_message['category'])
    print(flash_message)
    Employeeid = request.form.get('employee_id')
    Employeeidtup = (Employeeid,)
    cur = getCursor()
    sql = """
        SELECT e.emp_fname, e.emp_lname
        FROM employee e
        WHERE e.emp_id = %s;
    """
    cur.execute(sql, Employeeidtup)
    employee = cur.fetchone()
    emp_fname = employee[0]
    emp_lname = employee[1]
    
    sql = """
        SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, 
            lr.leave_end_date, lr.additional_info, lr.hrs_req, e.emp_id, lr.leave_status, la.action_taken
        FROM leave_request lr
        JOIN employee e ON lr.emp_id = e.emp_id
        JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
        LEFT JOIN leave_action la ON lr.leave_req_id = la.leave_req_id
        WHERE e.emp_id = %s;
    """

    cur.execute(sql, Employeeidtup)
    result = cur.fetchall()
    print(result)
    pending_requests = []
    approved_requests = []
    rejected_requests = []
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
            "emp_id": row[8],
            "action_taken": row[10] 
        }
        if row[9] == "Pending":
            pending_requests.append(leave_request)
        elif row[9] == "Approved" or row[9] == "Paid":
            approved_requests.append(leave_request)
        elif row [9] == "Rejected":
            rejected_requests.append(leave_request)

    return render_template("admin/mdashboardeemployeerequests.html", 
                            pending_requests=pending_requests, 
                            approved_requests=approved_requests, 
                            rejected_requests=rejected_requests, 
                            emp_fname=emp_fname, 
                            emp_lname=emp_lname)
# admin view employee balance page     
@xiaowei.route("/admin/employee/viewbalance", methods=["GET", "POST"])
def mviewbalance(): 
    Employeeid = request.form.get('employee_id')
    leave_balances = fetch_employee_leave_balances(Employeeid)
    return render_template("admin/mdashboardviewbalance.html", leave_balances=leave_balances)
#update leave requests
@xiaowei.route('/update_leave_request/<request_id>/<action>/<emp_id>', methods=['POST'])
def update_leave_request(request_id, action, emp_id):
    cur = getCursor()
    if action == 'approve':
        status = 'Approved'
    elif action == 'reject':
        status = 'Rejected'
    elif action == 'delete':
        status = 'Deleted'
    print(status)
    sql = """
        UPDATE leave_request
        SET leave_status = %s
        WHERE leave_req_id = %s;
    """
    cur.execute(sql, (status, request_id,))
    reason = request.form.get('reason')
    
    cur.execute("""
        SELECT u.role_type_id, e.approved_manager_name 
        FROM employee e 
        JOIN users u ON e.email = u.email 
        WHERE e.emp_id = %s
    """, (emp_id,))
    result = cur.fetchone()
    if result is None:
        flash(f'Could not find employee with id {emp_id}.', 'danger')
        return redirect(url_for('xiaowei.mviewemployee'))
    
    role_type_id, approved_manager_emp_id = result
    sql = """
        INSERT INTO leave_action 
        (leave_req_id, action_taken, action_date, role_type_id, reason, approved_manager_emp_id) 
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    action_date = datetime.now().date()
    values = (request_id, action, action_date, role_type_id, reason, approved_manager_emp_id)
    print(values)
    cur.execute(sql, values)

    try:
        
        session['flash'] = {
        'message': f'Leave request {status.lower()} successfully.',
        'category': 'success'
    }
        
        sql = """SELECT 
                    e.emp_fname, e.email, CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                    FROM employee e
                    LEFT JOIN employee a ON e.approved_manager_name = a.emp_id
                    WHERE e.emp_id = %s;"""
        cur.execute(sql, (emp_id,))
        result = cur.fetchall()
        print(result)
        employee_firstname = result[0][0]
        employee_email = result[0][1]
        approved_manager = result[0][2]
        email_subject = f"""Your leave has been {status.lower()}."""
        email_body = f"""Dear {employee_firstname}\n
Your leave has been {status.lower()}"""
        
        if status != 'Approved':
            email_body += f""" for the following reason:\n
{reason}.\n 
Please discuss with your manager for more details."""
            
        email_body += f"""
Best regards,
{approved_manager} 
Lincoln University
"""
        send_email(employee_email, email_subject, email_body)    
        

    except Exception as e:
        session['flash'] = {
        'message': 'There is an error with your leave request.',
        'category': 'danger'
    }
    return redirect(url_for('xiaowei.mviewemployee'))

# search box on the top of general page 
@xiaowei.route('/admin/search_leave_requests', methods=["GET", "POST"])
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
        if session["roletypeid"] == 3:
            return render_template("admin/search_leave_request.html", results=results)
        if session["roletypeid"] == 2:
            return render_template("manager/search_leave_request.html", results=results)
            
    return render_template("admin/search_leave_request.html")

#view your balances under apply page.
@xiaowei.route("/employee/viewbalance", methods=["GET", "POST"])
def applyviewbalance(): 
    Employeeid = session["emp_id"]
    leave_balances = fetch_employee_leave_balances(Employeeid)
    return render_template("common/applyviewbalance.html", leave_balances=leave_balances)
#project your balances under apply page.
@xiaowei.route("/employee/projected", methods=["GET", "POST"])
def applyviewproject():
    Employeeid = session["emp_id"]
    leave_balances = fetch_employee_leave_balances(Employeeid)
    return render_template("common/applyviewproject.html", emp_id=Employeeid, leave_balances=leave_balances)
# view your requests under apply page.
@xiaowei.route("/employee/viewrequests", methods=["GET", "POST"])
def applyviewrequest():
    Employeeid = session["emp_id"]
    Employeeidtup = (Employeeid,)
    cur = getCursor()
    sql = """
        SELECT e.emp_fname, e.emp_lname
        FROM employee e
        WHERE e.emp_id = %s;
    """
    cur.execute(sql, Employeeidtup)
    employee = cur.fetchone()
    emp_fname = employee[0]
    emp_lname = employee[1]
    
    sql = """
        SELECT lr.leave_req_id, e.emp_fname, e.emp_lname, lt.type, lr.leave_start_date, 
            lr.leave_end_date, lr.additional_info, lr.hrs_req, e.emp_id, lr.leave_status, la.action_taken
        FROM leave_request lr
        JOIN employee e ON lr.emp_id = e.emp_id
        JOIN leave_type lt ON lr.leave_type_id = lt.leave_type_id
        LEFT JOIN leave_action la ON lr.leave_req_id = la.leave_req_id
        WHERE e.emp_id = %s;
    """

    cur.execute(sql, Employeeidtup)
    result = cur.fetchall()
    print(result)
    pending_requests = []
    approved_requests = []
    rejected_requests = []
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
            "emp_id": row[8],
            "action_taken": row[10] 
        }
        if row[9] == "Pending":
            pending_requests.append(leave_request)
        elif row[9] == "Approved" or row[9] == "Paid":
            approved_requests.append(leave_request)
        elif row [9] == "Rejected":
            rejected_requests.append(leave_request)

    return render_template("common/applyviewrequests.html", 
                            pending_requests=pending_requests, 
                            approved_requests=approved_requests, 
                            rejected_requests=rejected_requests, 
                            emp_fname=emp_fname, 
                            emp_lname=emp_lname)