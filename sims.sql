-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: sims
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Current Database: `sims`
--

/*!40000 DROP DATABASE IF EXISTS `sims`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `sims` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `sims`;

--
-- Table structure for table `delivery`
--

DROP TABLE IF EXISTS `delivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery` (
  `DeliveryID` int NOT NULL AUTO_INCREMENT,
  `ItemID` varchar(16) NOT NULL,
  `DeliveryQuantity` int NOT NULL,
  `DeliveryDate` date NOT NULL DEFAULT (curdate()),
  `ReceivedBy` varchar(30) NOT NULL,
  PRIMARY KEY (`DeliveryID`),
  KEY `DeliveryItem` (`ItemID`),
  KEY `ReceivedBy` (`ReceivedBy`),
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`ReceivedBy`) REFERENCES `user` (`Username`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `expiration`
--

DROP TABLE IF EXISTS `expiration`;
/*!50001 DROP VIEW IF EXISTS `expiration`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `expiration` AS SELECT 
 1 AS `DeliveryID`,
 1 AS `DeliveryDate`,
 1 AS `ExpirationDate`,
 1 AS `IsExpired`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `ItemID` varchar(16) NOT NULL,
  `ItemName` varchar(20) NOT NULL,
  `ItemDescription` varchar(100) NOT NULL,
  `ShelfLife` int DEFAULT NULL,
  `Price` decimal(18,2) NOT NULL,
  `Unit` varchar(20) NOT NULL DEFAULT 'units',
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `RequestID` int NOT NULL AUTO_INCREMENT,
  `ItemID` varchar(16) NOT NULL,
  `RequestedBy` varchar(30) NOT NULL,
  `RequestQuantity` int NOT NULL,
  `RequestDate` date NOT NULL DEFAULT (curdate()),
  `Status` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`RequestID`),
  KEY `ItemCode` (`ItemID`),
  KEY `RequestedBy` (`RequestedBy`),
  KEY `Status` (`Status`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`RequestedBy`) REFERENCES `user` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_3` FOREIGN KEY (`Status`) REFERENCES `request_status` (`StatusID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `request_status`
--

DROP TABLE IF EXISTS `request_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_status` (
  `StatusID` int NOT NULL,
  `StatusName` varchar(10) NOT NULL,
  PRIMARY KEY (`StatusID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `RoleID` int NOT NULL,
  `RoleName` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `stock`
--

DROP TABLE IF EXISTS `stock`;
/*!50001 DROP VIEW IF EXISTS `stock`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `stock` AS SELECT 
 1 AS `ItemID`,
 1 AS `ItemName`,
 1 AS `ItemDescription`,
 1 AS `ShelfLife`,
 1 AS `Price`,
 1 AS `AvailableStock`,
 1 AS `Unit`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `Username` varchar(30) NOT NULL,
  `Password` varchar(64) NOT NULL,
  `FirstName` varchar(30) NOT NULL,
  `LastName` varchar(30) NOT NULL,
  `Email` varchar(64) NOT NULL,
  `RoleID` int NOT NULL,
  PRIMARY KEY (`Username`),
  KEY `RoleID` (`RoleID`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`RoleID`) REFERENCES `role` (`RoleID`),
  CONSTRAINT `user_chk_1` CHECK (regexp_like(`Email`,_utf8mb4'^([0-9a-z]|([0-9a-z][\\.\\-_]{1}[0-9a-z]))+@([0-9a-z\\-]+\\.)+[a-z]{2,}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Current Database: `sims`
--

USE `sims`;

--
-- Final view structure for view `expiration`
--

/*!50001 DROP VIEW IF EXISTS `expiration`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `expiration` AS select `delivery`.`DeliveryID` AS `DeliveryID`,`delivery`.`DeliveryDate` AS `DeliveryDate`,(`delivery`.`DeliveryDate` + interval `item`.`ShelfLife` day) AS `ExpirationDate`,coalesce(((to_days(curdate()) - to_days((`delivery`.`DeliveryDate` + interval `item`.`ShelfLife` day))) > 0),0) AS `IsExpired` from (`delivery` join `item` on((`delivery`.`ItemID` = `item`.`ItemID`))) order by `delivery`.`DeliveryID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `stock`
--

/*!50001 DROP VIEW IF EXISTS `stock`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `stock` AS select `item`.`ItemID` AS `ItemID`,`item`.`ItemName` AS `ItemName`,`item`.`ItemDescription` AS `ItemDescription`,`item`.`ShelfLife` AS `ShelfLife`,`item`.`Price` AS `Price`,coalesce(sum(if(`expiration`.`IsExpired`,0,`delivery`.`DeliveryQuantity`)),0) AS `AvailableStock`,`item`.`Unit` AS `Unit` from (`item` left join (`delivery` join `expiration` on((`delivery`.`DeliveryID` = `expiration`.`DeliveryID`))) on((`item`.`ItemID` = `delivery`.`ItemID`))) group by `item`.`ItemID` order by `item`.`ItemID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-23 20:32:46
