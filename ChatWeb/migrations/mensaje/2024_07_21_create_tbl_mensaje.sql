-- ! ================================================================================================================================================
-- !                                                   SQL PARA CREAR TABLA MENSAJE 
-- ! ================================================================================================================================================
-- @author Ramón Dario Rozo Torres (23 de Noviembre de 2024)
-- @lastModified Ramón Dario Rozo Torres (30 de Julio de 2024)
-- @version 1.0.0
-- backend/v1/migrations/operacion/whatsapp/mensaje/2024_07_21_create_tbl_mensaje.sql

-- ! ELIMINAR TABLA SI EXISTE
DROP TABLE IF EXISTS `tbl_mensaje`;

-- ! CREAR TABLA BAJO LAS SIGUIENTES ESPECIFICACIONES
CREATE TABLE `tbl_mensaje` (
  `PK_MES_NCODE` int NOT NULL AUTO_INCREMENT,
  `FK_GES_CODIGO` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_ACCOUNT_SID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_API_VERSION` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_BODY` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_FROM` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_TO` varchar(100) COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_CHANNEL` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_MEDIA_TYPE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_MEDIA_URL` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `MES_MESSAGE_ID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_NUM_MEDIA` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_NUM_SEGMENTS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_PROFILE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_REFFAL_NUM_MEDIA` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_SMS_MESSAGE_SID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_SMS_SID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_SMS_STATUS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_WAID` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_CREATION_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `MES_LAST_MODIFICATION_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MES_DATE_SENT__MESSAGE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_DATE_CREATED_MESSAGE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_DATE_UPDATED_MESSAGE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_DATE_DELIVERED` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_DATE_READ` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `MES_USER` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_MESSAGE_SHOW` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_TIPO_GESTION` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_IDSOUL_CONVERSACION` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_IDSOUL_CAMPANA` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_IDRRHH` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_ESTADO_ENVIO_SOUL` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  `MES_MSG_ENVIO` varchar(550) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`PK_MES_NCODE`)
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


