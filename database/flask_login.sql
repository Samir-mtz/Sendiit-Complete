-- Active: 1669601641800@@127.0.0.1@3306@flask_login

-- Estructura de tabla para la tabla `user`
create DATABASE `flask_login`;
use flask_login;

CREATE TABLE `user` (
  `id` smallint(3) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` char(150) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `direcion` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `confirmed`  BOOLEAN NOT NULL DEFAULT 0,
  `tipo` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'usuario',
  `confirmed_on` DATE,
  `sucursal` varchar(80) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores the user''s data.';

/* Alter table user add `numpaquetes` INTEGER COLLATE utf8_unicode_ci NOT NULL DEFAULT 0; */

/* drop table lockers; */

CREATE TABLE lockers (
  `id` smallint(3) NOT NULL AUTO_INCREMENT,
  `ubicacion` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `categoria` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `cantidadS` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `cantidadM` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `cantidadL` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `disponibilidad` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `enviados` INTEGER COLLATE utf8_unicode_ci NOT NULL DEFAULT 0,
  `recibidos` INTEGER COLLATE utf8_unicode_ci NOT NULL DEFAULT 0, 
  `activo`  BOOLEAN NOT NULL DEFAULT 1,
  `registrado` DATE,
  PRIMARY KEY(`id`)
);

CREATE TABLE envios (
  `id` smallint(3) NOT NULL AUTO_INCREMENT,
  `origen` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `destino` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `tamano` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `fragil` BOOLEAN NOT NULL DEFAULT 0,
  `estado` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `costo` FLOAT COLLATE utf8_unicode_ci NOT NULL,
  `idusuario` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `fechainicio` DATE DEFAULT NULL,
  `fechaentregado` DATE DEFAULT NULL,
  PRIMARY KEY(`id`)
);

CREATE TABLE tarjetas (
  `id` smallint(3) NOT NULL AUTO_INCREMENT,
  `idusuario` INTEGER COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `numtarjeta` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `expiracion` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `cvv` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY(`id`)
);



INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Lindavista', 'Calle test', 13, 4, 5, 4, 13);
INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Colonia del valle', 'Calle test', 13, 4, 5, 4, 13);
INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Satelite', 'Calle test', 13, 4, 5, 4, 13);
INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Villa de Aragon', 'Calle test', 13, 4, 5, 4, 13);
INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Lindavista', 'Calle test', 13, 4, 5, 4, 13);
INSERT INTO `lockers` (`ubicacion`, `direccion`, `categoria`, `cantidadS`, `cantidadM`, `cantidadL`, `disponibilidad`) VALUES ('Lindavista', 'Calle test', 13, 4, 5, 4, 13);


CREATE TABLE ubicaciones (
  `id` smallint(3) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY(`id`)
);


INSERT INTO `ubicaciones` (`nombre`) VALUES ('Lindavista');
INSERT INTO `ubicaciones` (`nombre`) VALUES ('Colonia del valle');
INSERT INTO `ubicaciones` (`nombre`) VALUES ('Satelite');
INSERT INTO `ubicaciones` (`nombre`) VALUES ('Villa de Aragon');


INSERT INTO `user` (`email`, `password`, `nombre`, `telefono`, `direcion`) VALUES
('armando@tecuani.me', 'sha256$lAYb6AT70LOYOI18$fcc7c27512a4d49a8dc6c6ce1f869d0866ad1534dc105f1925745cc3cdd57a30', 'Armando Martinez', '5616029988', 'None');
--Contraseña: root123
INSERT INTO envios(id,origen,destino,tamano,fragil,estado,nombre,email,telefono,costo,idusuario) VALUES(26,'Lindavista','Almacen','Mediano',0,'EN LOCKER DESTINO','Jorge Ruiz','jorge.ruiz@gmail.com','5516029944',105.35,17);

-- cambiar a numpaquetes a sucursal
ALTER TABLE user  CHANGE `numpaquetes` `sucursal` VARCHAR(80);