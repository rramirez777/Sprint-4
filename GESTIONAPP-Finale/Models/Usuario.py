# Clase Usuario: representa una persona que usa la app

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def mostrar_info(self):
        return f"Usuario: {self.nombre} | Correo: {self.correo}"
