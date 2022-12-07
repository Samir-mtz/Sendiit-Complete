from .entities.User import Locker
class ModelLocker():

    @classmethod
    def register(self, db, locker):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO lockers (ubicacion, direccion, tamano, cantidad, disponibilidad, enviados, recibidos, registrado) VALUES ('{locker.ubicacion}','{locker.direccion}','{locker.tamano}',{locker.cantidad},{locker.cantidad}, 0, 0, CURDATE())" #Cantidad va dos veces ya que en un inicio la disponibilidad es la misma
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consult(self, db, ubicacion, tamano): #Nota esta consulta es para obtener el id, por lo cual se le envia ubicacion y tamano
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id,ubicacion, direccion, tamano, cantidad, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}' and tamano='{tamano}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2],tamano=row[3], cantidad=row[4], disponibilidad=row[5], enviados=row[6], recibidos=row[7], activo=row[8], registrado=row[9])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consultAll(self, db, ubicacion): #Nota esta consulta es para obtener todos los que tengan la ubicacion que enviamos retorna una lista de objetos de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id,ubicacion, direccion, tamano, cantidad, disponibilidad, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}'";
            cursor.execute(sql)
            row = cursor.fetchone()
            lockers_registro = []
            if row != None:
                while row is not None:
                    lockers_registro.append(Locker(id=row[0], ubicacion=row[1],direccion=row[2],tamano=row[3], cantidad=row[4], disponibilidad=row[5], enviados=row[6], recibidos=row[7], activo=row[8], registrado=row[9]))
                    row = cursor.fetchone()
                return lockers_registro
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update(self, db, id, locker): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(consultar la disponibilidad anterior y sumar la cantidad de lockers que se van a aumentar)
        try:
            cursor = db.connection.cursor()
            sql = f"UPDATE lockers SET ubicacion='{locker.ubicacion}', direccion='{locker.direccion}', tamano='{locker.tamano}', cantidad={locker.cantidad}, disponibilidad={locker.disponibilidad} WHERE id='{id}'";
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
    