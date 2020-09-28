-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: ethans1
-- ------------------------------------------------------
-- Server version	8.0.20-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `ethans1`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ethans1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `ethans1`;

--
-- Table structure for table `Client_Info`
--

DROP TABLE IF EXISTS `Client_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Client_Info` (
  `Client_ID` int NOT NULL,
  `Name` varchar(40) DEFAULT NULL,
  `Phone` varchar(10) DEFAULT NULL,
  `Email` varchar(40) DEFAULT NULL,
  `PAN` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`Client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Client_Info`
--

LOCK TABLES `Client_Info` WRITE;
/*!40000 ALTER TABLE `Client_Info` DISABLE KEYS */;
INSERT INTO `Client_Info` VALUES (1,'User_1','3473843439','User1@company.com','APKR09364'),(2,'User_2','3473843440','User_2@company.com','APKR09365'),(3,'User_3','3473843441','User_3@company.com','APKR09366'),(4,'User_4','3473843442','User_4@company.com','APKR09367'),(5,'User_5','3473843443','User_5@company.com','APKR09368'),(6,'User_6','3473843444','User_6@company.com','APKR09369'),(7,'User_7','3473843445','User_7@company.com','APKR09370'),(8,'User_8','3473843446','User_8@company.com','APKR09371'),(9,'User_9','3473843447','User_9@company.com','APKR09372'),(10,'User_10','3473843448','User_10@company.com','APKR09373');
/*!40000 ALTER TABLE `Client_Info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Exe_Info`
--

DROP TABLE IF EXISTS `Exe_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Exe_Info` (
  `Client_ID` int DEFAULT NULL,
  `Transaction_Date` datetime DEFAULT NULL,
  `Transaction` varchar(4) DEFAULT NULL,
  `Stock` varchar(40) DEFAULT NULL,
  `Stock_Symbol` varchar(15) DEFAULT NULL,
  `Market` varchar(2) DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `Buy_Price` float DEFAULT NULL,
  `Hit_Price` float DEFAULT NULL,
  `Sell_Price` float DEFAULT NULL,
  KEY `Client_ID` (`Client_ID`),
  CONSTRAINT `Exe_Info_ibfk_1` FOREIGN KEY (`Client_ID`) REFERENCES `Client_Info` (`Client_ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Exe_Info`
--

LOCK TABLES `Exe_Info` WRITE;
/*!40000 ALTER TABLE `Exe_Info` DISABLE KEYS */;
INSERT INTO `Exe_Info` VALUES (3,'2020-05-27 00:23:44','Buy','Wipro','WIPRO','NS',20,198.34,250,0),(8,'2020-06-02 02:23:44','Buy','HDFC Bank Limited','HDFCBANK','NS',15,1001.34,1320,0),(3,'2020-05-21 03:23:44','Buy','Asian Paints','ASIANPAINT','NS',10,1550.03,1730,0),(7,'2020-03-19 04:23:44','Buy','Tata Consultancy Services Limited','TCS','BO',13,1600,2350,0),(4,'2020-03-19 05:23:44','Buy','Infosys','INFY','BO',15,550,970,0),(3,'2020-03-13 06:23:44','Buy','Kotak Mahindra Mutual Fund','KTKSENSEX','BO',10,400,480,0),(2,'2020-04-21 07:23:44','Buy','Wipro','WIPRO','NS',25,180,300,0),(10,'2020-04-07 08:23:44','Buy','HCL Technologies Limited','HCLTECH','BO',15,450,700,0),(1,'2020-03-13 09:23:44','Buy','Tata Consultancy Services Limited','TCS','BO',15,1700.39,2000,0),(2,'2020-05-29 10:23:44','Buy','Asian Paints','ASIANPAINT','NS',5,1670.45,1950,0),(4,'2020-03-25 11:23:44','Buy','Nestle India Limited','NESTLEIND','NS',5,13000,18500,0),(6,'2020-06-12 12:23:44','Buy','Reliance Industries Limited','RELIANCE','BO',10,1500,2000,0),(5,'2020-04-15 13:23:44','Buy','Asian Paints','ASIANPAINT','NS',10,1700,2000,0),(2,'2020-07-14 14:23:44','Buy','HCL Technologies Limited','HCLTECH','BO',10,600,750,0),(4,'2020-06-12 15:23:44','Buy','Bharti Airtel Limited','BHARTIARTL','NS',15,550,660,0),(1,'2020-02-28 16:23:44','Buy','ICICI Bank Limited ','ICICIBANK','BO',20,500,600,0),(3,'2020-07-15 17:23:44','Sell','Wipro','WIPRO','NS',10,0,270,250),(5,'2020-03-24 18:23:44','Buy','Infosys','INFY','BO',12,600,960,0),(2,'2020-03-02 19:23:44','Buy','State Bank of India','SBIN','NS',10,300,360,0),(9,'2020-07-06 20:23:44','Buy','Bajaj Finance Limited','BAJFINANCE','BO',6,3000,4000,0),(3,'2020-03-20 21:23:44','Buy','Tata Consultancy Services Limited','TCS','BO',10,1640,2340,0),(1,'2020-04-30 22:23:44','Sell','Tata Consultancy Services Limited','TCS','BO',12,0,2100,2000),(3,'2020-07-21 23:23:44','Sell','Asian Paints','ASIANPAINT','NS',10,0,0,1730),(3,'2020-07-23 08:21:44','Buy','Wipro','WIPRO','NS',15,274,300,0),(3,'2020-07-21 10:21:44','Sell','Wipro','WIPRO','NS',5,0,300,274),(1,'2020-07-21 11:21:44','Buy','Axis Bank Limited ','AXISBANK','NS',25,442,700,0);
/*!40000 ALTER TABLE `Exe_Info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scrape_data`
--

DROP TABLE IF EXISTS `scrape_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scrape_data` (
  `index` bigint DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Stock_symbol` text,
  `Current price` text,
  `Previous close` text,
  `Open` text,
  `Close` text,
  `Low` text,
  `High` text,
  `52 Week Low` text,
  `52 Week High` text,
  `Volume` text,
  `Avg. volume` text,
  KEY `ix_scrape_data_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scrape_data`
--

LOCK TABLES `scrape_data` WRITE;
/*!40000 ALTER TABLE `scrape_data` DISABLE KEYS */;
INSERT INTO `scrape_data` VALUES (0,'2020-07-23','WIPRO.NS','266.60','266.00','268.30','266.60','262.55 ',' 268.45','159.40 ',' 281.60','10,365,440','11,455,128'),(1,'2020-07-23','HDFCBANK.NS','1,130.40','1,126.35','1,125.00','1,130.40','1,116.25 ',' 1,143.90','738.75 ',' 1,305.50','10,072,390','18,961,291'),(2,'2020-07-23','ASIANPAINT.NS','1,727.80','1,695.75','1,690.00','1,727.80','1,687.00 ',' 1,740.00','1,431.20 ',' 1,916.70','2,375,027','2,767,071'),(3,'2020-07-23','TCS.BO','2,170.75','2,189.95','2,190.00','2,170.75','2,162.45 ',' 2,191.00','1,504.40 ',' 2,332.00','63,185','193,746'),(4,'2020-07-23','INFY.BO','908.85','919.40','916.00','908.85','900.65 ',' 916.55','511.10 ',' 952.00','790,412','476,774'),(5,'2020-07-23','KTKSENSEX.BO','394.80','392.50','393.50','394.80','393.50 ',' 395.00','265.00 ',' 461.00','21','1,010'),(6,'2020-07-23','HCLTECH.BO','652.65','650.60','649.00','652.65','643.70 ',' 656.95','375.50 ',' 662.30','147,329','175,912'),(7,'2020-07-23','NESTLEIND.NS','17,256.40','17,151.85','17,120.00','17,256.40','17,050.00 ',' 17,298.95','11,322.50 ',' 18,369.90','106,917','168,331'),(8,'2020-07-23','RELIANCE.BO','2,060.65','2,004.10','2,004.10','2,060.65','1,991.10 ',' 2,078.90','875.70 ',' 2,078.90','1,379,049','1,022,357'),(9,'2020-07-23','BHARTIARTL.NS','567.20','569.15','570.00','567.20','564.00 ',' 575.75','321.15 ',' 612.00','9,534,906','20,614,781'),(10,'2020-07-23','ICICIBANK.BO','392.30','381.10','382.70','392.30','378.85 ',' 395.50','269.00 ',' 552.40','2,529,698','1,680,839'),(11,'2020-07-23','SBIN.NS','198.25','192.00','192.40','198.25','191.15 ',' 199.10','149.45 ',' 351.00','70,765,196','68,342,652'),(12,'2020-07-23','BAJFINANCE.BO','3,298.25','3,252.55','3,253.00','3,298.25','3,220.00 ',' 3,319.85','1,783.10 ',' 4,923.20','274,677','546,013'),(13,'2020-07-23','AXISBANK.NS','460.85','478.95','472.95','460.85','459.20 ',' 474.75','286.00 ',' 765.85','40,243,176','41,768,124');
/*!40000 ALTER TABLE `scrape_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-24 18:43:28
