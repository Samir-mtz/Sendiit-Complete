from .entities.User import User
from .entities.Envio import Envio
# from .entities.Repartidor import Repartidor
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
    def paquetesAllCondition(self, db, estado, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estado, origen, destino FROM envios 
                    WHERE estado = '{}' and idrepartidor={}""".format(estado, id)
            cursor.execute(sql)
            print(sql)
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
    
    # @classmethod
    # def consultAll(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
    #     try:
    #         cursor = db.connection.cursor()
    #         sql = f"SELECT id, nombre, telefono, correo, rfc FROM repartidores";
    #         cursor.execute(sql)
    #         list_repartidores=[]
    #         while True:
    #             row = cursor.fetchone()
    #             if row == None:
    #                 break
    #             list_repartidores.append( Repartidor(id=row[0], nombre=row[1], telefono=row[2], correo=row[3], rfc=row[4]))
            
    #         if len(list_repartidores)>0:
    #             return list_repartidores
    #         else:
    #             return None
    #     except Exception as ex:
    #         raise Exception(ex)