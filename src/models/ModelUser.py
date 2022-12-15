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
            sql = "SELECT id, email, nombre FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
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
            print("*********NAAAAA*********")
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
    
