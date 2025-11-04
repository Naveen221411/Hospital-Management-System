/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.22-MariaDB : Database - lightweightpolicy
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`lightweightpolicy` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `lightweightpolicy`;

/*Table structure for table `appointments` */
DROP TABLE IF EXISTS `appointments`;

CREATE TABLE `appointments` (
  `id` int(200) NOT NULL AUTO_INCREMENT,
  `doctor` varchar(100) DEFAULT NULL,
  `patientemail` varchar(100) DEFAULT NULL,
  `status1` varchar(100) DEFAULT 'pending',
  `status2` varchar(100) DEFAULT 'pending',
  `appointmentdate` varchar(100) DEFAULT NULL,
  `timining` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `docreg` */

DROP TABLE IF EXISTS `docreg`;

CREATE TABLE `docreg` (
  `slno` int(100) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) DEFAULT NULL,
  `Department` varchar(100) DEFAULT NULL,
  `Age` varchar(100) DEFAULT NULL,
  `Number` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Experience` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  `profile` varchar(250) DEFAULT NULL,
  UNIQUE KEY `slno` (`slno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Table structure for table `patient_reg` */

DROP TABLE IF EXISTS `patient_reg`;

CREATE TABLE `patient_reg` (
  `ID` int(200) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;



/*Table structure for table `reports` */

DROP TABLE IF EXISTS `reports`;

CREATE TABLE `reports` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `FileName` varchar(200) DEFAULT NULL,
  `FileData` longblob DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `Status` varchar(200) DEFAULT NULL,
  `Key1` varchar(100) DEFAULT NULL,
  `appointmentid` varchar(100) DEFAULT NULL,
  `doctoremail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `reviews` */

DROP TABLE IF EXISTS `reviews`;

CREATE TABLE `reviews` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `myreview` text DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `contactus`;

CREATE TABLE `contactus` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `Name` varchar(200) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
