class Tarjeta():

    def __init__(self, numtarjeta, expiracion, nombre, idusuario=None, cvv=None, id=-1) -> None:
        self.id = id
        self.idusuario = idusuario
        self.nombre = nombre
        self.numtarjeta = numtarjeta
        self.expiracion = expiracion
        self.cvv = cvv
        