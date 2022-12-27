from .entities.Locker import Locker
class ModelMapbox():
    @classmethod
    def consultaCoordenadas(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT ubicacion, direccion, latitud, longitud FROM lockers where activo=1";
            cursor.execute(sql)
            dict_lockers={}
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append([row[0], row[1], row[2], row[3]])
            # dict_lockers['ubicaciones']=list_lockers
            # print(dict_lockers)
            if len(list_lockers)>0:
                return list_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)