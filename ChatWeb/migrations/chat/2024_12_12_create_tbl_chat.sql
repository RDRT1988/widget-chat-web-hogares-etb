-- ! ================================================================================================================================================
-- !                                                   SQL PARA CREAR TABLA CHAT
-- ! ================================================================================================================================================
-- @author Ramón Dario Rozo Torres (12 de Diciembre de 2024)
-- @lastModified Ramón Dario Rozo Torres (12 de Diciembre de 2024)
-- @version 1.0.0
-- ChatWeb/migrations/chat/2024_12_12_create_tbl_chat.sql

-- ! ELIMINAR TABLA SI EXISTE
DROP TABLE IF EXISTS `tbl_chat`;

-- ! CREAR TABLA BAJO LAS SIGUIENTES ESPECIFICACIONES
CREATE TABLE `tbl_chat` (
  `cht_id` int NOT NULL AUTO_INCREMENT,
  `cht_fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cht_id_chat_web` varchar(255) NOT NULL DEFAULT '-',
  `cht_tipo_gestion` varchar(45) NOT NULL DEFAULT '-',
  `cht_estado_chat` varchar(45) NOT NULL DEFAULT '-',
  `cht_recibido` varchar(45) NOT NULL DEFAULT '-',
  `cht_enviado` varchar(45) NOT NULL DEFAULT '-',
  `cht_navegacion_arbol` varchar(45) NOT NULL DEFAULT '-',
  `cht_numero_nit` varchar(45) NOT NULL DEFAULT '-',
  `cht_estado_nit` varchar(45) NOT NULL DEFAULT '-',
  `cht_segmento` varchar(45) NOT NULL DEFAULT '-',
  `cht_razon_social` varchar(250) NOT NULL DEFAULT '-',
  `cht_tipo_documento` varchar(45) NOT NULL DEFAULT '-',
  `cht_numero_documento` varchar(45) NOT NULL DEFAULT '-',
  `cht_nombres_apellidos` varchar(250) NOT NULL DEFAULT '-',
  `cht_numero_contacto` varchar(45) NOT NULL DEFAULT '-',
  `cht_correo_contacto` varchar(250) NOT NULL DEFAULT '-',
  `cht_id_grupo` varchar(45) NOT NULL DEFAULT '-',
  `cht_nombre_grupo` varchar(45) NOT NULL DEFAULT '-',
  `cht_motivo_tramite` varchar(1000) NOT NULL DEFAULT '-',
  `cht_peticion_abierta` varchar(45) NOT NULL DEFAULT '-',
  `cht_numero_caso` varchar(45) NOT NULL DEFAULT '-',
  `cht_adjuntos` varchar(45) NOT NULL DEFAULT '-',
  `cht_ruta_archivo_adjunto` varchar(250) NOT NULL DEFAULT '-',
  `cht_id_tipo_agendamiento` varchar(45) NOT NULL DEFAULT '-',
  `cht_tipo_agendamiento` varchar(45) NOT NULL DEFAULT '-',
  `cht_id_subgrupo` varchar(45) NOT NULL DEFAULT '-',
  `cht_nombre_subgrupo` varchar(45) NOT NULL DEFAULT '-',
  `cht_id_especialista` varchar(45) NOT NULL DEFAULT '-',
  `cht_nombre_especialista` varchar(45) NOT NULL DEFAULT '-',
  `cht_fecha_hora_agendamiento` varchar(45) NOT NULL DEFAULT '-',
  `cht_estado_gestion` varchar(45) NOT NULL DEFAULT '-',
  `cht_descripcion` varchar(1000) NOT NULL DEFAULT '-',
  `cht_tipo_estado` varchar(45) NOT NULL DEFAULT 'Activo',
  `cht_actualizacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cht_responsable` varchar(45) NOT NULL DEFAULT 'Chat Web Segmento 4 ETB',
  PRIMARY KEY (`cht_id`)
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


