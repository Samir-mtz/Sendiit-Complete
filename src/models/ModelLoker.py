from .entities.Locker import Locker
class ModelLocker():

    @classmethod
    def register(self, db, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO lockers (ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, registrado) VALUES ('{ubicacion}','{direccion}',{cantidadS}, {cantidadM}, {cantidadL},{disponibilidad}, 0, 0, CURDATE())" #Cantidad va dos veces ya que en un inicio la disponibilidad es la misma
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultAll(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers";
            cursor.execute(sql)
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append( Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], enviados=row[7], recibidos=row[8], activo=row[9], registrado=row[10]))
            
            if len(list_lockers)>0:
                return list_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consult_by_id(self, db, id): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id,ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where id='{id}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], enviados=row[7], recibidos=row[8], activo=row[9], registrado=row[10])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    def consult_by_location(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], enviados=row[7], recibidos=row[8], activo=row[9], registrado=row[10])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def update(self, db, id, direccion): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE lockers SET direccion = "' + direccion +'" WHERE id =' + id
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def active_desactive(self, db, id, locker): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            locker.activo = ~locker.activo
            cursor = db.connection.cursor()
            sql = f"UPDATE lockers SET activo={locker.activo} WHERE id='{id}'";
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete(self, db, id): 
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM lockers WHERE id="+id+";"
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)    

    #############Checar disponibilidad del locker
    @classmethod
    def checkDisponibilidad(self, db, origen, destino, tamano): 
        try:
            cursor = db.connection.cursor()
            if tamano == 'pequeno':
                sql = f"SELECT cantidadS FROM lockers where ubicacion='{origen}'";
                cursor.execute(sql)
                origen = cursor.fetchone()
                sql = f"SELECT cantidadS FROM lockers where ubicacion='{destino}'";
                cursor.execute(sql)
                destino = cursor.fetchone()
            if tamano == 'mediano':
                sql = f"SELECT cantidadM  FROM lockers where ubicacion='{origen}'";
                cursor.execute(sql)
                origen = cursor.fetchone()
                sql = f"SELECT cantidadM  FROM lockers where ubicacion='{destino}'";
                cursor.execute(sql)
                destino = cursor.fetchone()
            if tamano == 'grande':
                sql = f"SELECT cantidadL FROM lockers where ubicacion='{origen}'";
                cursor.execute(sql)
                origen = cursor.fetchone()
                sql = f"SELECT cantidadL FROM lockers where ubicacion='{destino}'";
                cursor.execute(sql)
                destino = cursor.fetchone()
            if origen > 0 and destino > 0:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)    