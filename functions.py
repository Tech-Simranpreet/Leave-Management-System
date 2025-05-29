
from flask import jsonify
import mysql.connector
from mysql.connector import FieldType
import connect
import math
from email.message import EmailMessage
import smtplib

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# Function to get all leave types
def get_leave_types():
    cur = getCursor()
    query = "SELECT leave_type_id, type FROM leave_type"
    cur.execute(query)
    leave_types = cur.fetchall()

    return leave_types



# Function to fetch annual/sick leave balance, annual/sick leave balance not approved, annual/sick leave balance approved not paid
def fetch_employee_leave_balances(employee_id):
    cur = getCursor()
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
        lb.emp_id = %s
    GROUP BY 
        e.emp_fname, e.emp_lname, lb.sick_leave_bal, lb.annual_leave_bal;
    """

    cur.execute(sql, (employee_id,))
    leave_balance = cur.fetchall()
    leave_balances = []
    for balance in leave_balance:
        leave_balances.append({
            "emp_fname": balance[0],
            "emp_lname": balance[1],
            "annual_leave_bal": "{} hours ({:} days)".format(balance[2], math.floor(float(balance[2]) / 7.5)),
            "pending_annual_leave": "{} hours ({:} days)".format(balance[3], math.floor(float(balance[3]) / 7.5)),
            "approved_annual_leave": "{} hours ({:} days)".format(balance[4], math.floor(float(balance[4]) / 7.5)),
            "sick_leave_bal": "{} hours ({:} days)".format(balance[5], math.floor(float(balance[5]) / 7.5)),
            "pending_sick_leave": "{} hours ({:} days)".format(balance[6], math.floor(float(balance[6]) / 7.5)),
            "approved_sick_leave": "{} hours ({:} days)".format(balance[7], math.floor(float(balance[7]) / 7.5)),
        })
    return leave_balances

# Function to send an email
def send_email(to, subject, body):
    your_email = 'patlorick@gmail.com'
    your_password = 'pjhtgywxrkiuhorx'
            
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "LU Leave System"
    msg['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(your_email, your_password)
    server.send_message(msg)
    server.quit()

   

# Function to extract number from string
def extract_number(string):
    return float(string.split(' ')[0])