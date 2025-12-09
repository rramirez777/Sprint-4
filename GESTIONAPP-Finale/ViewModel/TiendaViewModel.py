from Models.Tienda import Tienda
from Servicios.FireBServ import FBServ

class TiendaViewModel:
    def __init__(self, usuario):
        self.usuario = usuario
        self.db = FBServ()

    def registrar_tienda(self, nombre, categoria, direccion):
        tienda = Tienda(nombre, categoria, direccion, self.usuario)
        self.db.guardar_tienda(tienda)
        print("Tienda registrada correctamente.\n")

    def listar_tiendas(self):
        tiendas = self.db.obtener_tiendas_por_usuario(self.usuario.nombre)
        if not tiendas:
            print("No tienes tiendas registradas.")
            return []

        print("\n=== Tus Tiendas ===")
        lista_tiendas = []
        for i, (id_tienda, t) in enumerate(tiendas.items(), start=1):
            print(f"{i}. {t['nombre']} - {t['categoria']} ({t['direccion']})")
            lista_tiendas.append((id_tienda, t))
        return lista_tiendas

    def editar_tienda(self, id_tienda):
        print("\n=== Editar Tienda ===")
        nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ").strip()
        categoria = input("Nueva categoría (dejar en blanco): ").strip()
        direccion = input("Nueva dirección (dejar en blanco): ").strip()

        patch = {}
        if nombre:
            patch['nombre'] = nombre
        if categoria:
            patch['categoria'] = categoria
        if direccion:
            patch['direccion'] = direccion

        if patch:
            self.db.actualizar_tienda(id_tienda, patch)
            print("Tienda actualizada correctamente.\n")
        else:
            print("No se hizo ningún cambio.\n")

    def eliminar_tienda(self, id_tienda):
        confirm = input(f"¿Seguro que quieres eliminar la tienda '{id_tienda}'? Esto borrará sus productos. (s/n): ").strip().lower()
        if confirm == 's':
            self.db.eliminar_tienda(id_tienda)
            print("Tienda eliminada correctamente.\n")
        else:
            print("Cancelado.\n")
