
class Envio():

    def __init__(self, origen,estado, destino, tamano="", fragil="", nombre="", email="", telefono="", costo="", idusuario="", id=-1, fechainicio="", fechaentregado="") -> None:
        self.id = id
        self.origen = origen
        self.destino = destino
        self.tamano = tamano
        self.fragil = fragil
        self.estado = estado
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.costo = costo
        self.idusuario = idusuario
        self.fechainicio = fechainicio
        self.fechaentregado = fechaentregado
