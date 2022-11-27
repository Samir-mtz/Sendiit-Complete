
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
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores the user''s data.';


INSERT INTO `user` (`email`, `password`, `nombre`, `telefono`, `direcion`) VALUES
('armando@tecuani.me', 'sha256$lAYb6AT70LOYOI18$fcc7c27512a4d49a8dc6c6ce1f869d0866ad1534dc105f1925745cc3cdd57a30', 'Armando Martinez', '5616029988', 'None');
--Contraseña: root123

