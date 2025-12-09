from ViewModel.UserViewModel import UserViewModel
from ViewModel.TiendaViewModel import TiendaViewModel
from ViewModel.ProductoViewModel import ProductoViewModel
from View.SplashView import SplashView
import customtkinter as ctk


class AppTienda:
    def __init__(self):

        self.UserViewModel = UserViewModel
        self.TiendaViewModel = TiendaViewModel
        self.ProductoViewModel = ProductoViewModel

    def menu_tienda(self, usuario):
        tvm = self.TiendaViewModel(usuario)

        while True:
            print("\n=== Menú de Tiendas ===")
            print("1. Ver mis tiendas")
            print("2. Registrar nueva tienda")
            print("3. Gestionar productos de una tienda")
            print("4. Editar una tienda")
            print("5. Eliminar una tienda")
            print("6. Cerrar sesión")

            op = input("Seleccione una opción: ")

            if op == "1":
                tvm.listar_tiendas()

            elif op == "2":
                nombre = input("Nombre tienda: ")
                categoria = input("Categoría: ")
                direccion = input("Dirección: ")
                tvm.registrar_tienda(nombre, categoria, direccion)

            elif op == "3":
                tiendas = tvm.listar_tiendas()
                if not tiendas:
                    continue
                idx = int(input("Seleccione el número de la tienda: ")) - 1
                id_tienda, _ = tiendas[idx]
                self.menu_productos(id_tienda)

            elif op == "4":
                tiendas = tvm.listar_tiendas()
                if not tiendas:
                    continue
                idx = int(input("Seleccione el número de la tienda a editar: ")) - 1
                id_tienda, _ = tiendas[idx]
                tvm.editar_tienda(id_tienda)

            elif op == "5":
                tiendas = tvm.listar_tiendas()
                if not tiendas:
                    continue
                idx = int(input("Seleccione el número de la tienda a eliminar: ")) - 1
                id_tienda, _ = tiendas[idx]
                tvm.eliminar_tienda(id_tienda)

            elif op == "6":
                print("Cerrando sesión...\n")
                break

            else:
                print("Opción no válida.")

    def menu_productos(self, id_tienda):
        pvm = self.ProductoViewModel(id_tienda)

        while True:
            print("\n=== Menú de Productos ===")
            print("1. Ver productos")
            print("2. Agregar producto")
            print("3. Editar producto")
            print("4. Eliminar producto")
            print("5. Volver")

            op = input("Seleccione una opción: ")

            if op == "1":
                pvm.listar_productos()

            elif op == "2":
                nombre = input("Nombre producto: ")
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                ubicacion = input("Ubicación producto: ")
                pvm.agregar_producto(nombre, precio, stock, ubicacion)

            elif op == "3":
                pvm.editar_producto()
            
            elif op == "4":
                print("DEBUG — métodos disponibles en pvm:", [m for m in dir(pvm) if not m.startswith("__")])
                pvm.eliminar_producto()

            elif op == "5":
                break

            else:
                print("Opción no válida.")

    def run(self):
        vm_usuario = self.UserViewModel()

        while True:
            print("\n=== Sistema de Gestión de Tienda ===")
            print("1. Iniciar sesión")
            print("2. Registrar nuevo usuario")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                correo = input("Correo: ")
                contrasena = input("Contraseña: ")
                usuario = vm_usuario.iniciar_sesion(correo, contrasena)
                if usuario:
                    self.menu_tienda(usuario)

            elif opcion == "2":
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                contrasena = input("Contraseña: ")
                vm_usuario.registrar_usuario(nombre, correo, contrasena)

            elif opcion == "3":
                print("Saliendo...")
                break

            else:
                print("Opción no válida.\n")

ctk.set_appearance_mode("light")
if __name__ == "__main__":
    app = SplashView()
    app.mainloop()