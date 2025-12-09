import customtkinter as ctk
from tkinter import messagebox
from ViewModel.ProductoViewModel import ProductoViewModel
from Core.ThemeManager import ThemeManager
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import filedialog
from Servicios.ImageStorage import ImageStorage, SUPABASE_URL, SUPABASE_KEY
import os
import sdl2
import sdl2.sdlmixer as sdlmixer

class ProductoView(ctk.CTkFrame):
    def __init__(self, parent, id_tienda, volver_callback):
        self.theme = ThemeManager()
        self.storage = ImageStorage(SUPABASE_URL, SUPABASE_KEY)

        super().__init__(parent, fg_color=self.theme.get_color("bg"))

        self.id_tienda = id_tienda
        self.volver_callback = volver_callback
        self.vm_producto = ProductoViewModel(id_tienda)

        self.pack(fill="both", expand=True)
        self.render_ui()

    # UI
    def render_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Productos de la Tienda",
            font=("Segoe UI", 22, "bold"),
            text_color=self.theme.get_color("text"),
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="+ Agregar Producto",
            fg_color=self.theme.get_color("button"),
            text_color=self.theme.get_color("bg"),
            command=self.agregar_producto,
        ).pack(pady=10)

        self.lista_frame = ctk.CTkScrollableFrame(
            self, width=600, height=400,
            fg_color=self.theme.get_color("bg")
        )
        self.lista_frame.pack(pady=10, fill="both", expand=True)

        self.cargar_productos()

        ctk.CTkButton(
            self,
            text="← Volver",
            fg_color=self.theme.get_color("button"),
            text_color=self.theme.get_color("bg"),
            command=lambda: [self.pack_forget(), self.volver_callback()],
        ).pack(pady=10)

    # Sonido que pidio el profe
    def play_demo_sound(self):
        try:
            ruta = os.path.join(os.path.dirname(__file__), "assets", "halo.wav")
            if not os.path.exists(ruta):
                print("No existe halo.wav")
                return

            musica = sdlmixer.Mix_LoadWAV(ruta.encode("utf-8"))
            if musica:
                sdlmixer.Mix_PlayChannel(-1, musica, 0)

        except Exception as e:
            print("Error al reproducir sonido demo:", e)


    # LISTA
    def cargar_productos(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        productos = self.vm_producto.listar_productos()

        # DEMO EXTRA
        productos["test"] = {
            "nombre": "Producto Demo",
            "precio": 999.99,
            "stock": 10,
            "ubicacion": "Tienda X",
            "imagen_url": "https://picsum.photos/id/237/300/300"
        }

        for id_prod, p in productos.items():
            frame = ctk.CTkFrame(
                self.lista_frame,
                fg_color=self.theme.get_color("card"),
                border_color=self.theme.get_color("border"),
                border_width=2,
                corner_radius=8,
            )
            frame.pack(fill="x", padx=10, pady=5)

            content_frame = ctk.CTkFrame(frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=5, pady=5)

            # IMAGEN
            if p.get("imagen_url"):
                try:
                    response = requests.get(p["imagen_url"])
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((80, 80))
                    img_tk = ImageTk.PhotoImage(img)

                    img_label = ctk.CTkLabel(content_frame, image=img_tk, text="")
                    img_label.image = img_tk
                    img_label.pack(side="left", padx=10)

                    # Reproducir el sonidoque pidio el profe (Solo suena en producto demo)
                    if id_prod == "test":
                        img_label.bind("<Enter>", lambda e: self.play_demo_sound())

                except:
                    print(f"No se pudo cargar la imagen de {p['nombre']}")

            # TEXTO
            info = f"{p['nombre']}\n${p['precio']} (Stock: {p['stock']})\n{p['ubicacion']}"
            ctk.CTkLabel(
                content_frame,
                text=info,
                font=("Segoe UI", 15),
                text_color=self.theme.get_color("text"),
                justify="left"
            ).pack(side="left", padx=10)

            # BOTONES
            btns = ctk.CTkFrame(content_frame, fg_color="transparent")
            btns.pack(side="right", padx=5)

            ctk.CTkButton(
                btns, text="Editar", width=70,
                fg_color=self.theme.get_color("button"),
                text_color=self.theme.get_color("bg"),
                command=lambda i=id_prod: self.editar_producto(i),
            ).pack(pady=5)

            ctk.CTkButton(
                btns, text="🗑", width=40,
                fg_color="#c0392b", text_color="white",
                command=lambda i=id_prod: self.eliminar_producto(i),
            ).pack(pady=5)

    # AGREGAR PRODUCTO
    def agregar_producto(self):
        win = ctk.CTkToplevel(self)
        win.title("Nuevo Producto")
        win.geometry("300x420")
        win.configure(fg_color=self.theme.get_color("bg"))

        campos = ["Nombre", "Precio", "Stock", "Ubicación"]
        entries = {}

        for c in campos:
            ctk.CTkLabel(
                win, text=c + ":", text_color=self.theme.get_color("text")
            ).pack(pady=5)

            e = ctk.CTkEntry(win)
            e.pack()
            entries[c.lower()] = e

        # ===== SELECCIÓN DE IMAGEN =====
        ruta_imagen = {"path": None}

        def seleccionar_imagen():
            ruta = filedialog.askopenfilename(
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
            )
            if ruta:
                ruta_imagen["path"] = ruta
                messagebox.showinfo("Imagen", "Imagen seleccionada.")

        ctk.CTkButton(
            win, text="Seleccionar Imagen",
            fg_color=self.theme.get_color("button"),
            command=seleccionar_imagen
        ).pack(pady=10)

        # ===== GUARDAR =====
        def guardar():
            try:
                nombre = entries["nombre"].get()
                precio = float(entries["precio"].get())
                stock = int(entries["stock"].get())
                ubicacion = entries["ubicación"].get()

                if not nombre or not ubicacion:
                    raise ValueError("Campos vacíos.")

                imagen_url = None
                if ruta_imagen["path"]:
                    imagen_url = self.storage.upload_image(
                        ruta_imagen["path"], folder="productos"
                    )

                self.vm_producto.agregar_producto(
                    nombre, precio, stock, ubicacion, imagen_url
                )

                messagebox.showinfo("Éxito", "Producto agregado.")
                win.destroy()
                self.cargar_productos()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(
            win, text="Guardar",
            fg_color=self.theme.get_color("button"),
            text_color=self.theme.get_color("bg"),
            command=guardar
        ).pack(pady=20)

    # EDITAR PRODUCTO 
    def editar_producto(self, id_prod):
        productos = self.vm_producto.db.obtener_productos(self.id_tienda)
        producto = productos.get(id_prod)

        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Editar producto")
        popup.geometry("350x500")
        popup.configure(fg_color=self.theme.get_color("bg"))

        def campo(label, valor):
            ctk.CTkLabel(
                popup, text=label, text_color=self.theme.get_color("text")
            ).pack(pady=5)
            entry = ctk.CTkEntry(popup)
            entry.insert(0, valor)
            entry.pack()
            return entry

        entry_nombre = campo("Nombre:", producto["nombre"])
        entry_precio = campo("Precio:", producto["precio"])
        entry_stock = campo("Stock:", producto["stock"])
        entry_ubicacion = campo("Ubicación:", producto["ubicacion"])

        # CAMBIAR IMAGEN ---
        nueva_imagen_path = {"ruta": None}

        def seleccionar_imagen():
            from tkinter.filedialog import askopenfilename
            ruta = askopenfilename(
                title="Seleccionar nueva imagen",
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
            )
            if ruta:
                nueva_imagen_path["ruta"] = ruta
                lbl_img.configure(text=f"Imagen seleccionada:\n{ruta.split('/')[-1]}")

        ctk.CTkButton(
            popup, text="Seleccionar nueva imagen",
            fg_color=self.theme.get_color("button"),
            command=seleccionar_imagen
        ).pack(pady=10)

        lbl_img = ctk.CTkLabel(
            popup,
            text="(Mantendrá imagen actual si no seleccionas otra)",
            text_color=self.theme.get_color("text")
        )
        lbl_img.pack()

        # ---------------------------------------------------------

        def guardar_cambios():
            try:
                patch = {
                    "nombre": entry_nombre.get(),
                    "precio": float(entry_precio.get()),
                    "stock": int(entry_stock.get()),
                    "ubicacion": entry_ubicacion.get(),
                }

                if nueva_imagen_path["ruta"]:
                    ruta = nueva_imagen_path["ruta"]

                    # ELIMINAR IMAGEN ANTERIOR
                    imagen_vieja = producto.get("imagen_url")
                    if imagen_vieja:
                        try:
                            self.storage.delete_image(imagen_vieja)
                        except Exception as e:
                            print("No se pudo eliminar imagen vieja:", e)

                    # SUBIR IMAGEN NUEVA
                    nueva_url = self.storage.upload_image(ruta, folder="productos")
                    patch["imagen_url"] = nueva_url

                # --- ACTUALIZAR PRODUCTO ---
                self.vm_producto.db.actualizar_producto(self.id_tienda, id_prod, patch)

                messagebox.showinfo("Éxito", "Producto actualizado.")
                popup.destroy()
                self.cargar_productos()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(
            popup, text="Guardar cambios",
            fg_color=self.theme.get_color("button"),
            text_color=self.theme.get_color("bg"),
            command=guardar_cambios
        ).pack(pady=15)

    # ELIMINAR
    def eliminar_producto(self, id_prod):
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            self.vm_producto.db.eliminar_producto(self.id_tienda, id_prod)
            messagebox.showinfo("Eliminado", "Producto eliminado.")
            self.cargar_productos()
