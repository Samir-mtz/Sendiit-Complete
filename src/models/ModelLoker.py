from .entities.Locker import Locker
class ModelLocker():

    @classmethod
    def register(self, db, locker):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO lockers (ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, registrado) VALUES ('{locker.ubicacion}','{locker.direccion}',{locker.cantidadS}, {locker.cantidadM}, {locker.cantidadL},{locker.cantidad}, 0, 0, CURDATE())" #Cantidad va dos veces ya que en un inicio la disponibilidad es la misma
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultAll(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers";
            cursor.execute(sql)
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append( Locker(id=row[0], ubicacion=row[1],direccion=row[2], categoria=row[3] ,cantidadS=row[4], cantidadM=row[5], cantidadL=row[6], disponibilidad=row[7], enviados=row[8], recibidos=row[9], activo=row[10], registrado=row[11]))
            
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
            sql = f"SELECT id,ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{id}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2], categoria=row[3] ,cantidadS=row[4], cantidadM=row[5], cantidadL=row[6], disponibilidad=row[7], enviados=row[8], recibidos=row[9], activo=row[10], registrado=row[11])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    def consult_by_location(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id,ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2], categoria=row[3] ,cantidadS=row[4], cantidadM=row[5], cantidadL=row[6], disponibilidad=row[7], enviados=row[8], recibidos=row[9], activo=row[10], registrado=row[11])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def update(self, db, id, locker): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = f"UPDATE lockers SET ubicacion='{locker.ubicacion}', direccion='{locker.direccion}', direccion='{locker.categoria}', cantidadS={locker.cantidadS},cantidadM={locker.cantidadM}, cantidadL={locker.cantidadL}, disponibilidad={locker.disponibilidad} WHERE id='{id}'";
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
            sql = f"DELETE FROM lockers WHERE id='{id}'";
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)    