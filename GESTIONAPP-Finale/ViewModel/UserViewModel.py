from Models.Usuario import Usuario
from Servicios.FireBServ import FBServ
from firebase_admin import db

class UserViewModel:
    def __init__(self):
        self.db = FBServ()

    def registrar_usuario(self, nombre: str, correo: str, contrasena: str) -> Usuario:
        usuario = Usuario(nombre, correo, contrasena)
        self.db.guardar_usuario(usuario)
        print("Usuario registrado correctamente.\n")
        return usuario

    def iniciar_sesion(self, correo: str, contrasena: str) -> Usuario | None:
        ref = db.reference("/usuarios")
        usuarios = ref.get()
        if not usuarios:
            print("No hay usuarios registrados.")
            return None

        for uid, datos in usuarios.items():
            if datos.get("correo") == correo and datos.get("contrasena") == contrasena:
                return Usuario(datos.get("nombre"), datos.get("correo"), datos.get("contrasena"))

        print("Credenciales incorrectas.")
        return None

    def obtener_usuario_por_correo(self, correo: str) -> dict | None:
        ref = db.reference("/usuarios")
        usuarios = ref.get()
        if not usuarios:
            return None

        for uid, datos in usuarios.items():
            if datos.get("correo") == correo:
                return {"id": uid, **datos}
        return None