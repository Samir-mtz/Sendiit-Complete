from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import datetime


class User(UserMixin):

    def __init__(self, id, email, password, nombre="",telefono="", direccion="",confirmed=0, tipo="", confirmed_on=None, numPaq=0) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.confirmed = confirmed
        self.tipo = tipo
        self.confirmed_on = confirmed_on
        self.numPaq = numPaq


    @classmethod
    def check_password(self, hashed_password, password):
        # print ("pass: "+generate_password_hash("root123", "sha256"))
        return check_password_hash(hashed_password, password)

    @classmethod
    def generate_password(self, password):
        return generate_password_hash(password, "sha256")