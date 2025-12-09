import customtkinter as ctk
from ViewModel.FacturarViewModel import FacturaViewModel
from tkinter import messagebox
from Core.ThemeManager import ThemeManager

class FacturaView(ctk.CTkFrame):
    def __init__(self, parent, usuario, volver_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.usuario = usuario
        self.vm = FacturaViewModel(usuario.nombre if hasattr(usuario, "nombre") else usuario)
        self.theme = ThemeManager()
        self.fontxt = ("Segoe UI", 14)
        self.volver_callback = volver_callback
        self.apply_theme_colors()
        self.render_ui()

    def apply_theme_colors(self):
        self.bg_color = self.theme.get_color("bg")
        self.button_color = self.theme.get_color("button")
        self.text_color = self.theme.get_color("text")
        self.card = self.theme.get_color("card")
        self.border = self.theme.get_color("border")

    def render_ui(self):
        for w in self.winfo_children():
            w.destroy()

        titulo = ctk.CTkLabel(self, text="Facturación", font=("Segoe UI", 22, "bold"))
        titulo.pack(pady=12)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        ctk.CTkButton(btn_frame, text="+ Nueva Factura", fg_color=self.button_color,
                      text_color=self.bg_color, command=self.nueva_factura).pack(side="left")
        ctk.CTkButton(btn_frame, text="Refrescar historial", fg_color=self.button_color,
                      text_color=self.bg_color, command=self.mostrar_historial).pack(side="left", padx=8)
        if self.volver_callback:
            ctk.CTkButton(btn_frame, text="Volver", fg_color="#888", text_color="white",
                          command=self.volver_callback).pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=self.bg_color)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=12)

        self.mostrar_historial()

    def mostrar_historial(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        tiendas = self.vm.cargar_tiendas_usuario()
        if not tiendas:
            ctk.CTkLabel(self.scroll_frame, text="No tienes tiendas registradas.", font=self.fontxt,
                         text_color=self.text_color).pack(pady=20)
            return

        for nombre_tienda in tiendas:
            id_tienda = self.vm.obtener_id_tienda_por_nombre(nombre_tienda)
            ventas = self.vm.listar_ventas(id_tienda)
            frame_t = ctk.CTkFrame(self.scroll_frame, fg_color=self.card,
                                   border_color=self.border, border_width=1, corner_radius=8)
            frame_t.pack(fill="x", pady=8)

            ctk.CTkLabel(frame_t, text=nombre_tienda, font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=6)

            if not ventas:
                ctk.CTkLabel(frame_t, text="No hay ventas por ahora.", font=self.fontxt, text_color=self.text_color).pack(padx=10, pady=6)
                continue

            for id_venta, venta in ventas.items():
                sub = f"{venta.get('fecha','')}  •  Total: {venta.get('total',0)}"
                venta_frame = ctk.CTkFrame(frame_t, fg_color=self.bg_color, corner_radius=6)
                venta_frame.pack(fill="x", padx=10, pady=6)

                ctk.CTkLabel(venta_frame, text=sub, font=("Segoe UI", 12)).pack(side="left", padx=10)

                btns = ctk.CTkFrame(venta_frame, fg_color="transparent")
                btns.pack(side="right", padx=6)
                ctk.CTkButton(btns, text="Ver", width=70, fg_color=self.button_color,
                              command=lambda tid=id_tienda, vid=id_venta: self.ver_detalle(tid, vid)).pack(side="left", padx=6)
                ctk.CTkButton(btns, text="Eliminar", width=90, fg_color="#c0392b",
                              command=lambda tid=id_tienda, vid=id_venta: self.eliminar_venta(tid, vid)).pack(side="left")

    # ---- Nueva factura ----
    def nueva_factura(self):
        win = ctk.CTkToplevel(self)
        win.title("Nueva Factura")
        win.geometry("700x680")
        win.grab_set()

        # aplicar colores
        self.apply_theme_colors()
        win.configure(fg_color=self.bg_color)

        # TIENDA 
        ctk.CTkLabel(
            win, text="Tienda:", font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        tiendas = self.vm.cargar_tiendas_usuario()
        tienda_var = ctk.StringVar()

        tienda_border = ctk.CTkFrame(
            win, fg_color=self.border, corner_radius=8
        )
        tienda_border.pack(pady=6)

        tienda_combo = ctk.CTkOptionMenu(
            tienda_border,
            values=tiendas,
            variable=tienda_var,
            width=300,
            fg_color=self.card,
            button_color=self.card,
            text_color=self.text_color
        )
        tienda_combo.pack(padx=2, pady=2)

        # PRODUCTO 
        ctk.CTkLabel(
            win, text="Producto:", font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        prod_border = ctk.CTkFrame(
            win, fg_color=self.border, corner_radius=8
        )
        prod_border.pack(pady=6)

        producto_var = ctk.StringVar()
        producto_combo = ctk.CTkOptionMenu(
            prod_border,
            values=[],
            variable=producto_var,
            width=300,
            fg_color=self.card,
            button_color=self.card,
            text_color=self.text_color
        )
        producto_combo.pack(padx=2, pady=2)

        # STOCK
        stock_label = ctk.CTkLabel(
            win, 
            text="Stock disponible: ---",
            font=self.fontxt, text_color=self.text_color
        )
        stock_label.pack(pady=4)

        # actualizar stock 
        def actualizar_stock(*_):
            sel = producto_var.get()
            if not sel or not hasattr(producto_combo, "mapping"):
                stock_label.configure(text="Stock disponible: ---")
                return
            
            pid = producto_combo.mapping.get(sel)
            if not pid:
                stock_label.configure(text="Stock disponible: ---")
                return

            data = self.vm.productos_cache.get(pid)
            if not data:
                stock_label.configure(text="Stock disponible: ---")
                return

            stock_label.configure(text=f"Stock disponible: {data.get('stock', 0)}")

        producto_var.trace_add("write", actualizar_stock)

        # CANTIDAD 
        ctk.CTkLabel(
            win, text="Cantidad:", font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        cantidad_entry = ctk.CTkEntry(
            win, width=100,
            fg_color=self.card,
            text_color=self.text_color,
            border_color=self.button_color
        )
        cantidad_entry.pack(pady=6)

        #  ITEMS 
        items_frame = ctk.CTkFrame(
            win, fg_color=self.bg_color,
            border_color=self.button_color,
            border_width=2
        )
        items_frame.pack(fill="both", expand=True, padx=10, pady=10)

        items_listbox = ctk.CTkTextbox(
            items_frame, width=500, height=180,
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.button_color
        )
        items_listbox.pack(padx=6, pady=6)

        # TOTAL 
        total_var = ctk.StringVar(value="0.0")

        ctk.CTkLabel(
            win, text="Total:", font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        total_lbl = ctk.CTkLabel(
            win, textvariable=total_var, font=self.fontxt,
            text_color=self.text_color
        )
        total_lbl.pack()


        # cargar productos 
        def cargar_productos_para_tienda():
            nombre = tienda_var.get()
            if not nombre:
                return
            
            idt = self.vm.obtener_id_tienda_por_nombre(nombre)
            if not idt:
                return
            
            # obtener productos
            productos = self.vm.cargar_productos(idt)

            self.vm.productos_cache = productos if productos else {}

            prods = []
            mapping = {}

            for pid, p in self.vm.productos_cache.items():
                texto = f"{p.get('nombre')} | {pid}"
                prods.append(texto)
                mapping[texto] = pid
            
            producto_combo.configure(values=prods)
            producto_combo.mapping = mapping

            stock_label.configure(text="Stock disponible: ---")

        tienda_var.trace_add("write", lambda *_: cargar_productos_para_tienda())

        # agregar item al carrito
        def agregar_item_ui():
            sel = producto_var.get()
            if not sel:
                messagebox.showwarning("Producto", "Selecciona un producto")
                return

            mapping = getattr(producto_combo, "mapping", {})
            id_prod = mapping.get(sel)
            if not id_prod:
                messagebox.showwarning("Producto", "Producto inválido")
                return

            try:
                qty = int(cantidad_entry.get())
            except:
                messagebox.showwarning("Cantidad", "Cantidad inválida")
                return

            prod = self.vm.productos_cache.get(id_prod)
            stock_actual = int(prod.get("stock", 0)) if prod else 0

            if qty > stock_actual:
                messagebox.showwarning("Stock", f"Stock insuficiente (disp: {stock_actual})")
                return

            try:
                self.vm.agregar_item_al_carrito(id_prod, qty)

                items_listbox.delete("0.0", "end")
                for it in self.vm.cart:
                    items_listbox.insert(
                        "end",
                        f"{it.nombre}  x{it.cantidad}  @ {it.precio_unitario}  -> {it.subtotal}\n"
                    )

                total_var.set(str(self.vm.obtener_total()))

                # actualizar stock
                nuevo_stock = stock_actual - qty
                stock_label.configure(text=f"Stock disponible: {nuevo_stock}")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # eliminar item del carrito
        def quitar_item_ui():
            sel = producto_var.get()
            mapping = getattr(producto_combo, "mapping", {})
            id_prod = mapping.get(sel)
            if not id_prod:
                messagebox.showwarning("Eliminar", "Selecciona un producto a eliminar")
                return

            self.vm.eliminar_item_del_carrito(id_prod)

            items_listbox.delete("0.0", "end")
            for it in self.vm.cart:
                items_listbox.insert(
                    "end",
                    f"{it.nombre}  x{it.cantidad}  @ {it.precio_unitario}  -> {it.subtotal}\n"
                )

            total_var.set(str(self.vm.obtener_total()))

        # facturar
        def facturar_ui():
            if not tienda_var.get():
                messagebox.showwarning("Tienda", "Selecciona una tienda")
                return

            try:
                key = self.vm.guardar_factura_completa()
                messagebox.showinfo("OK", f"Factura registrada: {key}")
                win.destroy()
                self.mostrar_historial()
            except Exception as e:
                messagebox.showerror("Error al facturar", str(e))

        # =============== BOTONES ===================
        btn_frame = ctk.CTkFrame(win, fg_color=self.bg_color)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Agregar", command=agregar_item_ui,
            fg_color=self.button_color, text_color=self.text_color
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame, text="Quitar", command=quitar_item_ui,
            fg_color=self.button_color, text_color=self.text_color
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            btn_frame, text="Facturar", command=facturar_ui,
            fg_color=self.button_color, text_color=self.text_color
        ).grid(row=0, column=2, padx=10)

    # ---- Ver detalle ----
    
    def ver_detalle(self, id_tienda, id_venta):
        venta = self.vm.obtener_detalle_venta(id_tienda, id_venta)
        if not venta:
            messagebox.showwarning("Detalle", "Venta no encontrada")
            return

        win = ctk.CTkToplevel(self)
        win.title("Detalle de Venta")
        win.geometry("500x420")
        win.grab_set()
        win.configure(fg_color=self.bg_color)

        ctk.CTkLabel(
            win, text=f"Venta: {id_venta}",
            font=("Segoe UI", 14, "bold"),
            text_color=self.text_color
        ).pack(pady=6)

        ctk.CTkLabel(
            win, text=f"Fecha: {venta.get('fecha')}",
            font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        ctk.CTkLabel(
            win, text=f"Total: {venta.get('total')}",
            font=self.fontxt,
            text_color=self.text_color
        ).pack(pady=6)

        frame_items = ctk.CTkFrame(
            win,
            fg_color=self.button_color,
            corner_radius=10
        )
        frame_items.pack(fill="both", expand=True, padx=10, pady=8)

        txt = ctk.CTkTextbox(
            frame_items,
            width=460,
            height=250,
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.text_color,
            border_width=2
        )
        txt.pack(padx=6, pady=6, fill="both", expand=True)

        items = venta.get("items", {})
        for k, it in items.items():
            txt.insert(
                "end",
                f"{it.get('nombre')}  x{it.get('cantidad')}  @ {it.get('precio_unitario')}  -> {it.get('subtotal')}\n"
            )

        txt.configure(state="disabled")

    # ---- Eliminar ----
    def eliminar_venta(self, id_tienda, id_venta):
        confirm = messagebox.askyesno("Confirmar", "Eliminar esta venta? (no restaurará stock)")
        if not confirm:
            return
        self.vm.eliminar_factura(id_tienda, id_venta)
        messagebox.showinfo("Eliminada", "Venta eliminada")
        self.mostrar_historial()
