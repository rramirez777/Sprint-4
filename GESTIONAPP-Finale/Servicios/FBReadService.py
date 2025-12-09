import firebase_admin
from firebase_admin import credentials, db

class FBReadService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("FBKey.json")
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://gestion-363c6-default-rtdb.firebaseio.com/"
            })

    def obtener_tiendas_por_usuario(self, nombre_usuario):
        ref = db.reference("/tiendas")
        todas = ref.get()
        if not todas:
            return {}
        return {k: t for k, t in todas.items() if t.get("propietario") == nombre_usuario}


    def obtener_tienda_por_nombre(self, nombre, usuario):
        tiendas = self.obtener_tiendas_por_usuario(usuario)
        for id_t, info in tiendas.items():
            if info.get("nombre", "").lower() == nombre.lower():
                return {"id": id_t, **info}
        return None


    # ----------------------------------------
    def obtener_productos_de_tienda(self, id_tienda, usuario):
        tiendas = self.obtener_tiendas_por_usuario(usuario)

        if id_tienda not in tiendas:
            return {}  

        ref = db.reference(f"/tiendas/{id_tienda}/productos")
        productos = ref.get()
        return productos if productos else {}


    def buscar_producto(self, texto, usuario):
        texto = texto.lower()
        coincidencias = []

        tiendas = self.obtener_tiendas_por_usuario(usuario)

        for id_t, info_tienda in tiendas.items():
            productos = info_tienda.get("productos", {})
            for id_p, info_prod in productos.items():
                if texto in info_prod.get("nombre", "").lower():
                    coincidencias.append({
                        "tienda_id": id_t,
                        "tienda_nombre": info_tienda.get("nombre"),
                        "producto_id": id_p,
                        "producto": info_prod
                    })

        return coincidencias
    
    def obtener_ventas_por_usuario(self, nombre_usuario):
        ref_tiendas = db.reference("/tiendas")
        tiendas = ref_tiendas.get()
        if not tiendas:
            return {}

        ventas_por_usuario = {}

        tiendas_usuario = {k: v for k, v in tiendas.items() if v.get("propietario") == nombre_usuario}

        for id_tienda, tienda in tiendas_usuario.items():
            ref_ventas = db.reference(f"/tiendas/{id_tienda}/ventas")
            ventas = ref_ventas.get()
            if ventas:
                ventas_por_usuario[id_tienda] = ventas

        return ventas_por_usuario
