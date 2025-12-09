# Clase Tienda: representa una tienda registrada por un usuario

class Tienda:
    def __init__(self, nombre, categoria, direccion, propietario):
        self.nombre = nombre
        self.categoria = categoria
        self.direccion = direccion
        self.propietario = propietario  # objeto Usuario

    def mostrar_info(self):
        return (f"Tienda: {self.nombre} ({self.categoria})\n"
                f"Dirección: {self.direccion}\n"
                f"Propietario: {self.propietario.nombre}")
