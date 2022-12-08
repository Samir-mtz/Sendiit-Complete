from .entities.User import Locker
class ModelLocker():

    @classmethod
    def register(self, db, locker):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO lockers (ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, registrado) VALUES ('{locker.ubicacion}','{locker.direccion}',{locker.cantidadS}, {locker.cantidadM}, {locker.cantidadL},{locker.cantidad}, 0, 0, CURDATE())" #Cantidad va dos veces ya que en un inicio la disponibilidad es la misma
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultAll(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers";
            cursor.execute(sql)
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append( Locker(id=row[0], ubicacion=row[1],direccion=row[2], cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], enviados=row[7], recibidos=row[8], activo=row[9], registrado=row[10]))
            
            if len(list_lockers)>0:
                return list_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consult(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id,ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2], cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], enviados=row[7], recibidos=row[8], activo=row[9], registrado=row[10])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update(self, db, id, locker): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = f"UPDATE lockers SET ubicacion='{locker.ubicacion}', direccion='{locker.direccion}', cantidadS={locker.cantidadS},cantidadM={locker.cantidadM}, cantidadL={locker.cantidadL}, disponibilidad={locker.disponibilidad} WHERE id='{id}'";
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
    def update(self, db, id): 
        try:
            cursor = db.connection.cursor()
            sql = f"DELETE FROM lockers WHERE id='{id}'";
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)    