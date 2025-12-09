class Producto:
    def __init__(self, nombre, precio, stock, ubicacion, imagen_url=None):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.ubicacion = ubicacion
        self.imagen_url = imagen_url  

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "ubicacion": self.ubicacion,
            "imagen_url": self.imagen_url  
        }

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} (Stock: {self.stock}) (Ubicacion: {self.ubicacion})"
