-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: django_muestras
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Investigadores'),(1,'Técnicos de laboratorio');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (2,1,25),(3,1,26),(4,1,27),(5,1,28),(6,1,29),(7,1,30),(8,1,31),(1,1,32),(9,2,28),(10,2,29);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add muestra',7,'add_muestra'),(26,'Can change muestra',7,'change_muestra'),(27,'Can delete muestra',7,'delete_muestra'),(28,'Can view muestra',7,'view_muestra'),(29,'Puede ver muestras en la web',7,'can_view_muestras_web'),(30,'Puede añadir muestras en la web',7,'can_add_muestras_web'),(31,'Puede cambiar muestras en la web',7,'can_change_muestras_web'),(32,'Puede eliminar muestras en la web',7,'can_delete_muestras_web'),(33,'Can add localizacion',8,'add_localizacion'),(34,'Can change localizacion',8,'change_localizacion'),(35,'Can delete localizacion',8,'delete_localizacion'),(36,'Can view localizacion',8,'view_localizacion'),(37,'Can add estudio',9,'add_estudio'),(38,'Can change estudio',9,'change_estudio'),(39,'Can delete estudio',9,'delete_estudio'),(40,'Can view estudio',9,'view_estudio'),(41,'Can add envio',10,'add_envio'),(42,'Can change envio',10,'change_envio'),(43,'Can delete envio',10,'delete_envio'),(44,'Can view envio',10,'view_envio');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$gpoSpTRR0Od7Ulxe805chC$/yVq9nTxVEQ1evAhC517N3LW8gk7MKubW6XsRWiSipo=','2025-10-17 09:28:12.628685',1,'admin','','','',1,1,'2025-10-08 17:19:43.698095'),(2,'pbkdf2_sha256$1000000$0WDqgXLNBTaXnKpY7ASTZH$boFQx8S3OmXRstR1Cz+c0RQ2XiCNaLe+aicFDHzwjs8=','2025-10-17 09:30:36.738404',0,'Técnico','','','',0,1,'2025-10-08 17:20:53.000000'),(3,'pbkdf2_sha256$1000000$9ObUrSeq9X8tp0I9i0ADVm$GvZ/sIxxO1IPMrzNUzpX+hYzPD16ra8rqn4/9rK2PHM=','2025-10-17 09:09:34.643556',0,'Investigador','','','',0,1,'2025-10-15 11:54:31.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(2,3,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-08 17:20:39.476332','1','Técnicos de laboratorio',1,'[{\"added\": {}}]',3,1),(2,'2025-10-08 17:20:53.582427','2','Técnico',1,'[{\"added\": {}}]',4,1),(3,'2025-10-08 17:20:58.395675','2','Técnico',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(4,'2025-10-08 17:22:04.549462','1','1 - 1 - 1 - 1 - 1 - 1 - 1',1,'[{\"added\": {}}]',8,1),(5,'2025-10-09 15:46:55.750183','4','1 - 1 - 2 - 1 - 1 - 1 - 1',3,'',8,1),(6,'2025-10-15 11:54:31.727237','3','Investigador',1,'[{\"added\": {}}]',4,1),(7,'2025-10-15 11:54:41.939642','3','Investigador',2,'[]',4,1),(8,'2025-10-15 11:55:05.767789','2','Investigadores',1,'[{\"added\": {}}]',3,1),(9,'2025-10-15 11:55:14.588857','3','Investigador',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(10,'muestras','envio'),(9,'muestras','estudio'),(8,'muestras','localizacion'),(7,'muestras','muestra'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-08 17:14:53.601041'),(2,'auth','0001_initial','2025-10-08 17:14:54.077485'),(3,'admin','0001_initial','2025-10-08 17:14:54.195614'),(4,'admin','0002_logentry_remove_auto_add','2025-10-08 17:14:54.201122'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-08 17:14:54.206488'),(6,'contenttypes','0002_remove_content_type_name','2025-10-08 17:14:54.308777'),(7,'auth','0002_alter_permission_name_max_length','2025-10-08 17:14:54.362063'),(8,'auth','0003_alter_user_email_max_length','2025-10-08 17:14:54.377868'),(9,'auth','0004_alter_user_username_opts','2025-10-08 17:14:54.383393'),(10,'auth','0005_alter_user_last_login_null','2025-10-08 17:14:54.476467'),(11,'auth','0006_require_contenttypes_0002','2025-10-08 17:14:54.482310'),(12,'auth','0007_alter_validators_add_error_messages','2025-10-08 17:14:54.491993'),(13,'auth','0008_alter_user_username_max_length','2025-10-08 17:14:54.581782'),(14,'auth','0009_alter_user_last_name_max_length','2025-10-08 17:14:54.636358'),(15,'auth','0010_alter_group_name_max_length','2025-10-08 17:14:54.650873'),(16,'auth','0011_update_proxy_permissions','2025-10-08 17:14:54.658418'),(17,'auth','0012_alter_user_first_name_max_length','2025-10-08 17:14:54.708151'),(18,'sessions','0001_initial','2025-10-08 17:14:54.737166'),(23,'muestras','0001_initial','2025-10-09 15:23:23.010639'),(24,'muestras','0002_alter_localizacion_muestra','2025-10-09 15:35:04.149161'),(25,'muestras','0003_alter_localizacion_muestra','2025-10-09 15:38:55.843764'),(26,'muestras','0004_alter_localizacion_unique_together','2025-10-09 15:47:08.477949'),(27,'muestras','0005_alter_localizacion_muestra','2025-10-09 15:50:38.902863'),(28,'muestras','0006_alter_localizacion_muestra','2025-10-09 15:51:05.114755');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('i2v5oq1upuyzr5pjsfpqqv1ss2y924k9','.eJxVjEEOwiAQRe_C2pCh0Aou3XsGMjNMpWogKe3KeHdD0oVu_3vvv1XEfctxb7LGJamLGtTpdyPkp5QO0gPLvWquZVsX0l3RB236VpO8rof7d5Cx5V4H9DMwBvaCdrLiAIzxowsuMfpkaYIzEXs3IM1hNAAUXABLjIYF1OcL75w4Gg:1v923p:Zs8alGXFstObTRcMJOQD8riqneIlzOptgCWEX0v2E3A','2025-10-29 14:01:01.658055'),('u72j1lgy6y7uuuezoab04jwplrn5wepf','.eJxVjEEOwiAQRe_C2pCh0Aou3XsGMjNMpWogKe3KeHdD0oVu_3vvv1XEfctxb7LGJamLGtTpdyPkp5QO0gPLvWquZVsX0l3RB236VpO8rof7d5Cx5V4H9DMwBvaCdrLiAIzxowsuMfpkaYIzEXs3IM1hNAAUXABLjIYF1OcL75w4Gg:1v9gnE:voIMuJZbrPotBvg2GwDXWRFTQqGhbDUMH2WS4gkQT8g','2025-10-31 09:30:36.741077');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muestras_envio`
--

DROP TABLE IF EXISTS `muestras_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muestras_envio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `volumen_enviado` double NOT NULL,
  `unidad_volumen_enviado` varchar(15) NOT NULL,
  `concentracion_enviada` double NOT NULL,
  `unidad_concentracion_enviada` varchar(15) NOT NULL,
  `centro_destino` varchar(100) NOT NULL,
  `lugar_destino` varchar(100) NOT NULL,
  `muestra_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `muestras_envio_muestra_id_b6b53308_fk_muestras_muestra_id` (`muestra_id`),
  CONSTRAINT `muestras_envio_muestra_id_b6b53308_fk_muestras_muestra_id` FOREIGN KEY (`muestra_id`) REFERENCES `muestras_muestra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestras_envio`
--

LOCK TABLES `muestras_envio` WRITE;
/*!40000 ALTER TABLE `muestras_envio` DISABLE KEYS */;
/*!40000 ALTER TABLE `muestras_envio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muestras_estudio`
--

DROP TABLE IF EXISTS `muestras_estudio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muestras_estudio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_estudio` varchar(20) NOT NULL,
  `referencia_estudio` varchar(100) NOT NULL,
  `nombre_estudio` varchar(100) NOT NULL,
  `descripcion_estudio` longtext,
  `fecha_inicio_estudio` date NOT NULL,
  `fecha_fin_estudio` date DEFAULT NULL,
  `investigador_principal` varchar(100) NOT NULL,
  `muestra_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `muestras_estudio_muestra_id_53f4d5f9_fk_muestras_muestra_id` (`muestra_id`),
  CONSTRAINT `muestras_estudio_muestra_id_53f4d5f9_fk_muestras_muestra_id` FOREIGN KEY (`muestra_id`) REFERENCES `muestras_muestra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestras_estudio`
--

LOCK TABLES `muestras_estudio` WRITE;
/*!40000 ALTER TABLE `muestras_estudio` DISABLE KEYS */;
/*!40000 ALTER TABLE `muestras_estudio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muestras_localizacion`
--

DROP TABLE IF EXISTS `muestras_localizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muestras_localizacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `congelador` varchar(50) NOT NULL,
  `estante` varchar(50) NOT NULL,
  `posicion_rack_estante` varchar(50) NOT NULL,
  `rack` varchar(50) NOT NULL,
  `posicion_caja_rack` varchar(50) NOT NULL,
  `caja` varchar(50) NOT NULL,
  `subposicion` varchar(50) NOT NULL,
  `muestra_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `muestras_localizacion_congelador_estante_posic_9d409fd8_uniq` (`congelador`,`estante`,`posicion_rack_estante`,`rack`,`posicion_caja_rack`,`caja`,`subposicion`),
  KEY `muestras_localizacion_muestra_id_678e6fa0` (`muestra_id`),
  CONSTRAINT `muestras_localizacio_muestra_id_678e6fa0_fk_muestras_` FOREIGN KEY (`muestra_id`) REFERENCES `muestras_muestra` (`nom_lab`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestras_localizacion`
--

LOCK TABLES `muestras_localizacion` WRITE;
/*!40000 ALTER TABLE `muestras_localizacion` DISABLE KEYS */;
INSERT INTO `muestras_localizacion` VALUES (1,'1','1','2','1','1','1','1',NULL),(3,'1','2','1','1','1','1','1',NULL),(5,'2','2','2','2','2','2','2',NULL);
/*!40000 ALTER TABLE `muestras_localizacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muestras_muestra`
--

DROP TABLE IF EXISTS `muestras_muestra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muestras_muestra` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_individuo` varchar(20) NOT NULL,
  `nom_lab` varchar(100) NOT NULL,
  `id_material` varchar(20) NOT NULL,
  `volumen_actual` double NOT NULL,
  `unidad_volumen` varchar(15) NOT NULL,
  `concentracion_actual` double NOT NULL,
  `unidad_concentracion` varchar(15) NOT NULL,
  `masa_actual` double NOT NULL,
  `unidad_masa` varchar(15) NOT NULL,
  `fecha_extraccion` date NOT NULL,
  `fecha_llegada` date NOT NULL,
  `observaciones` longtext,
  `estado_inicial` varchar(50) NOT NULL,
  `centro_procedencia` varchar(100) NOT NULL,
  `lugar_procedencia` varchar(100) NOT NULL,
  `estado_actual` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom_lab` (`nom_lab`)
) ENGINE=InnoDB AUTO_INCREMENT=1047 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muestras_muestra`
--

LOCK TABLES `muestras_muestra` WRITE;
/*!40000 ALTER TABLE `muestras_muestra` DISABLE KEYS */;
INSERT INTO `muestras_muestra` VALUES (1011,'1','sample_1','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1012,'1','sample_2','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1013,'1','sample_3','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1014,'1','sample_4','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1015,'1','sample_5','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1016,'1','sample_6','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1017,'1','sample_7','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1018,'1','sample_8','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1019,'1','sample_9','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1020,'1','sample_10','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1021,'1','sample_11','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1022,'1','sample_12','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1023,'1','sample_13','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1024,'1','sample_14','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1025,'1','sample_15','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1026,'1','sample_16','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1027,'1','sample_17','cerebelo',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1028,'1','sample_18','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1029,'1','sample_19','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1030,'2','sample_20','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1031,'2','sample_21','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1032,'2','sample_22','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1033,'2','sample_23','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1034,'2','sample_24','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1035,'2','sample_25','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1036,'2','sample_26','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1037,'2','sample_27','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1038,'2','sample_28','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1039,'2','sample_29','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1040,'2','sample_30','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1041,'2','sample_31','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1042,'2','sample_32','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1043,'2','sample_33','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1044,'2','sample_34','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1045,'2','sample_35','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible'),(1046,'2','sample_36','corteza',3,'microlitros',4,'ng/ml',5,'mg','2025-09-18','2025-09-18','prueba','Congelado','Universidad Complutense','Madrid','Disponible');
/*!40000 ALTER TABLE `muestras_muestra` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-25 12:58:06
