import customtkinter as ctk
from ViewModel.TiendaViewModel import TiendaViewModel
from tkinter import messagebox
from View.ProductView import ProductoView
from Core.ThemeManager import ThemeManager

class TiendaView(ctk.CTkFrame):  
    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent")
        self.usuario = usuario
        self.vm_tienda = TiendaViewModel(usuario)
        
        self.theme = ThemeManager()

        self.fontxt = ("Segoe UI", 14)

        self.render_ui()

    def apply_theme_colors(self):
        self.bg_color = self.theme.get_color("bg")
        self.button_color = self.theme.get_color("button")
        self.text1_color = self.theme.get_color("text")

    def render_ui(self):
        self.apply_theme_colors()

        for widget in self.winfo_children():
            widget.destroy()

        titulo = ctk.CTkLabel(self, text="Tus Tiendas", font=("Segoe UI", 22, "bold"))
        titulo.pack(pady=20)

        btn_nueva = ctk.CTkButton(self, text="+ Nueva Tienda", fg_color=self.button_color,
                                  text_color=self.bg_color, font=("Segoe UI", 16, "bold"),
                                  hover_color="#e46816", command=self.agregar_tienda)
        btn_nueva.pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=self.bg_color)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.mostrar_tiendas()

    def mostrar_tiendas(self):
        self.apply_theme_colors()

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tiendas = self.vm_tienda.listar_tiendas()
        if not tiendas:
            ctk.CTkLabel(self.scroll_frame, text="No tienes tiendas registradas.",
                         text_color=self.text1_color, font=self.fontxt).pack(pady=20)
            return

        for id_tienda, t in tiendas:

            frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=self.theme.get_color("card"),
                border_color=self.theme.get_color("border"),
                border_width=2,
                corner_radius=8,
            )
            frame.pack(fill="x", padx=2, pady=2)

            info = f"{t['nombre']} - {t['categoria']}\n{t['direccion']}"
            lbl = ctk.CTkLabel(
                frame,
                text=info,
                text_color=self.text1_color,
                font=self.fontxt,
                anchor="w",
                justify="left"
            )
            lbl.pack(side="left", padx=15, pady=10, expand=True, fill="x")

            btn_opciones = ctk.CTkButton(
                frame,         
                text="⋮",
                width=40,
                fg_color=self.button_color,
                text_color=self.bg_color,
                hover_color="#e46816",
                command=lambda i=id_tienda, t=t: self.menu_opciones(i, t)
            )
            btn_opciones.pack(side="right", padx=10, pady=10)

    def menu_opciones(self, id_tienda, tienda_data):
        win = ctk.CTkToplevel(self)
        win.title("Opciones")
        win.geometry("250x200")
        win.grab_set()

        ctk.CTkLabel(win, text=f"{tienda_data['nombre']}", font=("Segoe UI", 16, "bold")).pack(pady=20)

        ctk.CTkButton(win, text="Editar", fg_color=self.button_color, text_color=self.bg_color,
                      command=lambda: [win.destroy(), self.editar_tienda(id_tienda, tienda_data)]).pack(pady=5)

        ctk.CTkButton(win, text="Eliminar", fg_color="#c0392b", text_color="white",
                      command=lambda: [win.destroy(), self.eliminar_tienda(id_tienda, tienda_data)]).pack(pady=5)

        ctk.CTkButton(win, text="Ver productos", fg_color="#2980b9", text_color="white",
                      command=lambda: [win.destroy(), self.ver_productos(id_tienda)]).pack(pady=5)

    def agregar_tienda(self):
        win = ctk.CTkToplevel(self)
        win.title("Registrar Tienda")
        win.geometry("400x400")
        win.grab_set()

        self.apply_theme_colors()

        campos = {}
        for texto in ["Nombre", "Categoría", "Dirección"]:
            ctk.CTkLabel(win, text=texto + ":", text_color=self.text1_color, font=self.fontxt).pack(pady=5)
            entry = ctk.CTkEntry(win, width=300)
            entry.pack(pady=5)
            campos[texto.lower()] = entry

        def registrar():
            nombre = campos["nombre"].get().strip()
            cat = campos["categoría"].get().strip()
            dir = campos["dirección"].get().strip()

            if not nombre or not cat or not dir:
                messagebox.showwarning("Campos vacíos", "Completa todos los campos")
                return
            
            self.vm_tienda.registrar_tienda(nombre, cat, dir)
            messagebox.showinfo("Éxito", "Tienda registrada correctamente")
            win.destroy()
            self.mostrar_tiendas()

        ctk.CTkButton(win, text="Guardar", fg_color=self.button_color,
                      text_color=self.bg_color, command=registrar).pack(pady=20)

    def editar_tienda(self, id_tienda, tienda_data):
        win = ctk.CTkToplevel(self)
        win.title("Editar Tienda")
        win.geometry("400x400")
        win.grab_set()

        self.apply_theme_colors()

        campos = {}
        for texto, valor in [("Nombre", tienda_data["nombre"]),
                             ("Categoría", tienda_data["categoria"]),
                             ("Dirección", tienda_data["direccion"])]:
            ctk.CTkLabel(win, text=texto + ":", font=self.fontxt).pack(pady=5)
            entry = ctk.CTkEntry(win, width=300)
            entry.insert(0, valor)
            entry.pack(pady=5)
            campos[texto.lower()] = entry

        def guardar():
            nombre = campos["nombre"].get().strip()
            cat = campos["categoría"].get().strip() 
            dir = campos["dirección"].get().strip()

            patch = {"nombre": nombre, "categoria": cat, "direccion": dir}
            self.vm_tienda.db.actualizar_tienda(id_tienda, patch)
            messagebox.showinfo("Éxito", "Tienda actualizada correctamente")
            win.destroy()
            self.mostrar_tiendas()

        ctk.CTkButton(win, text="Guardar cambios", fg_color=self.button_color,
                      text_color=self.bg_color, command=guardar).pack(pady=20)

    def eliminar_tienda(self, id_tienda, tienda_data):
        confirm = messagebox.askyesno("Confirmar eliminación",
                                      f"¿Eliminar la tienda '{tienda_data['nombre']}'?")
        if confirm:
            self.vm_tienda.db.eliminar_tienda(id_tienda)
            messagebox.showinfo("Eliminada", "Tienda eliminada correctamente")
            self.mostrar_tiendas()

    def ver_productos(self, id_tienda):
        self.pack_forget()  
        ProductoView(self.master, id_tienda, lambda: self.pack(fill="both", expand=True))