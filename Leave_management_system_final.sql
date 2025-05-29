DROP DATABASE IF EXISTS leave_management_system;

CREATE DATABASE leave_management_system;

USE leave_management_system;
DROP TABLE IF EXISTS department;

CREATE TABLE department (
  dept_id INT AUTO_INCREMENT PRIMARY KEY,
  dept_name VARCHAR(50) NOT NULL
);
DROP TABLE IF EXISTS role_type;

CREATE TABLE role_type (
  role_type_id INT AUTO_INCREMENT PRIMARY KEY,
  role_type VARCHAR(50) NOT NULL
);
DROP TABLE IF EXISTS leave_type;

CREATE TABLE leave_type (
  leave_type_id INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(50) NOT NULL,
  status VARCHAR(10) NOT NULL,
  leave_desc VARCHAR(255) NOT NULL
);
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  email VARCHAR(255) PRIMARY KEY,
  role_type_id INT NOT NULL,
  password VARCHAR(255) NOT NULL,
  CONSTRAINT fk_role_type
    FOREIGN KEY (role_type_id) REFERENCES role_type(role_type_id)
);

-- Drop the existing employee table
DROP TABLE IF EXISTS employee;

-- Recreate the employee table with the modified schema
-- create the employee table
CREATE TABLE employee (
  emp_id INT AUTO_INCREMENT PRIMARY KEY,
  emp_fname VARCHAR(50) NOT NULL,
  emp_lname VARCHAR(50) NOT NULL,
  join_date DATE NOT NULL,
  position_title VARCHAR(50) NOT NULL,
  start_date DATE NOT NULL,
  dept_id INT NOT NULL,
  email VARCHAR(255) NOT NULL,
  report_to_name INT,
  approved_manager_name INT,
  CONSTRAINT fk_department
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
  CONSTRAINT fk_employee_user
    FOREIGN KEY (email) REFERENCES users(email)
);

-- add the recursive foreign key for report_to_name
ALTER TABLE employee ADD CONSTRAINT fk_report_to_emp_id
  FOREIGN KEY (report_to_name) REFERENCES employee(emp_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

-- add the recursive foreign key for approved_manager_name
ALTER TABLE employee ADD CONSTRAINT fk_approved_manager_emp_id
  FOREIGN KEY (approved_manager_name) REFERENCES employee(emp_id)
  ON DELETE CASCADE
  ON UPDATE CASCADE;




DROP TABLE IF EXISTS leave_request;

CREATE TABLE leave_request (
  leave_req_id INT AUTO_INCREMENT PRIMARY KEY,
  emp_id INT NOT NULL,
  leave_type_id INT NOT NULL,
  leave_start_date DATE NOT NULL,
  leave_end_date DATE NOT NULL,
  hrs_req DECIMAL(5,2) NOT NULL,
  leave_status VARCHAR(50) NOT NULL,
  additional_info VARCHAR(255),
  CONSTRAINT fk_employee
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT fk_leave_type
    FOREIGN KEY (leave_type_id) REFERENCES leave_type(leave_type_id)
);
DROP TABLE IF EXISTS leave_balance;

CREATE TABLE leave_balance (
  bal_id INT AUTO_INCREMENT PRIMARY KEY,
  leave_type_id INT NOT NULL,
  emp_id INT NOT NULL,
  annual_leave_bal DECIMAL(5,2),
  sick_leave_bal DECIMAL(5,2) NOT NULL,
  updated_date DATE NOT NULL,
  CONSTRAINT fk_employee_balance
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
  CONSTRAINT fk_leave_type_balance
    FOREIGN KEY (leave_type_id) REFERENCES leave_type(leave_type_id)
);


CREATE TABLE leave_action (
  leave_action_id INT AUTO_INCREMENT PRIMARY KEY,
  leave_req_id INT NOT NULL,
  action_taken VARCHAR(50) NOT NULL,
  action_date DATE NOT NULL,
  role_type_id INT NOT NULL,
  reason VARCHAR(255),
  approved_manager_emp_id INT,
  CONSTRAINT fk_leave_request
    FOREIGN KEY (leave_req_id) REFERENCES leave_request (leave_req_id),
  CONSTRAINT fk_role_type_leave_action
    FOREIGN KEY (role_type_id) REFERENCES role_type(role_type_id),
  CONSTRAINT fk_approved_manager_emp_id_leave_action
    FOREIGN KEY (approved_manager_emp_id) REFERENCES employee(emp_id)
);

DROP TABLE IF EXISTS public_holiday;

CREATE TABLE public_holiday (
  pub_holi_id INT AUTO_INCREMENT PRIMARY KEY,
  holi_date DATE NOT NULL,
  holi_name VARCHAR(255) NOT NULL,
  emp_id INT NOT NULL,
  CONSTRAINT fk_employee_pub_holi
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

SET FOREIGN_KEY_CHECKS=0;

-- leave_balance

INSERT INTO leave_balance (leave_type_id, emp_id, annual_leave_bal, sick_leave_bal, updated_date) VALUES
(1, 1, 23, 0, '2023-05-13'),
(1, 2, 14, 0, '2023-05-13'),
(2, 3, 16, 0, '2023-05-13'),
(2, 4, 19, 0, '2023-05-13'),
(1, 5, 21, 0, '2023-05-13'), 
(1, 6, 16, 0, '2023-05-13'),
(2, 7, 43, 0, '2023-05-13'),
(2, 8, 33, 37.5, '2023-05-13'),
(1, 9, 35, 37.5, '2023-05-13'),
(1, 10, 23, 37.5, '2023-05-13'),
(2, 11, 54, 37.5, '2023-05-13'),
(2, 12, 34, 37.5, '2023-05-13'),
(1, 13, 54, 37.5, '2023-05-13'),
(1, 14, 14, 37.5, '2023-05-13'),
(2, 15, 18, 37.5, '2023-05-13'),
(2, 16, 19, 37.5, '2023-05-13'),
(1, 17, 22, 37.5, '2023-05-13'),
(1, 18, 26, 37.5, '2023-05-13'),
(2, 19, 29, 37.5, '2023-05-13'),
(2, 20, 20, 37.5, '2023-05-13'),
(1, 21, 21, 37.5, '2023-05-13'),
(1, 22, 43, 37.5, '2023-05-13'),
(2, 23, 44, 37.5, '2023-05-13'),
(2, 24, 23, 37.5, '2023-05-13'),
(1, 25, 23, 37.5, '2023-05-13'),
(1, 26, 21, 37.5, '2023-05-13'),
(2, 27, 12, 37.5, '2023-05-13'),
(2, 28, 22, 37.5, '2023-05-13'),
(1, 29, 11, 37.5, '2023-05-13'),
(1, 30, 17, 37.5, '2023-05-13'),
(2, 31, 11, 37.5, '2023-05-13'),
(2, 32, 13, 37.5, '2023-05-13'),
(1, 33, 18, 37.5, '2023-05-13'),
(1, 34, 10, 37.5, '2023-05-13'),
(2, 35, 29, 37.5, '2023-05-13'),
(2, 36, 22, 37.5, '2023-05-13'),
(1, 37, 25, 37.5, '2023-05-13'),
(1, 38, 27, 37.5, '2023-05-13'),
(2, 39, 28, 37.5, '2023-05-13'),
(2, 40, 34, 37.5, '2023-05-13'),
(1, 41, 37, 37.5, '2023-05-13'),
(1, 42, 33, 37.5, '2023-05-13'),
(2, 43, 32, 37.5, '2023-05-13'),
(2, 44, 28, 37.5, '2023-05-13');

-- department table
INSERT INTO department (dept_name) VALUES
('Corporate Services'),
('Computer Science'),
('Mathematics'),
('Physics'),
('Chemistry');


-- leave type table
INSERT INTO leave_type (type, status, leave_desc)
VALUES 
  ('Annual', '1', 'Leave entitlement that employees can use for holidays'),
  ('Bereavement', '1', 'Leave taken by employees due to the death of a family member or friend'),
  ('Parental','1', 'Leave taken by employees to care for a newborn or newly adopted child'),
  ('Sick Family', '1', 'Leave taken by employees to care for a sick family member'),
  ('Sick Leave', '1', 'Leave taken by employees due to personal illness or injury'),
  ('Special Leave without Pay', '1', 'Leave taken by employees that is not covered by other leave types and is without pay'),
  ('Special Leave with Pay', '1', 'Leave taken by employees that is not covered by other leave types and is with pay');

-- role type table
INSERT INTO role_type (role_type)
VALUES
('Employee'),
('Approval Manager'),
('Admin');

INSERT INTO users (email, role_type_id, password)
VALUES 
('william.jones@university.edu', 1, '5aP#9sRcT'),
('john.doe@university.edu', 2, 'password1'),
('jane.smith@university.edu', 1, 'password2'),
('michael.johnson@university.edu', 2, 'password3'), 
('sarah.lee@university.edu', 2, 'password4'),
('mark.chen@university.edu', 2, 'password5'),
('emily.wang@university.edu', 2, 'password6'),
('david.nguyen@university.edu', 2, 'password7'),
('bob.johnson@university.edu', 2, 'password123'),
('alice.williams@university.edu', 1, 'password456'),
('sarah.nguyen@university.edu', 2, 'password789'),
('max.anderson@university.edu', 2, 'password123'),
('olivia.johnson@university.edu', 1, 'password456'),
('daniel.garcia@university.edu', 1, 'password789'),
('megan.lee@university.edu', 1, 'password123'),
('matthew.chen@university.edu', 1, 'password456'),
('lucas.kim@university.edu', 1, 'password789'),
('ava.gonzalez@university.edu', 1, 'password123'),
('noah.smith@university.edu', 1, 'password456'),
('chloe.nguyen@university.edu', 1, 'password789'),
('ethan.wong@university.edu', 1, 'password123'),
('isabella.chen@university.edu', 1, 'password456'),
('david.lee@university.edu', 1, 'S&2P8u@NfC'),
('emily.wong@university.edu', 1, 'Kt4$zY6!dV'),
('michael.chen@university.edu', 1, 'R#7mZ9^sLw'),
('daniel.wright@university.edu', 1, 'Xc8Gv@1nBq'),
('sophie.kim@university.edu', 1, 'Tg2Jf%5kPz'),
('alex.nguyen@university.edu', 1, 'Mw6Tl#9pRy'),
('olivia.smith@university.edu', 1, 'Hj3Dx@7rKq'),
('avery.brown@university.edu', 1, 'Vb1Nk%2tLs'),
('grace.taylor@university.edu', 1, 'Yh9Fz#6pRq'),
('max.garcia@university.edu', 1, 'Lm5Cn@3sVf'),
('isabella.wilson@university.edu', 1, 'Qd2Xj%9gTc'),
('ethan.johnson@university.edu', 1, 'Bt7Mf#1pNz'),
('liam.miller@university.edu', 1, 'Zs4Lx!8mFp'),
('sophia.anderson@university.edu', 1, 'Aq6Gy$2wPz'),
('aiden.clark@university.edu', 1, 'Cn8Vb@3tMq'),
('mia.martinez@university.edu', 1, 'Uy4Np@9cXz'),
('harper.clark@university.edu', 1, 'Ew7Kf$3sLq'),
('mia.allen@university.edu', 1, 'Pj2Tn@6mGh'),
('adam.lee@university.edu', 3, '8fD#3gHjK'),
('anne.smith@university.edu', 3, '7hJ#2kLmN'),
('tom.johnson@university.edu', 3, '9rT#4uVxY'),
('alice.brown@university.edu', 3, '6eF#1bGhJ');


-- Insert or update the rows that were causing the foreign key constraint error

SET FOREIGN_KEY_CHECKS=0;


INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (1,'William','Jones','2000-01-01','Vice-Chancellor','2000-01-01',1,'william.jones@university.edu',42,44);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (2,'John','Doe','2010-09-01','Professor','2010-09-01',2,'john.doe@university.edu',41,41);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (3,'Jane','Smith','2015-09-01','Professor','2015-09-01',2,'jane.smith@university.edu',42,42);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (4,'Michael','Johnson','2010-01-01','Professor','2010-01-01',3,'michael.johnson@university.edu',1,6);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (5,'Sarah','Lee','2015-01-01','Professor','2015-01-01',2,'sarah.lee@university.edu',3,4);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (6,'Mark','Chen','2018-01-01','Professor','2018-01-01',3,'mark.chen@university.edu',4,5);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (7,'Emily','Wang','2019-01-01','Professor','2019-01-01',4,'emily.wang@university.edu',3,6);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (8,'David','Nguyen','2020-01-01','Professor','2020-01-01',5,'david.nguyen@university.edu',2,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (9,'Bob','Johnson','2020-09-01','Lecturer','2020-09-01',2,'bob.johnson@university.edu',2,2);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (10,'Alice','Williams','2021-01-01','Lecturer','2021-01-01',2,'alice.williams@university.edu',2,2);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (11,'Sarah','Nguyen','2021-05-01','Lecturer','2021-05-01',3,'sarah.nguyen@university.edu',4,4);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (12,'Max','Anderson','2022-02-15','Lecturer','2022-02-15',4,'max.anderson@university.edu',7,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (13,'Olivia','Johnson','2022-03-01','Lecturer','2022-03-01',4,'olivia.johnson@university.edu',7,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (14,'Daniel','Garcia','2022-03-15','Lecturer ','2022-03-15',3,'daniel.garcia@university.edu',4,4);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (15,'Megan','Lee','2021-09-01','Lecturer','2021-09-01',4,'megan.lee@university.edu',7,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (16,'Matthew','Chen','2022-01-01','Lecturer','2022-01-01',5,'matthew.chen@university.edu',8,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (17,'Lucas','Kim','2022-05-01','Lecturer','2022-05-01',3,'lucas.kim@university.edu',4,4);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (18,'Ava','Gonzalez','2021-07-01','Lecturer','2021-07-01',4,'ava.gonzalez@university.edu',7,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (19,'Noah','Smith','2022-04-15','Lecturer','2022-04-15',5,'noah.smith@university.edu',8,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (20,'Chloe','Nguyen','2021-10-01','Lecturer','2021-10-01',3,'chloe.nguyen@university.edu',4,4);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (21,'Ethan','Wong','2022-02-01','Lecturer','2022-02-01',4,'ethan.wong@university.edu',7,7);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (22,'Isabella','Chen','2021-11-01','Lecturer','2021-11-01',5,'isabella.chen@university.edu',8,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (23,'David','Lee','2022-02-01','Tutor','2022-02-01',2,'david.lee@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (24,'Emily','Wong','2022-02-01','Tutor','2022-02-01',2,'emily.wong@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (25,'Michael','Chen','2022-02-01','Tutor','2022-02-01',2,'michael.chen@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (26,'Daniel','Wright','2022-03-01','Tutor','2022-03-01',3,'daniel.wright@university.edu',11,11);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (27,'Sophie','Kim','2022-03-01','Tutor','2022-03-01',3,'sophie.kim@university.edu',11,11);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (28,'Alex','Nguyen','2022-03-01','Tutor','2022-03-01',3,'alex.nguyen@university.edu',11,11);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (29,'Olivia','Smith','2022-04-01','Tutor','2022-04-01',4,'olivia.smith@university.edu',12,12);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (30,'Avery','Brown','2022-04-01','Tutor','2022-04-01',4,'avery.brown@university.edu',12,12);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (31,'Grace','Taylor','2022-04-01','Tutor','2022-04-01',4,'grace.taylor@university.edu',12,12);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (32,'Max','Garcia','2022-05-01','Tutor ','2022-05-01',2,'max.garcia@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (33,'Isabella','Wilson','2022-05-01','Tutor','2022-05-01',2,'isabella.wilson@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (34,'Ethan','Johnson','2022-05-01','Tutor ','2022-05-01',2,'ethan.johnson@university.edu',9,9);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (35,'Liam','Miller','2022-06-01','Tutor','2022-06-01',5,'liam.miller@university.edu',16,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (36,'Sophia','Anderson','2022-06-01','Tutor','2022-06-01',5,'sophia.anderson@university.edu',16,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (37,'Aiden','Clark','2022-06-01','Tutor','2022-06-01',5,'aiden.clark@university.edu',16,8);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (38,'Mia','Martinez','2022-07-01','Tutor','2022-07-01',3,'mia.martinez@university.edu',11,11);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (39,'Harper','Clark','2022-02-01','Tutor','2022-02-01',4,'harper.clark@university.edu',12,12);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (40,'Mia','Allen','2022-02-01','Tutor','2022-02-01',4,'mia.allen@university.edu',12,12);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (41,'Adam','Lee','2020-01-01','Human Resources Director','2020-01-01',1,'adam.lee@university.edu',1,42);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (42,'Anne','Smith','2018-01-01','Human Resources Director','2018-01-01',1,'jane.smith@university.edu',1,43);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (43,'Tom','Johnson','2022-03-01','Technology Director','2022-03-01',1,'tom.johnson@university.edu',1,44);
INSERT INTO employee (`emp_id`,`emp_fname`,`emp_lname`,`join_date`,`position_title`,`start_date`,`dept_id`,`email`,`report_to_name`,`approved_manager_name`) VALUES (44,'Alice','Brown','2019-01-01','Finance Director','2019-01-01',1,'alice.brown@university.edu',1,41);


-- leave_request 
INSERT INTO leave_request (emp_id, leave_type_id, leave_start_date, leave_end_date, hrs_req, leave_status, additional_info)
VALUES
  (1, 1, '2023-06-01', '2023-06-04', 30.00, 'Pending', 'Going on vacation'),
  (2, 2, '2023-06-12', '2023-06-15', 15.00, 'Approved', 'Family emergency'),
  (3, 3, '2023-06-22', '2023-06-23', 15.00, 'Rejected', 'Not enough accrued leave'),
  (4, 1, '2023-07-01', '2023-07-05', 37.50, 'Pending', 'Attending conference'),
  (1, 4, '2023-07-15', '2023-07-20', 7.50, 'Pending', 'Sick leave'),
  (3, 2, '2023-07-25', '2023-07-28', 15.00, 'Approved', 'Personal reasons'),
  (7, 1, '2023-06-01', '2023-06-04', 45.00, 'Pending', 'Going on vacation'),
  (8, 2, '2023-06-12', '2023-06-15', 15.00, 'Approved', 'Family emergency'),
  (7, 3, '2023-06-22', '2023-06-23', 30.00, 'Rejected', 'Not enough accrued leave'),
  (13, 1, '2023-07-01', '2023-07-05', 37.50, 'Pending', 'Attending conference'),
  (11, 4, '2023-07-15', '2023-07-20', 15.00, 'Pending', 'Sick leave'),
  (21, 2, '2023-07-25', '2023-07-28', 30.00, 'Approved', 'Personal reasons');
  



INSERT INTO public_holiday (holi_date, holi_name, emp_id)
VALUES 
('2023-01-01', "New Year's Day", 41),
('2023-01-02', "Day after New Year's Day", 41),
('2023-02-06', 'Waitangi Day', 41),
('2023-04-14', 'Good Friday', 41),
('2023-04-17', 'Easter Monday', 41),
('2023-04-25', "ANZAC Day", 41),
('2023-06-05', "Queen's Birthday", 41),
('2023-10-23', "Labour Day", 41),
('2023-12-25', 'Christmas Day', 41),
('2023-12-26', 'Boxing Day', 41),
('2023-01-01', "New Year's Day", 42),
('2023-01-02', "Day after New Year's Day", 42),
('2023-02-06', 'Waitangi Day', 42),
('2023-04-14', 'Good Friday', 42),
('2023-04-17', 'Easter Monday', 42),
('2023-04-25', "ANZAC Day", 42),
('2023-06-05', "Queen's Birthday", 42),
('2023-10-23', "Labour Day", 42),
('2023-12-25', 'Christmas Day', 42),
('2023-12-26', 'Boxing Day', 42),
('2024-01-01', "New Year's Day", 41),
('2024-01-02', "Day after New Year's Day", 41),
('2024-02-06', 'Waitangi Day', 41),
('2024-03-29', 'Good Friday', 41),
('2024-04-01', 'Easter Monday', 41),
('2024-04-25', "ANZAC Day", 41),
('2024-06-03', "Queen's Birthday", 41),
('2024-06-28', "Matariki", 41),
('2024-10-28', "Labour Day", 41),
('2024-12-25', 'Christmas Day', 41),
('2024-12-26', 'Boxing Day', 41),
('2024-01-01', "New Year's Day", 42),
('2024-01-02', "Day after New Year's Day", 42),
('2024-02-06', 'Waitangi Day', 42),
('2024-03-29', 'Good Friday', 42),
('2024-04-01', 'Easter Monday', 42),
('2024-04-25', "ANZAC Day", 42),
('2024-06-03', "Queen's Birthday", 42),
('2024-06-28', "Matariki", 42),
('2024-10-28', "Labour Day", 42),
('2024-12-25', 'Christmas Day', 42),
('2024-12-26', 'Boxing Day', 42);


