class Tarjeta():

    def __init__(self, id, numtarjeta, expiracion, nombre, idusuario, cvv) -> None:
        self.id = id
        self.idusuario = idusuario
        self.nombre = nombre
        self.numtarjeta = numtarjeta
        self.expiracion = expiracion
        self.cvv = cvv
        