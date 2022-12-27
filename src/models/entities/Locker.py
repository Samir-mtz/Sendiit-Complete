
class Locker():

    def __init__(self, id, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud, enviados, recibidos, activo, registrado=None) -> None:
        self.id = id
        self.ubicacion = ubicacion
        self.direccion = direccion
        self.cantidadS = cantidadS
        self.cantidadM = cantidadM
        self.cantidadL = cantidadL
        self.disponibilidad = disponibilidad
        self.enviados = enviados
        self.recibidos = recibidos
        self.activo = activo
        self.latitud = latitud
        self.longitud = longitud
        self.registrado = registrado


