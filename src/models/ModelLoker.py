from .entities.Locker import Locker
class ModelLocker():

    @classmethod
    def register(self, db, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud):
        try:
            cursor = db.connection.cursor()
            sql = f"INSERT INTO lockers (ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, registrado) VALUES ('{ubicacion}','{direccion}',{cantidadS}, {cantidadM}, {cantidadL},{disponibilidad}, {latitud}, {longitud}, 0, 0, CURDATE())" #Cantidad va dos veces ya que en un inicio la disponibilidad es la misma
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultAll(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, activo, registrado FROM lockers"
            cursor.execute(sql)
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append( Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], latitud=row[7], longitud=row[8], enviados=row[9], recibidos=row[10], activo=row[11], registrado=row[12]))
            
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
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, activo, registrado FROM lockers where id='{id}'"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], latitud=row[7], longitud=row[8], enviados=row[9], recibidos=row[10], activo=row[11], registrado=row[12])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_to_search(self, db, dato): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, activo, registrado FROM lockers WHERE ubicacion LIKE '%"+dato+"%'"
            cursor.execute(sql)
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append( Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], latitud=row[7], longitud=row[8], enviados=row[9], recibidos=row[10], activo=row[11], registrado=row[12]))
            
            if len(list_lockers)>0:
                return list_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)        
        
    @classmethod
    def consult_by_location(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, activo, registrado FROM lockers where ubicacion='{ubicacion}'"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Locker(id=row[0], ubicacion=row[1],direccion=row[2] ,cantidadS=row[3], cantidadM=row[4], cantidadL=row[5], disponibilidad=row[6], latitud=row[7], longitud=row[8], enviados=row[9], recibidos=row[10], activo=row[11], registrado=row[12])

            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def update(self, db, id_recibido, direccion, cantidadS, cantidadM, cantidadL, latitud, longitud): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE lockers SET direccion="'+direccion+'", cantidadS='+str(cantidadS)+', cantidadM='+str(cantidadM)+', cantidadL='+str(cantidadL)+', latitud="'+latitud+'", longitud="'+longitud+'" WHERE id='+id_recibido
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def active_desactive(self, db, id, locker): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            locker.activo = ~locker.activo
            cursor = db.connection.cursor()
            sql = f"UPDATE lockers SET activo={locker.activo} WHERE id={id}"
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def modificar_estado(self, db, id_locker, estado):
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE lockers SET activo='+str(estado)+' WHERE id='+id_locker
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete(self, db, id_locker): 
        try:
            cursor = db.connection.cursor()
            sql = 'DELETE FROM lockers WHERE id ='+id_locker
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)    

    #############Checar disponibilidad del locker
    @classmethod
    def checkDisponibilidad(self, db, origen, destino): 
        try:
            cursor = db.connection.cursor()
            dict_lockers={}
            list_lockers=[]
            sql = f"SELECT cantidadS, cantidadM, cantidadL FROM lockers where ubicacion='{origen}'";
            cursor.execute(sql)
            origen = cursor.fetchone()
            sql = f"SELECT cantidadS, cantidadM, cantidadL FROM lockers where ubicacion='{destino}'";
            cursor.execute(sql)
            destino = cursor.fetchone()

            if origen[0] > 0 and destino[0] > 0:
                list_lockers.append("Chico (20cm, 35cm, 50cm)")
            if origen[1] > 0 and destino[1] > 0:
                list_lockers.append("Mediano(45cm, 35cm, 50cm)")
                
            if origen[2] > 0 and destino[2] > 0:
                list_lockers.append("Grande(85cm, 35cm, 50cm)")
            
            dict_lockers['tamanos']=list_lockers

            if len(dict_lockers)>0:
                return dict_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consultAllDisponibles(self, db): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT ubicacion FROM lockers where activo=1";
            cursor.execute(sql)
            dict_lockers={}
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append(row[0])
            dict_lockers['ubicaciones']=list_lockers
            # print(dict_lockers)
            if len(dict_lockers)>0:
                return dict_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    @classmethod
    def consultDestinos(self, db, ubicacion): #Nota esta consulta es para obtener el registro que contengan la ubicacion que enviamos retorna un objeto de tipo locker
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT ubicacion FROM lockers where ubicacion!='{ubicacion}' and activo=1";
            cursor.execute(sql)
            dict_lockers={}
            list_lockers=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_lockers.append(row[0])
            dict_lockers['ubicaciones']=list_lockers
            # print(dict_lockers)
            if len(dict_lockers)>0:
                return dict_lockers
            else:
                return None
        except Exception as ex:
            raise Exception(ex)