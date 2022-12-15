from .entities.User import User
from .entities.Envio import Envio
import datetime
class ModelRepartidor():

    @classmethod
    def paquetesAll(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estado, origen, destino FROM envios 
                    WHERE idrepartidor = '{}'""".format(id)
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append(Envio(estado=row[0], origen=row[1],destino=row[2]))
            
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def paquetesAllCondition(self, db, estado):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estado, origen, destino FROM envios 
                    WHERE estado = '{}'""".format(estado)
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append(Envio(estado=row[0], origen=row[1],destino=row[2]))
            
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    