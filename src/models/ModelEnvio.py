from .entities.Envio import Envio


class ModelEnvio():

    @classmethod
    def register(self, db, envio):
        try:
            # ASIGNAR AL REPARTIDOR ENCONTRANDO EL QUE TENGA MENOS PAQUETES ASIGNADOS
            cursor = db.connection.cursor()
            sql = f"SELECT id, numpaquetes FROM user where tipo='repartidor'"
            cursor.execute(sql)
            minimo = 1000000
            asignacion = -1
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                if minimo >= row[1]:
                    minimo = row[1]
                    asignacion = row[0]
            sql = f"UPDATE user SET numpaquetes = { minimo + 1} WHERE id={asignacion}"
            cursor.execute(sql)
            db.connection.commit()
            ##
            # INSERTAMOS EN LA TABLA ENVIOS
            cursor = db.connection.cursor()
            sql = f"INSERT INTO envios (origen, destino, tamano, estado, nombre, email, telefono, costo, idusuario, idrepartidor) VALUES ('{envio.origen}','{envio.destino}','{envio.tamano}', '{envio.estado}', '{envio.nombre}', '{envio.email}', '{envio.telefono}', {envio.costo}, {envio.idusuario}, {asignacion})"
            cursor.execute(sql)
            db.connection.commit()

            # Decrementamos la cantidad de lockers vacios en origen y destino
            if envio.tamano == 'Chico':
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.origen}'"
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.destino}'"
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'Mediano':
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.origen}'"
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.destino}'"
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'Grande':
                sql = f"UPDATE lockers SET cantidadL = cantidadL - 1 WHERE ubicacion='{envio.origen}'"
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadL = cantidadL - 1 WHERE ubicacion='{envio.destino}'"
                cursor.execute(sql)
                db.connection.commit()

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultLast(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario, idrepartidor, id FROM envios ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Envio(origen=row[0], destino=row[1], tamano=row[2], fragil=row[3], estado=row[4], nombre=row[5], email=row[6], telefono=row[7], costo=row[8], idusuario=row[9], idrepartidor=row[10], id=row[11])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


# SELECT * FROM envios ORDER BY id DESC LIMIT 1;
