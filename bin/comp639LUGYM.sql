DROP SCHEMA IF EXISTS LUGYM;
CREATE SCHEMA LUGYM;
USE LUGYM;

/* Created by Changpo Jiang 1148594, When doing database design, I try to find a balance between elegant design
 and programmer code workload. If you want to design a perfect design, support multiple functions in the future, 
 and ensure that data is not redundant, you must join More tables, but adding more tables will require programmers
  to write longer sql statements, which will become code redundancy. So the design has considered the optimal design
   after the above requirements.*/


CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `familyname` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `role` int DEFAULT NULL,       /*reference 0 member, 1 trainer, 2 manager*/
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`userid`)
);

CREATE TABLE `member` (
  `memberid` int NOT NULL AUTO_INCREMENT,
  `userid` int NOT NULL,
  `dateofbirth` date DEFAULT NULL,
  `address` varchar(55) DEFAULT NULL,
  `health` varchar(85) DEFAULT NULL,
  `active` int DEFAULT NULL,		/*reference 0 non-active, 1 active */
  PRIMARY KEY (`memberid`),
  CONSTRAINT FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE
);

CREATE TABLE `trainer` (
  `trainerid` int NOT NULL AUTO_INCREMENT,
  `userid` int NOT NULL,
  `dateofbirth` date DEFAULT NULL,
  `address` varchar(55) DEFAULT NULL,
  `qualification` varchar(85) DEFAULT NULL,
  `jobtitle` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`trainerid`),
  CONSTRAINT FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE
);

CREATE TABLE `class` (
  `classid` int NOT NULL AUTO_INCREMENT,
  `classname` varchar(45) DEFAULT NULL,
  `category` varchar(15) DEFAULT NULL,
  `dateofstart` datetime DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `description` longtext,
  `bookingnumber` int,
  PRIMARY KEY (`classid`)

);

CREATE TABLE `payment` (
  `paymentid` int NOT NULL AUTO_INCREMENT,
  `paymentname` varchar(45) DEFAULT NULL,
  `category` int DEFAULT NULL, /*reference  1 subscription, 2 session*/
  `datetime` datetime DEFAULT NULL,
  `paymentstatus` int DEFAULT NULL,  /*reference 0 success, 1 pending, 2 failed*/
  `description` longtext,
  `amount` DECIMAL(9,2) NOT NULL,
  `memberid` int NOT NULL,
  `trainerid` int,
  PRIMARY KEY (`paymentid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`)
);

CREATE TABLE `session` (
  `sessionid` int NOT NULL AUTO_INCREMENT,
  `trainerid` int DEFAULT NULL,
  `category` varchar(15) DEFAULT NULL,
  `dateofstart` datetime DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `description` longtext,
  `price` DECIMAL(9,2) NOT NULL,
  PRIMARY KEY (`sessionid`),
  CONSTRAINT FOREIGN KEY (`trainerid`) REFERENCES `trainer` (`trainerid`)
);




CREATE TABLE `classbooking` (
  `classbookingid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `classid` int,
  `trainerid` int,
  `datetime` datetime NOT NULL,
  `success` tinyint DEFAULT NULL,
  `attendance` int,  /*reference 0 attendance, 1 absent*/
  PRIMARY KEY (`classbookingid`),
   CONSTRAINT FOREIGN KEY (`classid`) REFERENCES `class` (`classid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`),
   CONSTRAINT FOREIGN KEY (`trainerid`) REFERENCES `trainer` (`trainerid`)
);

CREATE TABLE `sessionbooking` (
  `sessionbookingid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `sessionid` int,
  `paymentid` int,
  `trainerid` int,
  `datetime` datetime NOT NULL,
  `success` tinyint DEFAULT NULL,
  `attendance` int,  /*reference 0 attendance, 1 absent*/
  PRIMARY KEY (`sessionbookingid`),
   CONSTRAINT FOREIGN KEY (`sessionid`) REFERENCES `session` (`sessionid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`),
   CONSTRAINT FOREIGN KEY (`trainerid`) REFERENCES `trainer` (`trainerid`),
   CONSTRAINT FOREIGN KEY (`paymentid`) REFERENCES `payment` (`paymentid`)
);

CREATE TABLE `subscription` (
  `subscriptionid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `price` DECIMAL(9,2),
  `paymentid` int,
  `dateofstart` date,
  `dateofexpiration` date NOT NULL,
  `success` tinyint DEFAULT NULL,
  PRIMARY KEY (`subscriptionid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`),
   CONSTRAINT FOREIGN KEY (`paymentid`) REFERENCES `payment` (`paymentid`)
);


CREATE TABLE `attendance` (
  `attendanceid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `datetime` datetime NOT NULL,
   PRIMARY KEY (`attendanceid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`)
);

CREATE TABLE `notification` (
  `notificationid` int NOT NULL AUTO_INCREMENT,
  `memberid` int NOT NULL,
  `datetime` datetime NOT NULL,
  `title` varchar(45) DEFAULT NULL,
  `message` longtext,
  `status` int,  /*reference 0 successfully sent, 1 have read*/
   PRIMARY KEY (`notificationid`),
   CONSTRAINT FOREIGN KEY (`memberid`) REFERENCES `member` (`memberid`)
);

INSERT INTO user VALUES(100,'lixiaowei','Xiaowei','li','lixiaowei@gamil.com',0,'');
INSERT INTO user VALUES(101,'ericli','Eric','li','EricLi@gamil.com',0,'');
INSERT INTO user VALUES(102,'faysong',' Fay','song',' FaySong1155193@gamil.com',0,'');
INSERT INTO user VALUES(103,'jessicazhao','Jessica','zhao','JessicaZhao@gamil.com',1,'');
INSERT INTO user VALUES(104,'cpjiang','CP','jiang','changpo.jiang@gamil.com',2,'');
INSERT INTO user VALUES(105,'alexliu','Alex','liu','aleeex@gamil.com',1,'');


INSERT INTO member VALUES(100,100,'1980-07-24','lincoln','good health',1);
INSERT INTO member VALUES(101,101,'1990-07-12','lincoln','good health',1);
INSERT INTO member VALUES(102,102,'1999-01-24','lincoln','good health',1);

INSERT INTO trainer VALUES(101,103,'1998-08-24','lincoln','master','senior coach');
INSERT INTO trainer VALUES(103,105,'1995-1-11','christchurch','master','coach');

INSERT INTO class VALUES(100,'Bodypump','practice','2023-03-20 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',1);
INSERT INTO class VALUES(101,'Yoga','stretch','2023-03-20 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',1);
INSERT INTO class VALUES(102,'Zumba','dance','2023-03-20 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',27);
INSERT INTO class VALUES(103,'Yoga','stretch','2023-03-21 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',28);
INSERT INTO class VALUES(104,'Pilates','stretch','2023-03-21 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',27);
INSERT INTO class VALUES(105,'Sprint','bicycle','2023-03-22 08:00:00','bicycle hall','bicycle dance',30);
INSERT INTO class VALUES(106,'Pilates','stretch','2023-03-22 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',20);
INSERT INTO class VALUES(107,'Bodypump','practice','2023-03-23 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',27);
INSERT INTO class VALUES(108,'Yoga','stretch','2023-03-24 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',1);
INSERT INTO class VALUES(109,'Zumba','dance','2023-03-24 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',13);
INSERT INTO class VALUES(110,'Yoga','stretch','2023-03-25 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',12);
INSERT INTO class VALUES(111,'Pilates','stretch','2023-03-25 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',11);
INSERT INTO class VALUES(112,'Sprint','bicycle','2023-03-26 08:00:00','bicycle hall','bicycle dance',12);
INSERT INTO class VALUES(113,'Pilates','stretch','2023-03-26 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',11);

INSERT INTO class VALUES(114,'Bodypump','practice','2023-03-27 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',22);
INSERT INTO class VALUES(115,'Yoga','stretch','2023-03-27 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',23);
INSERT INTO class VALUES(116,'Zumba','dance','2023-03-27 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',23);
INSERT INTO class VALUES(117,'Yoga','stretch','2023-03-28 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',28);
INSERT INTO class VALUES(118,'Pilates','stretch','2023-03-28 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',22);
INSERT INTO class VALUES(119,'Sprint','bicycle','2023-03-29 08:00:00','bicycle hall','bicycle dance',21);
INSERT INTO class VALUES(120,'Pilates','stretch','2023-03-29 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',13);
INSERT INTO class VALUES(121,'Bodypump','practice','2023-03-29 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',12);
INSERT INTO class VALUES(122,'Yoga','stretch','2023-03-30 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',3);
INSERT INTO class VALUES(123,'Zumba','dance','2023-03-30 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',4);
INSERT INTO class VALUES(124,'Yoga','stretch','2023-03-31 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',12);
INSERT INTO class VALUES(125,'Pilates','stretch','2023-03-31 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',13);
INSERT INTO class VALUES(126,'Sprint','bicycle','2023-04-1 08:00:00','bicycle hall','bicycle dance',12);
INSERT INTO class VALUES(127,'Pilates','stretch','2023-04-1 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',15);

INSERT INTO class VALUES(128,'Bodypump','practice','2023-04-03 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',22);
INSERT INTO class VALUES(129,'Yoga','stretch','2023-04-03 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',23);
INSERT INTO class VALUES(130,'Zumba','dance','2023-04-03 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',23);
INSERT INTO class VALUES(131,'Yoga','stretch','2023-04-04 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',28);
INSERT INTO class VALUES(132,'Pilates','stretch','2023-04-04 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',22);
INSERT INTO class VALUES(133,'Sprint','bicycle','2023-04-05 08:00:00','bicycle hall','bicycle dance',21);
INSERT INTO class VALUES(134,'Pilates','stretch','2023-04-05 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',2);
INSERT INTO class VALUES(135,'Bodypump','practice','2023-04-05 08:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',0);
INSERT INTO class VALUES(136,'Yoga','stretch','2023-04-06 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',5);
INSERT INTO class VALUES(137,'Zumba','dance','2023-04-06 19:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',8);
INSERT INTO class VALUES(138,'Yoga','stretch','2023-04-06 12:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',10);
INSERT INTO class VALUES(139,'Pilates','stretch','2023-04-07 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',6);
INSERT INTO class VALUES(140,'Sprint','bicycle','2023-04-08 08:00:00','bicycle hall','bicycle dance',12);
INSERT INTO class VALUES(141,'Pilates','stretch','2023-04-08 19:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',9);

INSERT INTO session VALUES(100,101,'practice','2023-03-20 10:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(101,101,'stretch','2023-03-20 15:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(102,103,'dance','2023-03-20 18:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',60);
INSERT INTO session VALUES(103,101,'stretch','2023-03-21 09:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(104,103,'dance','2023-03-21 14:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(105,101,'bicycle','2023-03-22 07:00:00','equipment district','bicycle dance',80);
INSERT INTO session VALUES(106,103,'dance','2023-03-22 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(107,101,'practice','2023-03-23 09:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(108,103,'stretch','2023-03-24 10:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(109,101,'dance','2023-03-24 14:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',80);
INSERT INTO session VALUES(110,103,'stretch','2023-03-25 11:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(111,101,'dance','2023-03-25 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);
INSERT INTO session VALUES(112,103,'bicycle','2023-03-26 10:00:00','equipment district','bicycle dance',60);
INSERT INTO session VALUES(113,101,'dance','2023-03-26 17:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);

INSERT INTO session VALUES(114,101,'practice','2023-03-27 10:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(115,101,'stretch','2023-03-27 15:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(116,103,'dance','2023-03-27 18:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',60);
INSERT INTO session VALUES(117,101,'stretch','2023-03-28 09:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(118,103,'dance','2023-03-28 14:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(119,101,'bicycle','2023-03-29 07:00:00','equipment district','bicycle dance',80);
INSERT INTO session VALUES(120,103,'dance','2023-03-29 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(121,101,'practice','2023-03-30 09:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(122,103,'stretch','2023-03-31 10:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(123,101,'dance','2023-03-31 14:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',80);
INSERT INTO session VALUES(124,103,'stretch','2023-04-01 11:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(125,101,'dance','2023-04-01 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);
INSERT INTO session VALUES(126,103,'bicycle','2023-04-02 10:00:00','equipment district','bicycle dance',60);
INSERT INTO session VALUES(127,101,'dance','2023-04-02 17:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);

INSERT INTO session VALUES(128,101,'practice','2023-04-03 10:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(129,101,'stretch','2023-04-03 15:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(130,103,'dance','2023-04-03 18:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',60);
INSERT INTO session VALUES(131,101,'stretch','2023-04-04 09:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',80);
INSERT INTO session VALUES(132,103,'dance','2023-04-04 14:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(133,101,'bicycle','2023-04-05 07:00:00','equipment district','bicycle dance',80);
INSERT INTO session VALUES(134,103,'dance','2023-04-05 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',60);
INSERT INTO session VALUES(135,101,'practice','2023-04-06 09:00:00','hall one','BODYPUMP is a fast-paced, barbell-based workout thats specifically designed to help you get lean, toned and fit',80);
INSERT INTO session VALUES(136,103,'stretch','2023-04-07 10:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(137,101,'dance','2023-04-07 14:00:00','hall one',' Zumba is a fitness program that involves cardio and Latin-inspired dance.',80);
INSERT INTO session VALUES(138,103,'stretch','2023-04-08 11:00:00','hall one',' is a group of physical, mental, and spiritual practices or disciplines which originated in ancient India',60);
INSERT INTO session VALUES(139,101,'dance','2023-04-08 16:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);
INSERT INTO session VALUES(140,103,'bicycle','2023-04-09 10:00:00','equipment district','bicycle dance',60);
INSERT INTO session VALUES(141,101,'dance','2023-04-09 17:00:00','hall one',' Pilates  is a type of mind-body exercise developed in the early 20th century by German physical trainer Joseph Pilates,.',80);

INSERT INTO payment VALUES(200,'lixiaowei',1,'2023-01-01',0,'success',240,100,101);
INSERT INTO payment VALUES(201,'ericli',1,'2023-01-10',0,'success',240,101,101);
INSERT INTO payment VALUES(202,'faysong',1,'2023-01-12',0,'success',240,102,101);
INSERT INTO payment VALUES(203,'faysong',2,'2023-01-15',0,'success',60,102,103);
INSERT INTO payment VALUES(204,'lixiaowei',2,'2023-02-12',0,'success',80,100,101);
INSERT INTO payment VALUES(205,'lixiaowei',2,'2023-02-20',0,'success',80,100,101);
INSERT INTO payment VALUES(206,'ericli',2,'2023-02-27',0,'success',60,101,103);
INSERT INTO payment VALUES(207,'ericli',2,'2023-03-02',0,'success',60,101,103);
INSERT INTO payment VALUES(208,'faysong',2,'2023-03-05',0,'success',60,102,103);
INSERT INTO payment VALUES(209,'ericli',2,'2023-03-11',0,'success',60,101,103);
INSERT INTO payment VALUES(210,'faysong',2,'2023-03-22',0,'success',60,102,103);

INSERT INTO subscription VALUES(200,100, 240,200,'2023-01-01','2023-12-31',1);
INSERT INTO subscription VALUES(201,101, 240,201,'2023-01-10','2024-01-09',1);
INSERT INTO subscription VALUES(202,102, 240,202,'2023-01-12','2024-01-11',1);

INSERT INTO classbooking VALUES(100,100, 100,101,'2023-01-01',1,0);
INSERT INTO classbooking VALUES(101,101, 101,101,'2023-01-11',1,0);
INSERT INTO classbooking VALUES(102,102, 101,101,'2023-01-12',1,0);
INSERT INTO classbooking VALUES(103,102, 102,103,'2023-01-15',1,0);
INSERT INTO classbooking VALUES(104,100, 110,103,'2023-01-30',1,0);
INSERT INTO classbooking VALUES(105,100, 118,101,'2023-02-02',1,0);
INSERT INTO classbooking VALUES(106,101, 118,103,'2023-02-03',1,0);
INSERT INTO classbooking VALUES(107,100, 128,103,'2023-02-25',1,0);
INSERT INTO classbooking VALUES(108,102, 128,103,'2023-02-25',1,0);
INSERT INTO classbooking VALUES(109,101, 129,103,'2023-03-02',1,0);
INSERT INTO classbooking VALUES(110,100, 132,103,'2023-03-05',1,0);
INSERT INTO classbooking VALUES(111,101, 132,103,'2023-03-06',1,0);
INSERT INTO classbooking VALUES(112,102, 138,103,'2023-03-16',1,0);
INSERT INTO classbooking VALUES(113,102, 140,101,'2023-03-21',1,0);
INSERT INTO classbooking VALUES(114,100, 140,101,'2023-03-21',1,0);

INSERT INTO sessionbooking VALUES(100,100,100,204,101,'2023-02-12',1,0);
INSERT INTO sessionbooking VALUES(101,100,101,205,101,'2023-02-20',1,0);
INSERT INTO sessionbooking VALUES(102,101,106,206,103,'2023-02-27',1,0);
INSERT INTO sessionbooking VALUES(103,101,126,207,103,'2023-03-02',1,0);
INSERT INTO sessionbooking VALUES(104,102,132,208,103,'2023-03-05',1,0);
INSERT INTO sessionbooking VALUES(105,101,135,209,103,'2023-03-11',1,0);
INSERT INTO sessionbooking VALUES(106,102,138,210,103,'2023-03-22',1,0);

INSERT INTO attendance VALUES ('300', '100', '2023-01-03 08:17:09');
INSERT INTO attendance VALUES ('301', '100', '2023-01-05 06:12:20');
INSERT INTO attendance VALUES ('302', '100', '2023-01-06 13:23:00');
INSERT INTO attendance VALUES ('303', '100', '2023-01-07 08:30:34');
INSERT INTO attendance VALUES ('304', '101', '2023-01-11 09:24:30');
INSERT INTO attendance VALUES ('305', '100', '2023-01-15 17:12:35');
INSERT INTO attendance VALUES ('306', '101', '2023-01-17 17:40:12');
INSERT INTO attendance VALUES ('307', '101', '2023-01-20 18:25:40');
INSERT INTO attendance VALUES ('308', '102', '2023-01-28 19:12:45');
INSERT INTO attendance VALUES ('309', '102', '2023-02-27 15:34:12');
INSERT INTO attendance VALUES ('310', '102', '2023-03-18 18:10:14');