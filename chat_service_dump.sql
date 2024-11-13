-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: chat_service
-- ------------------------------------------------------
-- Server version	9.1.0

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
-- Table structure for table `group_messages`
--

DROP TABLE IF EXISTS `group_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_id` int NOT NULL,
  `sender_id` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `group_messages_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `group_rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_messages`
--

LOCK TABLES `group_messages` WRITE;
/*!40000 ALTER TABLE `group_messages` DISABLE KEYS */;
INSERT INTO `group_messages` VALUES (1,3,'hantalk','안녕','2024-11-12 19:58:05'),(2,3,'hantalk','안녕','2024-11-12 20:00:05');
/*!40000 ALTER TABLE `group_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_rooms`
--

DROP TABLE IF EXISTS `group_rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_rooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_name` (`room_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_rooms`
--

LOCK TABLES `group_rooms` WRITE;
/*!40000 ALTER TABLE `group_rooms` DISABLE KEYS */;
INSERT INTO `group_rooms` VALUES (1,'데이터통신','2024-11-12 19:08:05'),(2,'알고리즘','2024-11-12 19:08:05'),(3,'객체지향언어','2024-11-12 19:08:05'),(4,'자료구조','2024-11-12 19:08:05'),(5,'프로그래밍언어','2024-11-12 19:08:05'),(6,'오픈소스','2024-11-12 19:08:05');
/*!40000 ALTER TABLE `group_rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room` varchar(255) DEFAULT NULL,
  `sender_id` varchar(255) DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'your_room_id','hantalk','안녕하세요','2024-11-12 16:38:41'),(2,'your_room_id','hantalk','안녕하세요','2024-11-12 16:38:47'),(3,'your_room_id','hantalk','안녕하세요','2024-11-12 16:40:38'),(4,'your_room_id','hantalk','안녕하세요','2024-11-12 16:41:13'),(5,'your_room_id','hantalk','안녕하세요','2024-11-12 16:41:28'),(6,'your_room_id','hantalk','안녕하세요','2024-11-12 16:43:54'),(7,'your_room_id','hantalk','안녕하세요','2024-11-12 16:44:05'),(8,'hansung1','hantalk','안녕하세요','2024-11-12 16:44:22'),(9,'hansung1','hantalk','hi','2024-11-12 16:45:51'),(10,'hansung1','hantalk','안녕하세요','2024-11-12 17:18:41'),(11,'hansung1','hantalk','안녕하세요','2024-11-12 17:21:19'),(12,'hansung1','hantalk','안녕','2024-11-12 17:23:26'),(13,'hansung1','hantalk','안녕하세요','2024-11-12 17:24:09'),(14,'hansung1','hantalk','안녕하세요','2024-11-12 17:27:33'),(15,'hansung1','hantalk','안녕하세요','2024-11-12 17:27:54'),(16,'hansung1','hantalk','안녕하세요','2024-11-12 17:30:45'),(17,'hansung1','hantalk','안녕','2024-11-12 17:38:37'),(18,'hansung1','hantalk','안녕','2024-11-12 17:43:06'),(19,'hansung1','hantalk','안녕','2024-11-12 17:43:11'),(20,'hansung1','hantalk','안녕','2024-11-12 17:43:33'),(21,'hansung1','hantalk','안녕','2024-11-12 17:47:55'),(22,'hansung1','hantalk','안녕','2024-11-12 17:49:27'),(23,'hansung1','hantalk','안녕','2024-11-12 17:50:39'),(24,'hansung1','hantalk2','안녕','2024-11-12 17:52:07'),(25,'hansung1','hantalk','반가워','2024-11-12 17:52:12'),(26,'hansung1','hantalk','나도','2024-11-12 17:52:17'),(27,'hansung1','hantalk2','우리 뭐해?','2024-11-12 17:52:23'),(28,'hansung1','hantalk2','안녕','2024-11-12 18:01:16'),(29,'hansung1','hantalk2','안녕','2024-11-12 18:01:21'),(30,'hansung1','hantalk2','안녕','2024-11-12 18:01:27'),(31,'hansung1','hantalk','안녕','2024-11-12 18:02:08'),(32,'hansung1','hantalk2','안녕','2024-11-12 18:02:13'),(33,'hansung1','hantalk','안녕','2024-11-12 18:02:26'),(34,'hansung1','hantalk','안녕','2024-11-12 18:02:31'),(35,'hansung1','hantalk2','안녕','2024-11-12 18:04:03'),(36,'hansung1','hantalk','안녕','2024-11-12 18:04:07'),(37,'hansung1','hantalk','너 뭐해?','2024-11-12 18:04:16'),(38,'hansung1','hantalk2','나 밥먹어','2024-11-12 18:04:20'),(39,'hansung1','hantalk','안녕','2024-11-12 18:08:26'),(40,'hansung1','hantalk','안녕','2024-11-12 18:10:44'),(41,'{{ room }}','hantalk','안녕','2024-11-12 18:12:42'),(42,'{{ room }}','hantalk','안녕','2024-11-12 18:14:27'),(43,'hansung1','hantalk','한성','2024-11-12 18:18:41'),(44,'hansung1','hantalk','안녕','2024-11-12 18:20:27'),(45,'hansung1','hantalk','안녕','2024-11-12 18:24:12'),(46,'hansung1','hantalk','안녕하세요','2024-11-12 18:30:30'),(47,'hansung1','hantalk','안녕','2024-11-12 18:31:46');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `student_id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'한톡','1111','hantalk','$2b$12$0HSGUQteIeA8MJbAet28tOFLJ52.Zz871ILlbNexlogjH0DwMMETG','2024-11-12 15:21:59'),(2,'한톡2','22222','hantalk2','$2b$12$JRqeEMNu0erC5kkUagq9l.N6.4xS6uHJjr22m8j1g4rCiT/1iCIAC','2024-11-12 17:51:47');
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

-- Dump completed on 2024-11-13 14:38:51
