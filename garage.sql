-- MySQL dump 10.13  Distrib 5.7.14, for Win64 (x86_64)
--
-- Host: localhost    Database: carhire
-- ------------------------------------------------------
-- Server version	5.7.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS `garage`;
CREATE DATABASE `garage`;
USE `garage`;


--
-- Table structure for table `manufacturer`
--

DROP TABLE IF EXISTS `manufacturer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manufacturer` (
  `manu_code` varchar(3) NOT NULL,
  `manu_name` varchar(200) NOT NULL,
  `manu_details` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`manu_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturer`
--

LOCK TABLES `manufacturer` WRITE;
/*!40000 ALTER TABLE `manufacturer` DISABLE KEYS */;
INSERT INTO `manufacturer` VALUES ('FOR','Ford','The Ford Motor Company is an American multinational automaker headquartered in Dearborn, Michigan, a suburb of Detroit. It was founded in 1903'),('GM','General Motors','General Motors is an American multinational automaker headquartered in Detroit, Michigan. It was founded in 1908'),('NIS','Nissan','Nissan Motor Company Ltd is a Japanese multinational automobile manufacturer headquartered in Nishi-ku, Yokohama, Japan. It was founded in 1934'),('TOY','Toyota','Toyota Motor Corporation is a Japanese automotive manufacturer headquartered in Toyota, Aichi, Japan. It was founded in 1937'),('VOL','Volkswagen','Volkswagen is a German automaker headquartered in Wolfsburg, Germany. It was founded in 1937');
/*!40000 ALTER TABLE `manufacturer` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle` (
  `reg` varchar(20) NOT NULL,
  `manu_code` varchar(3) NOT NULL,
  `mileage` int(11) DEFAULT NULL,
  `price` decimal(8,2) NOT NULL,
  `colour` varchar(20) NOT NULL,
  `fuel` ENUM('petrol', 'diesel'),
  PRIMARY KEY (`reg`),
  CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`manu_code`) REFERENCES `manufacturer` (`manu_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES ('2003-LM-201','TOY',170000,3500.50,'Red','petrol'),('2010-G-13345','TOY',50000,8599,'Silver','petrol'),('2014-WH-2189','FOR',12553,11000,'Blue','diesel'),('2016-D-12345','TOY',3456,15000,'Red','petrol'),('2011-G-995','FOR',33500,8500,'Blue','petrol'),('2011-WH-2121','FOR',55998,14000,'Black','diesel'),('2009-RN-12','FOR',98242,2500,'Red','petrol');
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-10 17:53:19
