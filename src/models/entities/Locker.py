
class Locker():

    def __init__(self, id, ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad,enviados, recibidos, activo, registrado=None) -> None:
        self.id = id
        self.ubicacion = ubicacion
        self.direccion = direccion
        self.categoria = categoria
        self.cantidadS = cantidadS
        self.cantidadM = cantidadM
        self.cantidadL = cantidadL
        self.disponibilidad = disponibilidad
        self.enviados = enviados
        self.recibidos = recibidos
        self.activo = activo
        self.registrado = registrado


