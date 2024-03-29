from .entities.Envio import Envio


class ModelEnvio():

    @classmethod
    def register(self, db, envio):
        try:
            # INSERTAMOS EN LA TABLA ENVIOS
            cursor = db.connection.cursor() 
            sql = f"INSERT INTO envios (origen, destino, tamano, estado, nombre, email, telefono, costo, idusuario, fragil, fechainicio) VALUES ('{envio.origen}','{envio.destino}','{envio.tamano}', '{envio.estado}', '{envio.nombre}', '{envio.email}', '{envio.telefono}', {envio.costo}, {envio.idusuario}, {envio.fragil}, CURDATE())"
            cursor.execute(sql)
            db.connection.commit()

            # Decrementamos la cantidad de lockers vacios en origen y destino
            if envio.tamano == 'Chico (20cm, 35cm, 50cm)':
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.origen}'"
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadS = cantidadS - 1 WHERE ubicacion='{envio.destino}'"
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'Mediano(45cm, 35cm, 50cm)':
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.origen}'"
                cursor.execute(sql)
                db.connection.commit()
                sql = f"UPDATE lockers SET cantidadM = cantidadM - 1 WHERE ubicacion='{envio.destino}'"
                cursor.execute(sql)
                db.connection.commit()
            if envio.tamano == 'Grande(85cm, 35cm, 50cm)':
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
            sql = "SELECT origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario, id, fechainicio, fechaentregado FROM envios ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Envio(origen=row[0], destino=row[1], tamano=row[2], fragil=row[3], estado=row[4], nombre=row[5], email=row[6], telefono=row[7], costo=row[8], idusuario=row[9], id=row[10], fechainicio=row[11], fechaentregado=row[12])
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
    def consultaEstado2(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT estado FROM envios where id={id}"
            cursor.execute(sql)
            row = cursor.fetchone()
            lista_estado = []
            envio_dict = {}
            lista_estado.append(row[0])
            envio_dict["estado"] = lista_estado
            if len(envio_dict)>0:
                return envio_dict
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
    
    @classmethod
    def consult_all_by_user(self, db, id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario, fechainicio, fechaentregado FROM envios where idusuario={id_usuario}"
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append( Envio(id=row[0], origen=row[1], destino=row[2], tamano=row[3], fragil=row[4], estado=row[5], nombre=row[6], email=row[7], telefono=row[8], costo=row[9], idusuario=row[10], fechainicio=row[11], fechaentregado=row[12]) )
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return []
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_to_search_paquete(self, db, id_usuario, dato):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario FROM envios where idusuario="+id_usuario+" and id like '%"+dato+"%' or origen like '%"+dato+"%' or destino like '%"+dato+"%' or tamano like '%"+dato+"%' or fragil like '%"+dato+"%' or estado like '%"+dato+"%' or nombre like '%"+dato+"%' or email like '%"+dato+"%' or telefono like '%"+dato+"%' or costo like '%"+dato+"%' or fechainicio like '%"+dato+"%' or fechaentregado like '%"+dato+"%'"
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append( Envio(id=row[0], origen=row[1], destino=row[2], tamano=row[3], fragil=row[4], estado=row[5], nombre=row[6], email=row[7], telefono=row[8], costo=row[9], idusuario=row[10]) )
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return []
        except Exception as ex:
            raise Exception(ex)
        
# SELECT * FROM envios ORDER BY id DESC LIMIT 1;
