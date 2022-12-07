
class Locker():

    def __init__(self, id, ubicacion, direccion, tamano,cantidad, disponibilidad,enviados, recibidos, activo, registrado=None) -> None:
        self.id = id
        self.ubicacion = ubicacion
        self.direccion = direccion
        self.tamano = tamano
        self.cantidad = cantidad
        self.disponibilidad = disponibilidad
        self.enviados = enviados
        self.recibidos = recibidos
        self.activo = activo
        self.registrado = registrado


