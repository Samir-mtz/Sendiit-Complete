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
            sql = f"SELECT numtarjeta, nombre, expiracion FROM tarjetas where idusuario='{id}'";
            cursor.execute(sql)
            listtarjetas = []
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                return listtarjetas.append(Tarjeta(numtarjeta=row[0], nombre=row[1],expiracion=row[2]))
            return listtarjetas
        except Exception as ex:
            raise Exception(ex)