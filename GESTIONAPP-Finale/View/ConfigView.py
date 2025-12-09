import customtkinter as ctk

class ConfigView(ctk.CTkFrame):
    def __init__(self, parent, usuario=None, cambiar_tema_callback=None, cerrar_sesion_callback=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.usuario = usuario
        self.cambiar_tema_callback = cambiar_tema_callback
        self.cerrar_sesion_callback = cerrar_sesion_callback

        self.label = ctk.CTkLabel(self, text="Configuración", font=("Segoe UI", 24, "bold"))
        self.label.pack(pady=20)

        # Botón tema
        self.btn_tema = ctk.CTkButton(
            self, text="Cambiar tema", 
            command=self.cambiar_tema_callback,
            fg_color="#ff751f", text_color="white"
        )
        self.btn_tema.pack(pady=10)

        # Botón cerrar sesión
        self.btn_logout = ctk.CTkButton(
            self, text="Cerrar sesión", 
            command=self.cerrar_sesion_callback,
            fg_color="#e53935", text_color="white"
        )
        self.btn_logout.pack(pady=10)
