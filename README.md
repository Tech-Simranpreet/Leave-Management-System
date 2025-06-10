# Employee Leave Management System

This is a full-stack Leave Management System developed as part of a group project. The system supports employee leave applications, validations, notifications, and balance projections. My core responsibility was designing and implementing the **Leave Request Workflow**, including its business logic, database interactions, and user interface integration.

# My Contribution

I was primarily responsible for building the **Employee Leave Request Module** and **Projected Leave Balance Calculator**, which involved:

### User Session Management
- Checked for authenticated sessions before allowing access to leave functionality.
- Ensured route protection and redirection for unauthenticated users.

### Leave Request Functionality
- Enabled employees to apply for leave by selecting leave type, start and end dates, and additional information.
- Fetched employee data from the database using secure queries.
- Implemented detailed validation to ensure:
  - End date is not earlier than the start date.
  - Duplicate leave entries for overlapping dates are prevented.
  - Only working days are counted towards leave duration.
  - Leave duration calculation excludes public holidays and weekends.
  
### Business Day & Leave Hour Calculation
- Used `numpy.busday_count()` to calculate business days between two dates.
- Integrated logic to count hours based on a standard 7.5 hours per day.
- Accounted for public holidays (fetched from the database) to improve accuracy.

### Email Notification System
- Developed a function to send automated leave submission emails to the employee's approving manager.
- Used SMTP with secure authentication and templated content.

### Projected Leave Balance Estimator
- Built a tool to help employees predict their leave balance for a future date.
- Used current balance, pending approvals, approved leaves, and future accrual calculations to project remaining leave hours/days.
- Returned the result via JSON for frontend AJAX consumption.

## Technologies & Tools Used

- **Backend**: Python, Flask, Jinja2
- **Database**: MySQL (via `mysql.connector`)
- **Frontend**: HTML, Bootstrap (via templates)
- **Email**: SMTP, Gmail
- **Libraries**: NumPy for business day calculations
- **Others**: Sessions, Flash messaging, JSON API

## Highlights of My Work

- Integrated Flask with MySQL for real-time form data handling and validation.
- Built reusable utility functions (`check_leave_exists`, `get_public_holidays`, `count_business_days`) to modularize logic.
- Maintained a clean and user-friendly leave submission workflow with accurate business logic and validations.
- Implemented a robust email notification feature for streamlined communication with managers.
- Provided projected leave insights by dynamically calculating accruals based on future dates.

## Key Skills Demonstrated

- Flask routing and session-based authentication
- SQL query building and parameterization
- Time-based calculations using NumPy and datetime
- Flask `Blueprints` for modular code structure
- Exception handling and user feedback using `flash()`
- JSON response handling for AJAX operations



Data Model

The following two diagrams provided is Hierarchy Chart and Entity Relationship Model (ERM) designed by the CS team for the leave management system of Lincoln University.

One type of leave has many leave requests. (1-to-many)
An employee can make many leave requests. (1-to-many)
An employee can have a much leave balance. (1-to-many)
One leave type has more than one leave balance. (1-to-many)
One leave balance can be for only one type of leave. (1-to-1)
Only one employee has many projected leave balance. (1-to-many)
One projected leave balance can be for only one employee. (1-to-1)
Only one leave request is made by only one employee. (1-to-1)
One leave type balance is for only one employee. (1-to-1)
One leave request is for only one type of leave. (1-to-1)
One user can have many public holidays. (1-to-many)

ERD
Link:https://github.com/LUMasterOfAppliedComputing/comp639-2023-s1-project2-group8/blob/main/ERD.png

Role Hierarchy Chart
Link: https://github.com/LUMasterOfAppliedComputing/comp639-2023-s1-project2-group8/blob/main/hierachy%20chart.png
################################################################################

Artefact

1 Employee Artefact

All the users are the employees of Lincoln University and they all use Leave Management System for applying leaves. An employee works 5 days a week for 7.5 hours each day, they get 30 Annual leaves and 5 sick leaves. An employee has been given the credentials to log in to the Leave Management System, and the first screen which appears as the Dashboard ( route- /user ), shows the Leaves requested by the employee in a table along with the Approved leaves in another table.

• From the requested leaves table which are unapproved leaves, employee can still edit and delete the requested leave.

    If a user clicks on edit, it will redirect user to “/editrequest” route, from where user can change leave type, start date, end date or the reason, once the details are edited, user can click on Update and then it will again redirect the user to the Dashboard.

    If user will click on delete, then the user will be prompted to enter the reason for deleting the leave which is required, and then can delete the request once the reason is submitted. However, if a user has to apply for a leave, user can click on “Apply” button and then will get redirected to “/apply/default” route with the Leave request form.

    In the form, user can fill the details as Leave Type, Start date, End date and Additional info as the textarea, where user can mention reason for taking leave. After clicking on submit, user will get redirected to “/submission?hrs_req=” route showing that the leave request has been submitted with the requested hours. The calendar has the validation as the End date can not be earlier than the start date, all weekends and public holidays are disabled. Hours requested are calculated on the basis of the working hours of the employee.

• Then on the same route “/apply/default”, user have other 3 options along with the request leave, which are View Requests, View Balance, Projected Leave Balance.

    View Request- By clicking on view request, “/employee/viewrequests” route opens and all the leaves are shown in distinct tables to the users from where the user can track his leaves.

    By click on View Balance, “/employee/viewbalance” user gets redirected to this route and can access six different types of leave balances.

    However, by clicking on Projected Leave Balance, user can select future date from the calendar and can access the projected leave balance by clicking on calculate projected balance when “/employee/projected” route opens. While,

    by clicking the button where the user’s name is shown, a drop down appears and user can view his profile by clicking on profile. There is an option of change password as well.

• Overall, this Leave Management System allows the users to apply new leaves and manage the already requested leaves along with their remaining leave balances.

2 Approval Manager Artefact

When users log into the Approval Manager interface, they will see a familiar navigation system where they will find links that lead them to the Dashboard and Apply across the top. They also have the options to view their own profile, change their password, and log out. These features are easily accessible in the top-right corner of the interface. For more specific tasks for the approval manager, users will have additional navigational links that allow them to manage requests, search for employees, access the Leave Exception Report, and view the Annual Leave Liability Report.

• Dashboard

    On the Dashboard, users can search for specific leave requests by inputting an employee's first or last name, or even the leave status. If the user wishes to view all employees, they simply need to click the search button, turning the search box into an optional feature for more detailed inquiries. Once a search is completed, a table will appear, displaying all the corresponding employees along with their respective leave details.

    The Dashboard also serves as a hub for all leave requests that the approval manager is in charge of, including both approved and unapproved ones. For any unapproved requests, users have the ability to edit, approve, reject, or delete them according to their needs. Approved but unpaid leave requests can

    be edited or deleted as well. Once these leave requests have been paid, they will no longer be visible on the Dashboard. Furthermore, the users will find their own leave requests displayed at the bottom of the page, and they will be able to manage unapproved requests similarly. To keep the interface uncluttered and user-friendly, each category of requests is limited to show a maximum of five rows at once. Users can use the pagination feature view additional rows. If there are no leave requests, it will show the text “There are no unapproved/approved requests yet” on the screen.

• Managing leaves

    Users can approve a leave request by clicking the “Approve” button, which triggers a confirmation message displayed at the top of the page. If the user chooses to reject or delete a leave request, they are required to provide a reason for their decision. Once a leave request is rejected or deleted, a confirmation message will be displayed at the top of the page. Regardless of whether the leave request is approved, rejected, or deleted, an email notification will be sent to the respective employee detailing the action taken and the provided reason.

• Searching for an employee

    Within the “Employee” tab, users can search for an employee by entering their first name, last name, or employee ID. Following the completion of the search, a table containing detailed employee information will be displayed. This table includes actionable buttons that allow users to view the selected employee's leave requests, current leave balances, and projected leave balances. A responsive design methodology is used here to maintain an optimal mobile user experience, as well as desktop experience.

    Upon clicking the "View Requests" button, the user will see all of the selected employee's leave requests, whether pending, approved, or rejected.

    This view also includes approved leaves that have already been paid which is different from what the user can see from the dashboard. By clicking the "View Balance" button, users can access the current annual and sick leave balances of the selected employee. This shows the balance (at close of last pay), leave approved not paid and leave applied not yet approved. The balance shows in both hours and days. By clicking on the "View Projected Balance" button, users can select a future date from a date picker, which allows them to project an employee's annual leave balance as of that selected date. This date can range from the present day up to one year into the future.

    Once a date is selected, the user then clicks the “Calculate Projected Balance” button. The resulting table will display the employee's annual leave balance as it stood at the end of the last pay period, leave applications that have been approved but not yet paid, and leave applications not yet approved. In addition, it also includes the projected accrual balance, which is an estimate of the leave the employee will accumulate by the selected date. Finally, the table provides an estimated projected leave balance both in hours and days.

    A “Return to Employee List” is shown under each page, when it is clicked, the user will be taken back to the previous page where they can continue their search.

• Reports

    In the “Leave Exception Report” tab, users can generate a report that lists all employees with an annual leave balance that is equal to or greater than 30 days. The report is presented in a table format, displaying the employee's basic details along with their leave balance in both hours and days. The “Annual Leave Liability Report” tab offers a similar report that lists all employees under the

    manager's authority and displays their respective leave balances. Both of these reports can be sorted for better visibility and easier data comprehension.

3 Admin Artefact

• As an administrator, you have access to additional tabs and functionalities compared to approval managers. You can perform various tasks related to employees, such as checking leave requests, leave balances, and project balances for all employees in the university. Additionally, you have the ability to change employees' role types, granting you the flexibility to modify their access and permissions.

• Moving on to the unique functions of administrators, the "Leave Type" tab allows you to manage and view all leave types. You can activate or deactivate types, edit their names and descriptions, and ensure that each type has a unique name. You can also add new leave types based on the requirements provided, but there is no option to delete existing types.

• In the "Holiday" tab, you can view and manage holidays for the current year and the following year. As an administrator, you can add new holidays, edit existing ones, and delete them if necessary. Duplicate validation is not implemented for holidays, considering their annual recurrence.

• Finally, the "Update Balance" function simplifies the process of updating staff balances. Admins are required to manually update balances every two weeks. A validation mechanism ensures that the update can only be performed when the displayed next payroll date matches the current date. This helps prevent accidental balance updates on incorrect dates. When the validation is successful, clicking the "Update" button will update all staff balances, deducting the amounts used until the current date. A success message is displayed upon completion,

    while an error message is shown if the dates do not match.

• Please note:

It is crucial to ensure that the current date of your computer is adjusted to match the "Next Payroll Date" displayed on the "Update Balance" page before testing the update balance functionality as an administrator. Only when the dates match, the administrator can successfully test the update balance feature and receive a green success notification. If the dates do not match, a red error notification will be displayed. This validation mechanism ensures that administrators perform the balance update operation at the appropriate time, preventing any unintended actions on incorrect dates. Please make sure to adjust your computer's current date accordingly.
