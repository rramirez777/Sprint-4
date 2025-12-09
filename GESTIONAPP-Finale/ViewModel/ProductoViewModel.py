from Models.Producto import Producto
from Servicios.FireBServ import FBServ

class ProductoViewModel:
    def __init__(self, id_tienda):
        self.id_tienda = id_tienda
        self.db = FBServ()

    def agregar_producto(self, nombre, precio, stock, ubicacion, imagen_url=None):

        producto = Producto(nombre, precio, stock, ubicacion, imagen_url)
        self.db.agregar_producto(self.id_tienda, producto)
        print("Producto agregado correctamente.\n")

    def listar_productos(self):
        productos = self.db.obtener_productos(self.id_tienda)
        if not productos:
            print("No hay productos registrados.")
            return {}
        else:
            print("\n=== Productos ===")
            for i, (id_prod, p) in enumerate(productos.items(), 1):
                linea_img = f"IMG: {p.get('imagen_url', 'No tiene')}"
                print(f"{i}. {p['nombre']} - ${p['precio']:.2f} (Stock: {p['stock']}) - {p['ubicacion']} | {linea_img}")
            return productos

    def editar_producto(self):
        productos = self.listar_productos()
        if not productos:
            return

        productos = list(productos.items())
        idx = int(input("Seleccione el número del producto a editar: ")) - 1
        if idx < 0 or idx >= len(productos):
            print("Índice inválido.")
            return

        id_producto, p = productos[idx]

        print("\n=== Editar Producto ===")
        nombre = input(f"Nuevo nombre ({p['nombre']}): ").strip()
        precio = input(f"Nuevo precio ({p['precio']}): ").strip()
        stock = input(f"Nuevo stock ({p['stock']}): ").strip()
        ubicacion = input(f"Nueva ubicación ({p['ubicacion']}): ").strip()
        imagen_url = input(f"Nueva URL de imagen ({p.get('imagen_url', 'sin imagen')}): ").strip()

        patch = {}
        if nombre:
            patch["nombre"] = nombre
        if precio:
            try:
                patch["precio"] = float(precio)
            except ValueError:
                print("Precio inválido. No se modificó.")
        if stock:
            try:
                patch["stock"] = int(stock)
            except ValueError:
                print("Stock inválido. No se modificó.")
        if ubicacion:
            patch["ubicacion"] = ubicacion
        if imagen_url:
            patch["imagen_url"] = imagen_url

        if patch:
            self.db.actualizar_producto(self.id_tienda, id_producto, patch)
            print("Producto actualizado correctamente.\n")
        else:
            print("No se realizaron cambios.\n")

    def eliminar_producto(self):
        productos = self.db.obtener_productos(self.id_tienda)
        if not productos:
            print("No hay productos para eliminar.")
            return

        print("\n=== Productos disponibles ===")
        for i, (id_producto, p) in enumerate(productos.items(), start=1):
            print(f"{i}. {p.get('nombre', '<sin nombre>')} - ${float(p.get('precio', 0)):.2f} (Stock: {p.get('stock', 0)})")

        try:
            idx = int(input("\nSeleccione el número del producto a eliminar: ")) - 1
            id_producto = list(productos.keys())[idx]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        self.db.eliminar_producto(self.id_tienda, id_producto)
        print("Producto eliminado correctamente.\n")