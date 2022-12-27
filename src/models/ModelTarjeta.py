from .entities.Tarjeta import Tarjeta
class ModelTarjeta():

    @classmethod
    def register(self, db, tarjeta):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO tarjetas (idusuario, nombre, numtarjeta, expiracion, cvv) VALUES ('{tarjeta.idusuario}','{tarjeta.nombre}','{tarjeta.numtarjeta}', '{tarjeta.expiracion}', {tarjeta.cvv})"
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultAll(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT numtarjeta, expiracion, nombre, idusuario, cvv, id FROM tarjetas"
            cursor.execute(sql)
            
            list_tarjetas = []
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_tarjetas.append(Tarjeta(numtarjeta=row[0], expiracion=row[1], nombre=row[2], idusuario=row[3], cvv=row[4], id=row[5]))
            if len(list_tarjetas)>0:
                return list_tarjetas
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT numtarjeta, expiracion, nombre, cvv, id FROM tarjetas where idusuario='{id}'"
            cursor.execute(sql)
            
            list_tarjetas = []
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_tarjetas.append(Tarjeta(numtarjeta=row[0], expiracion=row[1], nombre=row[2], idusuario=id, cvv=row[3], id=row[4]))
            if len(list_tarjetas)>0:
                return list_tarjetas
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update(self, db, tarjeta): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE tarjetas SET idusuario='+  tarjeta.idusuario +', nombre="'+  tarjeta.nombre +'", numtarjeta="'+  tarjeta.numtarjeta +'", expiracion="'+  tarjeta.expiracion +'", cvv="'+  tarjeta.idusuario +'" where id =' + tarjeta.id
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete(self, db, tarjeta): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = 'DELETE FROM tarjetas where id =' + tarjeta.id
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)