
import json
import math
from flask import Flask, flash, render_template, redirect, request, session
from flask import url_for
from flask import jsonify
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Blueprint
import os
from dateutil.relativedelta import relativedelta
from functions import *
import numpy as np

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

patrick = Blueprint('patrick', __name__)

#G8P2 - patrick part
#code start


# Search for employee by name and employee ID
@patrick.route('/manager/employee', methods=["GET", "POST"])
def mviewemployee():
    emp_id = session["emp_id"]
    print("Emp_id from session:", emp_id)
     
    cur = getCursor()
    
    if request.method == "POST":
        search_query = request.form.get('search_query', '').strip()
        session['search_query'] = search_query
    else:
        search_query = session.get('search_query', '')

    query = '%' + search_query + '%'
        
    if search_query.strip() == "":
                sql = """SELECT 
                        e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
                        CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
                        CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                    FROM employee e
                    JOIN department d ON e.dept_id = d.dept_id
                    LEFT JOIN employee r ON e.report_to_name = r.emp_id
                    LEFT JOIN employee a ON e.approved_manager_name = a.emp_id
                    WHERE e.approved_manager_name = %s;"""
                cur.execute(sql, (emp_id,))
    else:
                sql = """SELECT 
                        e.emp_id, e.emp_fname, e.emp_lname, e.position_title, e.join_date, e.start_date, d.dept_name, e.email as username,
                        CONCAT(r.emp_fname, ' ', r.emp_lname) as report_to_name,
                        CONCAT(a.emp_fname, ' ', a.emp_lname) as approved_manager_name
                    FROM employee e
                    JOIN department d ON e.dept_id = d.dept_id
                    LEFT JOIN employee r ON e.report_to_name = r.emp_id
                    LEFT JOIN employee a ON e.approved_manager_name = a.emp_id
                    WHERE (e.emp_fname LIKE %s OR e.emp_lname LIKE %s OR CONVERT(e.emp_id, CHAR) LIKE %s) AND a.emp_id = %s;"""
                val = (query, query, query, emp_id)
                cur.execute(sql, val)    
                
    employees = cur.fetchall()
    return render_template("manager/mdashboardemployee.html", employees=employees)

# View leave requests for a particular employee
@patrick.route("/manager/employee/viewrequests", methods=["GET", "POST"])
def mviewrequest():
    
    flash_message = session.pop('flash', None)
    if flash_message is not None:
        flash(flash_message['message'], flash_message['category'])
    
    Employeeid = request.args.get('emp_id')
    if Employeeid is None:
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

    return render_template("manager/mdashboardeemployeerequests.html", 
                            pending_requests=pending_requests, 
                            approved_requests=approved_requests, 
                            rejected_requests=rejected_requests, 
                            emp_fname=emp_fname, 
                            emp_lname=emp_lname)

# View leave balances for a particular employee
@patrick.route("/manager/employee/viewbalance", methods=["GET", "POST"])
def mviewbalance(): 
    Employeeid = request.form.get('employee_id')
    leave_balances = fetch_employee_leave_balances(Employeeid)
    return render_template("manager/mdashboardviewbalance.html", leave_balances=leave_balances)

# Update leave request status for a particular employee's leave request
@patrick.route('/update_leave_request/<request_id>/<action>/<emp_id>', methods=['POST'])
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
        return redirect(url_for('patrick.mviewemployee'))
    
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
    return redirect(url_for('patrick.mviewemployee'))

# Edit leave request for a particular employee
@patrick.route('/manager/employee/requests/edit', methods=["POST"])
def mviewrequestedit():
    emp_id = request.form.get('emp_id')
    print(emp_id)
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
    print(leave_types)
    return render_template("manager/mvieweditrequest.html", emp_id=emp_id,leave_request_id=leave_request_id,emp_fname=emp_fname,emp_lname=emp_lname,leave_type=leave_type,leave_start_date=leave_start_date,leave_end_date=leave_end_date,additional_info=additional_info,hrs_req=hrs_req,leave_types=leave_types)

# Update leave request for a particular employee
@patrick.route("/manager/employee/requests/update", methods=["GET", "POST"])
def mviewrequestupdate():
        emp_id = request.form.get('emp_id')
        print(emp_id)
        leave_request_id = request.form.get('leave_request_id')
        leave_type_id = request.form.get('leave_type_id')
        print(leave_type_id)
        leave_start_date = request.form.get('leave_start_date')
        leave_end_date = request.form.get('leave_end_date')
        additional_info = request.form.get('additional_info')

        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(leave_start_date, date_format).date()
        end_date = datetime.strptime(leave_end_date, date_format).date()
        daydiff = end_date-start_date   
        days = daydiff.days
        hrs_req = days*7.5

        try:
            cur = getCursor()
            cur.execute("UPDATE leave_request SET leave_type_id = %s, leave_start_date = %s, leave_end_date = %s, additional_info = %s, hrs_req = %s, leave_status = 'Pending' WHERE leave_req_id = %s;", (leave_type_id, leave_start_date, leave_end_date, additional_info, hrs_req, leave_request_id))
            cur.execute("DELETE FROM leave_action WHERE leave_req_id = %s AND action_taken = 'approve';", (leave_request_id,))
        except Exception as e:
            session['flash'] = {
        'message': 'There is an error with your edit.',
        'category': 'danger'
    }
            return redirect(f"/manager/employee/viewrequests?emp_id={emp_id}")
        else:
            session['flash'] = {
        'message': f'Leave request is edited successfully.',
        'category': 'success'
    }
        return redirect(f"/manager/employee/viewrequests?emp_id={emp_id}")
          
# View projected leave balances for a particular employee
@patrick.route("/manager/employee/projected", methods=["POST"])
def mviewemployeeproject():
    emp_id = request.form.get('employee_id')
    leave_balances = fetch_employee_leave_balances(emp_id)
    return render_template("manager/mviewemployeeproject.html", emp_id=emp_id, leave_balances=leave_balances)

@patrick.route("/manager/employee/projected/<emp_id>", methods=["POST"])
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
    projected_accrual = f"{round(projected_accrual_cal, 2)} hours ({round(projected_accrual_cal / 7.5)} days)"
    estimated_projected_balance_cal = extract_number(leave_balances[0]["annual_leave_bal"]) + projected_accrual_cal - extract_number(leave_balances[0]["pending_annual_leave"]) - extract_number(leave_balances[0]["approved_annual_leave"])
    estimated_projected_balance = f"{round(estimated_projected_balance_cal, 2)} hours ({round(estimated_projected_balance_cal / 7.5)} days)"

    return jsonify({
        'date': date,
        'annual_leave_balance': annual_leave_balance,
        'leave_applied_not_paid': leave_applied_not_paid,
        'leave_applied_not_approved': leave_applied_not_approved,
        'projected_accrual': projected_accrual,
        'estimated_projected_balance': estimated_projected_balance
    })


#code end
