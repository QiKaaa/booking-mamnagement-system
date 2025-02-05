CREATE DATABASE  IF NOT EXISTS `papermanagment` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `papermanagment`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: papermanagment
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `gno` int(8) unsigned zerofill NOT NULL,
  `gna` varchar(45) NOT NULL,
  `gte` varchar(45) NOT NULL,
  `gad` varchar(100) NOT NULL,
  `gpo` varchar(45) NOT NULL,
  PRIMARY KEY (`gno`),
  KEY `gna_gte` (`gna`,`gte`),
  CONSTRAINT `chk_gpo_length` CHECK ((length(`gpo`) = 6)),
  CONSTRAINT `chk_gte_length` CHECK ((length(`gte`) = 11)),
  CONSTRAINT `chk_gte_number` CHECK ((not(regexp_like(`gte`,_utf8mb3'[^0-9]'))))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (00000001,'张三','11111111111','广州市新港西路135号','510000'),(00000002,'李四','12345678901','广州市新港西路135号','510000'),(00000003,'胡图图','13599110000','翻斗大街翻斗花园二号楼1001室','510000');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `oid` int(8) unsigned zerofill NOT NULL,
  `onum` int unsigned NOT NULL,
  `pno` int(6) unsigned zerofill DEFAULT NULL,
  `gno` int(8) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`oid`),
  KEY `fk_orders_paper_idx` (`pno`),
  KEY `fk_orders_customer1_idx` (`gno`),
  CONSTRAINT `fk_orders_customer1` FOREIGN KEY (`gno`) REFERENCES `customer` (`gno`) ON DELETE CASCADE ON UPDATE SET NULL,
  CONSTRAINT `fk_orders_paper` FOREIGN KEY (`pno`) REFERENCES `paper` (`pno`) ON DELETE CASCADE ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (00000001,1,000001,00000002),(00000002,1,000004,00000002),(00000003,1,000001,00000003),(00000004,1,000002,00000003),(00000005,1,000004,00000003);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper`
--

DROP TABLE IF EXISTS `paper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paper` (
  `pno` int(6) unsigned zerofill NOT NULL,
  `pna` varchar(45) NOT NULL,
  `ppr` float unsigned NOT NULL,
  `psi` int unsigned NOT NULL,
  `pdw` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper`
--

LOCK TABLES `paper` WRITE;
/*!40000 ALTER TABLE `paper` DISABLE KEYS */;
INSERT INTO `paper` VALUES (000001,'人民日报',12.5,4,'人民日报出版社'),(000002,'解放军报',14.5,4,'解放军报社'),(000003,'光明日报',10.5,4,'光明日报出版社'),(000004,'青年报',11.5,4,'青年报社'),(000005,'扬子晚报',18.5,4,'中共江苏省委直属事业单位新华日报社'),(000006,'广州日报',12.5,4,'广州日报出版社');
/*!40000 ALTER TABLE `paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `uid` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `admin` enum('0','1','2') NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('aaaa','aaaaa','1'),('admin','123456','1'),('superadmin','123456','2'),('user','123456','0');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-08  4:38:29
