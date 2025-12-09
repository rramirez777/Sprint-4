import firebase_admin
from firebase_admin import credentials, db
from Models.Tienda import Tienda
from firebase_admin import storage

class FBServ:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("FBKey.json")
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://gestion-363c6-default-rtdb.firebaseio.com/"
            })

    # ==== USUARIOS ====
    def guardar_usuario(self, usuario):
        ref = db.reference("/usuarios")
        ref.push({
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "contrasena": usuario.contrasena
        })

    # ==== TIENDAS ====
    def guardar_tienda(self, tienda: Tienda):
        ref = db.reference("/tiendas")
        ref.push({
            "nombre": tienda.nombre,
            "categoria": tienda.categoria,
            "direccion": tienda.direccion,
            "propietario": tienda.propietario.nombre
        })

    def obtener_tiendas_por_usuario(self, nombre_usuario):
        ref = db.reference("/tiendas")
        todas = ref.get()
        if not todas:
            return {}
        return {k: t for k, t in todas.items() if t.get("propietario") == nombre_usuario}

    def actualizar_tienda(self, id_tienda, datos_actualizados):
        ref = db.reference(f"/tiendas/{id_tienda}")
        ref.update(datos_actualizados)

    def eliminar_tienda(self, id_tienda):
        ref = db.reference(f"/tiendas/{id_tienda}")
        ref.delete()

    # ==== PRODUCTOS ====
    def agregar_producto(self, id_tienda, producto):
        ref = db.reference(f"/tiendas/{id_tienda}/productos")
        ref.push({
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "ubicacion": producto.ubicacion,
            "imagen_url": producto.imagen_url

        })

    def obtener_productos(self, id_tienda):
        ref = db.reference(f"/tiendas/{id_tienda}/productos")
        productos = ref.get()
        return productos if productos else {}

    def actualizar_producto(self, id_tienda, id_producto, datos_actualizados):
        ref = db.reference(f"/tiendas/{id_tienda}/productos/{id_producto}")
        ref.update(datos_actualizados)

    def eliminar_producto(self, id_tienda, id_producto):
        ref = db.reference(f"/tiendas/{id_tienda}/productos/{id_producto}")
        ref.delete()

    from datetime import datetime

    # ==== FACTURACIÓN ====

    def registrar_factura(self, id_tienda, factura_data):
        ref = db.reference(f"/tiendas/{id_tienda}/ventas")
        return ref.push(factura_data).key

    def obtener_historial_ventas(self, id_tienda):
        ref = db.reference(f"/tiendas/{id_tienda}/ventas")
        ventas = ref.get()
        return ventas if ventas else {}

    def obtener_venta(self, id_tienda, id_venta):
        ref = db.reference(f"/tiendas/{id_tienda}/ventas/{id_venta}")
        venta = ref.get()
        return venta

    def eliminar_venta(self, id_tienda, id_venta):
        ref = db.reference(f"/tiendas/{id_tienda}/ventas/{id_venta}")
        ref.delete()

    def descontar_stocks(self, id_tienda, items):
        for it in items:
            id_producto = it.get("id_producto")
            cantidad = int(it.get("cantidad", 0))
            if not id_producto or cantidad <= 0:
                continue
            prod_ref = db.reference(f"/tiendas/{id_tienda}/productos/{id_producto}")
            producto = prod_ref.get()
            if not producto:
                continue
            stock_actual = int(producto.get("stock", 0))
            nuevo_stock = max(stock_actual - cantidad, 0)
            prod_ref.update({"stock": nuevo_stock})
