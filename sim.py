from flask import Flask, session, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Blueprint
import bcrypt
from flask import session
import bcrypt
import hashlib
from flask import flash
import numpy as np
from functions import *
import json
from flask import jsonify


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

sim = Blueprint('sim', __name__)

#G8P2 - sim part
#code start
#This will be the login, we need to use both GET and POST requests    

# @sim.route("/loginn", methods=['GET', 'POST'])
# def login():
#     #Output message if something goes wrong
#     msg=''

#  # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST':
#         if 'email' in request.form and 'password' in request.form:
# # Create variables for easy access
#             username = request.form['email']
#             user_password = request.form['password']
#             connection = getCursor()
#             connection.execute("Select * from employee where email = %s", (username,))
#              # Fetch one record and return result
#             account = connection.fetchone()
#             if account is not None:
#                 hash_password = account[2]
#                 salt = bcrypt.gensalt().decode('utf-8')  # Generate a new salt
#                 hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
#                 if bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8')):
#             # If account exists in accounts table in out database
#             # Create session data, we can access this data in other routes
#                     session['loggedin'] = True
#                     session['id'] = account[1]
#                     session['username'] = account[0]
#                     session['email'] = account[7]
#                     return redirect("/profile")
#                 else:
#                 #password incorrect
#                     msg = 'Incorrect password!'
#             else:
#             # Account doesnt exist or username incorrect
#                 msg = 'Invalid credentials'

#         else:
#             msg = 'Invalid details'      
#             flash(msg,'error')  
#     # Show the login form with message (if any)
#     return render_template('login.html', msg=msg)    


# Employee leave request route

@sim.route("/employee/apply/default", methods = ["GET", "POST"])
def leaverequest():
    print('request')

    if 'email' not in session:
        return redirect("/user")
    
    

    if request.method == "POST":
        
        email = session['email']
        print(email)
        leave_type_id = request.form['leave_type_id']
        start_date = datetime.strptime(request.form['leave_start_date'], '%d-%m-%Y').date()
        end_date = datetime.strptime(request.form['leave_end_date'], '%d-%m-%Y').date()

        #checking if the end date is earlier than start date
        if end_date < start_date:
            flash("End date cannot be earlier than start date.")
            return redirect("/employee/apply/default")

        
        #check for already applied and approved leaves
        leave_exists = check_leave_exists(email, start_date, end_date)
        if leave_exists:
            error_message = "Leave already exists!"
            flash(error_message)
            return redirect("/employee/apply/default")
        #check for overlapping leave
        overlapping_leaves = check_overlapping_leave(email, start_date, end_date)
        if overlapping_leaves:
            error_message = "Leave already exists!"
            flash(error_message)
            return redirect("/employee/apply/default")
        
        public_holidays = get_public_holidays(start_date, end_date)
        business_days = count_business_days(start_date, end_date, public_holidays = public_holidays)
        total_days = (end_date - start_date).days + 1
        hours_per_day = 7.5
        requested_hours = float(business_days * hours_per_day)
    #Include end date 
        if total_days >= 1 and np.is_busday(end_date):
            requested_hours += float(hours_per_day)    
        
        if requested_hours <= 0:
            flash("Invalid leave duration.")
            return redirect("/employee/apply/default")
        
        leave_status = 'Pending'
        additional_info = request.form['additional_info']

        #Email = session['email']
        connection= getCursor()
        query="INSERT INTO leave_request(emp_id,leave_type_id, leave_start_date, leave_end_date,hrs_req, leave_status, additional_info) VALUES ((SELECT emp_id FROM employee WHERE email = %s), %s, %s, %s, %s, %s, %s);"
        values= (email, leave_type_id,start_date,end_date,requested_hours, leave_status, additional_info,)
        connection.execute(query, values)
        return redirect("/submission?hrs_req=" + str(requested_hours))
    email = session['email']
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    connection = getCursor()
    connection.execute(""" SELECT e.emp_fname, e.email, CONCAT(a.emp_fname,' ',a.emp_lname) as approved_manager_name, a.email as approved_manager_email from employee e LEFT JOIN employee a ON e.approved_manager_name = a.emp_id WHERE e.email = %s;""",(email,)
                       )
    result = connection.fetchone()
    if result is None:
        flash(f'Could not find employee with email {email}.','danger')
        return redirect("/employee/apply/default")
    
    employee_firstname = result[0]
    employee_email = result[1]
    approved_manager = result[2]
    approved_manager_email = result[3]

    email_subject = f"Leave Request Submitted by {employee_firstname}"
    email_body = f"Dear {approved_manager}, \n\nA leave request has been submitted by {employee_firstname}.\n\nBest regards, \nLincoln University"

    send_email_approval(approved_manager_email, email_subject, email_body, start_date, end_date)
    leave_types=get_leave_types()
    return render_template("common/requestleave.html", leave_types = leave_types)
    

#Calculation hours according to weekdays excluding weekends
def count_business_days(start_date, end_date, public_holidays= None):
    business_days = np.busday_count(start_date, end_date, holidays = public_holidays)
    return business_days                    

#excluding public_holidays
def get_public_holidays(start_date, end_date):
    public_holiday = []
    connection = getCursor()
    query = "Select DISTINCT holi_date from public_holiday WHERE holi_date BETWEEN %s AND %s;"
    values = (start_date, end_date)
    connection.execute(query, values)
    rows = connection.fetchall()
    for row in rows:
        public_holiday.append(row[0])
        print("Public Holidays:", public_holiday)
    return public_holiday



#function for check leaves which already exist in database
def check_leave_exists(email, start_date, end_date):
    connection = getCursor()
    query = "Select COUNT(*) from leave_request WHERE emp_id= (Select emp_id from employee where email= %s) AND leave_start_date <=%s AND leave_end_date >=%s AND leave_status IN ('Pending', 'Approved');"
    values = (email, start_date, end_date)
    connection.execute(query, values)
    result = connection.fetchone()
    leave_count = result[0]
    return leave_count > 0

#function for checking overlapping leave
def check_overlapping_leave(email, start_date, end_date):
    connection = getCursor()
    query = "Select COUNT(*) from leave_request WHERE emp_id= (Select emp_id from employee where email= %s) AND leave_start_date <=%s AND leave_end_date >=%s AND leave_status != 'deleted';"
    values = (email, start_date, end_date)
    connection.execute(query, values)
    overlapping_leave = connection.fetchone()
    leave_count = overlapping_leave[0]
    return leave_count > 0



def send_email_approval(to, subject, body, start_date, end_date):
    your_email = 'patlorick@gmail.com'
    your_password = 'pjhtgywxrkiuhorx'
            
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "LU Leave System"
    msg['To'] = to

    if check_leave_exists(to, start_date, end_date):
        print("Leave already exists.")
        return

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(your_email, your_password)
    server.send_message(msg)
    server.quit() 

  


#leave submission route
@sim.route("/submission")
def submission():
    requested_hours = request.args.get("hrs_req")
    return render_template("common/esubmissionleave.html", requested_hours = requested_hours)    
            

#Projected leave balance for employee
@sim.route("/apply/projected", methods = ['POST'])
def calculate_projected_balance():

    date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
    today = datetime.today().date()
    print(date)
    print(today)
    
    employee_id = session['emp_id']
    leave_balances = fetch_employee_leave_balances(employee_id)
    print(leave_balances)
    
    annual_leave_hours = 30 * 7.5 
    work_hours = 7.5 * 5 * 52 
    accrual_rate = annual_leave_hours / work_hours
    
    num_work_days = np.busday_count(today, date)
    
    if leave_balances:
        annual_leave_balance = leave_balances[0]["annual_leave_bal"]
        leave_applied_not_paid = leave_balances[0]["pending_annual_leave"]
        leave_applied_not_approved = leave_balances[0]["approved_annual_leave"]
        projected_accrual_cal = num_work_days * accrual_rate
        projected_accrual = f"{round(projected_accrual_cal, 2)} ({round(projected_accrual_cal / 7.5)} days)"
        estimated_projected_balance_cal = extract_number(leave_balances[0]["annual_leave_bal"]) + projected_accrual_cal - extract_number(leave_balances[0]["pending_annual_leave"]) - extract_number(leave_balances[0]["approved_annual_leave"])
        estimated_projected_balance = f"{round(estimated_projected_balance_cal, 2)} ({round(estimated_projected_balance_cal / 7.5)} days)"
        response_data = {
            'projected-date' : date,
            'annual-leave-balance' : annual_leave_balance,
            'leave-applied-not-paid' : leave_applied_not_paid,
            'leave-applied-not-approved' : leave_applied_not_approved,
            'projected-accrual' : projected_accrual,
            'estimated-projected-balance' : estimated_projected_balance
        }

        return jsonify(response_data)
    
    else:
         error_message = "Leave Balance does not exist!"
         flash(error_message)
         return redirect("/apply/projected")
   


   
#code end
