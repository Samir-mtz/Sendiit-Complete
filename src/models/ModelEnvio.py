from .entities.Envio import Envio


class ModelEnvio():

    @classmethod
    def register(self, db, envio):
        try:
            # INSERTAMOS EN LA TABLA ENVIOS
            cursor = db.connection.cursor()
            sql = f"INSERT INTO envios (origen, destino, tamano, estado, nombre, email, telefono, costo, idusuario) VALUES ('{envio.origen}','{envio.destino}','{envio.tamano}', '{envio.estado}', '{envio.nombre}', '{envio.email}', '{envio.telefono}', {envio.costo}, {envio.idusuario})"
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
            sql = "SELECT origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario, id FROM envios ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Envio(origen=row[0], destino=row[1], tamano=row[2], fragil=row[3], estado=row[4], nombre=row[5], email=row[6], telefono=row[7], costo=row[8], idusuario=row[9], id=row[10])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultaEstado(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT estado FROM envios where id={id}"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ChangeStatus(self, db, id, estado): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = f"UPDATE envios SET estado='{estado}' WHERE id='{id}'"
            print(sql)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def rastreoEnvio(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT estado, origen, destino FROM envios where id={id}"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Envio(estado=row[0], origen=row[1], destino=row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
# SELECT * FROM envios ORDER BY id DESC LIMIT 1;
