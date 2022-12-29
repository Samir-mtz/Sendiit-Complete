from .entities.User import User
from .entities.Envio import Envio
# from .entities.Repartidor import Repartidor
import datetime
class ModelRepartidor():

    @classmethod
    def paquetesAll(self, db, sucursal):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estado, origen, destino, id FROM envios 
                    WHERE origen = '{}' or destino = '{}' """.format(sucursal, sucursal)
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                if row[0]=="EN ESPERA DEL REPARTIDOR":
                    list_paquetes.append(Envio(estado="RECOLECTAR", origen=row[1],destino=row[2], id=row[3]))
                else:
                    list_paquetes.append(Envio(estado="ENTREGAR", origen=row[1],destino=row[2], id=row[3]))
            
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def paquetesRecolectar(self, db, sucursal):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estado, origen, destino, id FROM envios 
                    WHERE estado = 'EN ESPERA DEL REPARTIDOR' and origen = '{}'""".format( sucursal)
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append(Envio(estado="RECOLECTAR", origen=row[1],destino=row[2], id=row[3]))
            
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def paquetesEntregar(self, db, sucursal):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT  estado, origen, destino, id destino FROM envios 
                    WHERE estado = 'EN CAMINO' and destino = '{}'""".format( sucursal)
            cursor.execute(sql)
            list_paquetes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_paquetes.append(Envio(estado="ENTREGAR", origen=row[1],destino=row[2], id=row[3]))
            
            if len(list_paquetes)>0:
                return list_paquetes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    