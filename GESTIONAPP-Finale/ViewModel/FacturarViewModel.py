from Models.Factura import FacturaModel, FacturaItem
from Servicios.FireBServ import FBServ
from datetime import datetime

class FacturaViewModel:
    def __init__(self, usuario_nombre):
        self.fb = FBServ()
        self.usuario_nombre = usuario_nombre
        self.tiendas_cache = {}   
        self.productos_cache = {} 
        self.cart = []            
        self.current_tienda_id = None

    # ---- Tiendas ----
    def cargar_tiendas_usuario(self):
        tiendas = self.fb.obtener_tiendas_por_usuario(self.usuario_nombre)
        # tiendas: {id: data}
        self.tiendas_cache = {t["nombre"]: k for k, t in (tiendas.items() if tiendas else [])}
        return list(self.tiendas_cache.keys())

    def obtener_id_tienda_por_nombre(self, nombre_tienda):
        return self.tiendas_cache.get(nombre_tienda)

    # ---- Productos ----
    def cargar_productos(self, id_tienda):
        self.current_tienda_id = id_tienda
        productos = self.fb.obtener_productos(id_tienda)
        self.productos_cache = productos if productos else {}
        return self.productos_cache

    def obtener_producto(self, id_producto):
        return self.productos_cache.get(id_producto)

    # ---- Carrito ----
    def agregar_item_al_carrito(self, id_producto, cantidad):
        prod = self.obtener_producto(id_producto)
        if not prod:
            raise ValueError("Producto no encontrado")
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")

        # Si ya existe en carrito, sumar cantidades
        for item in self.cart:
            if item.id_producto == id_producto:
                item.cantidad += cantidad
                item.subtotal = item.cantidad * float(item.precio_unitario)
                return

        precio = float(prod.get("precio", 0))
        item = FacturaItem(
            id_producto=id_producto,
            nombre=prod.get("nombre", ""),
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=precio * cantidad
        )
        self.cart.append(item)

    def eliminar_item_del_carrito(self, id_producto):
        self.cart = [it for it in self.cart if it.id_producto != id_producto]

    def vaciar_carrito(self):
        self.cart = []

    def obtener_total(self):
        return sum(float(it.subtotal) for it in self.cart)

    def obtener_resumen_carrito(self):
        return [{
            "id_producto": it.id_producto,
            "nombre": it.nombre,
            "cantidad": it.cantidad,
            "precio_unitario": it.precio_unitario,
            "subtotal": it.subtotal
        } for it in self.cart]

    # ---- Validaciones de stock ----
    def stock_suficiente_para_carrito(self):
        for it in self.cart:
            prod = self.obtener_producto(it.id_producto)
            if not prod:
                return False, f"Producto {it.nombre} no disponible"
            stock = int(prod.get("stock", 0))
            if stock < it.cantidad:
                return False, f"Stock insuficiente para {it.nombre} (disp: {stock})"
        return True, None

    # ---- Guardar factura completa ----
    def guardar_factura_completa(self):
        if not self.current_tienda_id:
            raise ValueError("Tienda no seleccionada")
        if len(self.cart) == 0:
            raise ValueError("Carrito vacío")

        ok, msg = self.stock_suficiente_para_carrito()
        if not ok:
            raise ValueError(msg)

        total = self.obtener_total()

        items_dict = {}
        for idx, it in enumerate(self.cart):
            items_dict[f"item_{idx}"] = {
                "id_producto": it.id_producto,
                "nombre": it.nombre,
                "cantidad": it.cantidad,
                "precio_unitario": it.precio_unitario,
                "subtotal": it.subtotal
            }

        factura_data = {
            "fecha": datetime.now().isoformat(),
            "total": total,
            "items": items_dict
        }

        key = self.fb.registrar_factura(self.current_tienda_id, factura_data)

        items_for_descontar = [{"id_producto": it.id_producto, "cantidad": it.cantidad} for it in self.cart]
        self.fb.descontar_stocks(self.current_tienda_id, items_for_descontar)

        self.vaciar_carrito()

        return key

    # ---- Historial / detalle / eliminar ----
    def listar_ventas(self, id_tienda):
        ventas = self.fb.obtener_historial_ventas(id_tienda)
        return ventas if ventas else {}

    def obtener_detalle_venta(self, id_tienda, id_venta):
        return self.fb.obtener_venta(id_tienda, id_venta)

    def eliminar_factura(self, id_tienda, id_venta):
        self.fb.eliminar_venta(id_tienda, id_venta)
        return True
