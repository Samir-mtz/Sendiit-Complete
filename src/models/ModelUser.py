from .entities.User import User
import datetime

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, password, nombre FROM user 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, nombre, sucursal FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], sucursal=row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def register(self, db, user):
        try:
            encrypted_password = User.generate_password(user.password)
            cursor = db.connection.cursor()
            sql = f"INSERT INTO user (email, password, nombre, telefono, direcion) VALUES ('{user.email}','{encrypted_password}','{user.nombre}','{user.telefono}','{user.direccion}')"
            cursor.execute(sql)
            db.connection.commit()
            
            try:
                cursor = db.connection.cursor()
                sql = """SELECT id, email, password, nombre FROM user 
                        WHERE email = '{}'""".format(user.email)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                    return user
                else:
                    return None
            except Exception as ex:
                raise Exception(ex)
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def check_email(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre FROM user WHERE email = '{}'".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consulta_email(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, confirmed, nombre, tipo FROM user WHERE email = '{}'".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(email="",password=None,id=row[0], confirmed=row[1], nombre=row[2], tipo=row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consulta_telefono(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT telefono FROM user WHERE id =" + str(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def confirm_user(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE user SET confirmed=1, confirmed_on=CURDATE() WHERE email='" + email + "';"
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)    
    
    @classmethod
    def infoRepartidor(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT nombre, email, telefono, direcion, confirmed_on FROM user WHERE email = '{}'".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(nombre=row[0], email=row[1], telefono=row[2], direccion=row[3], confirmed_on=row[4], id=-1, password=None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)    

    @classmethod
    def registerRepartidor(self, db, email, password, nombre, telefono, direccion, sucursal):
        try:
            encrypted_password = User.generate_password(password)
            cursor = db.connection.cursor()
            sql = f"INSERT INTO user (email, password, nombre, telefono, direcion, sucursal, tipo, confirmed, confirmed_on ) VALUES ('{email}','{encrypted_password}','{nombre}','{telefono}','{direccion}', '{sucursal}', 'repartidor', 1, CURDATE())"
            cursor.execute(sql)
            db.connection.commit()
            return 1
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consultRepartidoresAll(self, db):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, nombre, email, telefono, direcion, sucursal, confirmed FROM user where tipo='repartidor'";
            cursor.execute(sql)
            list_repartidores=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_repartidores.append( User(id=row[0], nombre=row[1],email=row[2], telefono=row[3] ,direccion=row[4], password='', sucursal=row[5], confirmed=row[6], tipo=''))
            
            if len(list_repartidores)>0:
                return list_repartidores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_to_search_repartidor(self, db, dato):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre, email, telefono, direcion, sucursal, confirmed FROM user where tipo='repartidor' and id like '%"+dato+"%' or nombre like '%"+dato+"%' or email like '%"+dato+"%' or telefono like '%"+dato+"%' or direcion like '%"+dato+"%' or sucursal like '%"+dato+"%'"
            cursor.execute(sql)
            list_repartidores=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_repartidores.append( User(id=row[0], nombre=row[1],email=row[2], telefono=row[3] ,direccion=row[4], password='', sucursal=row[5], confirmed=row[6], tipo=''))
            
            if len(list_repartidores)>0:
                return list_repartidores
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_repartidor_by_id(self, db, id_repartidor):
        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, nombre, email, telefono, direcion, confirmed FROM user where id='+id_repartidor
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[1],email=row[2], telefono=row[3] ,direccion=row[4], password='', confirmed=row[5], tipo='')
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def consultClientesAll(self, db):
        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, nombre, email, telefono, direcion, confirmed FROM user where tipo="usuario"'
            cursor.execute(sql)
            list_clientes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_clientes.append( User(id=row[0], nombre=row[1],email=row[2], telefono=row[3], direccion=row[4], password='', confirmed=row[5], tipo=''))
            
            if len(list_clientes)>0:
                return list_clientes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_to_search_cliente(self, db, dato):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre, email, telefono, direcion, confirmed FROM user where tipo='usuario' and nombre like '%"+dato+"%' or email like '%"+dato+"%' or telefono like '%"+dato+"%' or direcion like '%"+dato+"%'"
            cursor.execute(sql)
            list_clientes=[]
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                list_clientes.append( User(id=row[0], nombre=row[1],email=row[2], telefono=row[3], direccion=row[4], password='', confirmed=row[5], tipo=''))
            
            if len(list_clientes)>0:
                return list_clientes
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_cliente_by_id(self, db, id_recibido):
        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, nombre, email, telefono, direcion, confirmed FROM user where id='+id_recibido
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[1],email=row[2], telefono=row[3] ,direccion=row[4], password='', confirmed=row[5], tipo='')
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def consult_paquetes_clientes(self, db, id_cliente):
        try:
            cursor = db.connection.cursor()
            sql = 'SELECT count(*) FROM envios where idusuario='+id_cliente
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete(self, db, id_user):
        try:
            cursor = db.connection.cursor()
            sql = 'DELETE FROM user WHERE id ='+ id_user
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_cliente(self, db, id_recibido, nombre, email, telefono, direccion): #Nota al incrementar la cantidad de locker la disponibilidad cambia, este dato se debe de corregir en el objeto que se envie(diccionario)
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE user SET nombre="'+nombre+'", email="'+email+'", telefono="'+telefono+'", direcion="'+direccion+'" WHERE id='+id_recibido
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def modificar_estado(self, db, id_user, estado):
        try:
            cursor = db.connection.cursor()
            sql = 'UPDATE user SET confirmed="'+str(estado)+'" WHERE id='+id_user
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)