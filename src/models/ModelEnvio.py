from .entities.Envio import Envio
class ModelEnvio():

    @classmethod
    def register(self, db, envio):
        try:
            ###ASIGNAR AL REPARTIDOR ENCONTRANDO EL QUE TENGA MENOS PAQUETES ASIGNADOS
            cursor = db.connection.cursor()
            sql = f"SELECT id, numpaquetes FROM user where tipo='repartidor'";
            cursor.execute(sql)
            minimo=1000000
            asignacion=-1
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                if minimo >= row[1]:
                    minimo = row[1]
                    asignacion = row[0]
            ###
            ###INSERTAMOS EN LA TABLA ENVIOS
            cursor = db.connection.cursor()
            sql = f"INSERT INTO envios (origen, destino, tamano, estado, nombre, email, telefono, costo, idusuario, idrepartidor) VALUES ('{envio.origen}','{envio.destino}','{envio.tamano}', 'EN ESPERA DE ENTREGA', {envio.nombre}, {envio.email}, {envio.telefono}, {envio.costo}, {envio.idusuario}, {asignacion})"
            cursor.execute(sql)
            db.connection.commit()

            #Decrementamos la cantidad de lockers vacios en origen y destino
            if envio.tamano == 'pequeno':
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.origen}'";
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.destino}'";
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'mediano':
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.origen}'";
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.destino}'";
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'grande':
                sql = f"UPDATE lockers SET cantidadL = cantidadL - 1 WHERE ubicacion='{envio.origen}'";
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadL = cantidadL - 1 WHERE ubicacion='{envio.destino}'";
                cursor.execute(sql)
                db.connection.commit()
            
        except Exception as ex:
            raise Exception(ex)
