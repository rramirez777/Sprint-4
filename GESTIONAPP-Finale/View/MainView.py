from View.BasedView import BaseView
import customtkinter as ctk
from PIL import Image
import os
from Core.ThemeManager import ThemeManager

class MainView(BaseView):
    def __init__(self, usuario=None):
        super().__init__(titulo="GestionApp", usuario=usuario)

        self.theme = ThemeManager()
        self.bg_color = self.theme.get_color("bg")
        self.text_color = self.theme.get_color("text")
        self.main_frame.configure(fg_color=self.bg_color)

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        card = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_color,
            corner_radius=12,
            border_width=2,
            border_color=self.theme.get_color("button")
        )
        card.pack(padx=40, pady=40, fill="both", expand=True)

        # === Texto de bienvenida ===
        bienvenida = f"¡Bienvenido, {usuario.nombre if usuario else 'usuario'}!"
        ctk.CTkLabel(
            card,
            text=bienvenida,
            text_color=self.text_color,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            card,
            text="¡Esperamos que tengas un excelente día! :D",
            text_color=self.text_color,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(0, 40))

        # === Logo (claro/oscuro) ===
        self.logo_placeholder = ctk.CTkFrame(
            card,
            width=200,
            height=200,
            fg_color="#ffffff" if self.theme.get_theme() == "light" else "#2b2b2b",
            corner_radius=20,
            border_width=2,
            border_color=self.theme.get_color("button")
        )
        self.logo_placeholder.pack(pady=(0, 30))

        try:
            base_dir = os.path.join(os.path.dirname(__file__), "assets")
            light_path = os.path.join(base_dir, "logo_light.png")
            dark_path = os.path.join(base_dir, "logo_dark.png")

            if not os.path.exists(light_path) or not os.path.exists(dark_path):
                raise FileNotFoundError(f"Logo files not found at {base_dir}")

            logo_image = ctk.CTkImage(
                light_image=Image.open(light_path),
                dark_image=Image.open(dark_path),
                size=(240, 222)
            )

            self.logo_image = logo_image

            self.logo_label = ctk.CTkLabel(
                self.logo_placeholder,
                image=self.logo_image,
                text=""
            )
            self.logo_label.pack(expand=True)
        except Exception as e:
            print(f"❌ No se pudo cargar la imagen del logo: {e}")
            ctk.CTkLabel(
                self.logo_placeholder,
                text="Logo\nno disponible",
                text_color=self.text_color,
                font=("Segoe UI", 14, "bold"),
                justify="center"
            ).pack(expand=True)

        # === Descripción ===
        ctk.CTkLabel(
            card,
            text=(
                "Esta es la pantalla principal de tu aplicación.\n"
                "Desde aquí podrás acceder a las Tiendas, la Configuración y más opciones\n"
                "usando el menú lateral."
            ),
            text_color=self.text_color,
            font=self.fontxt,
            justify="center"
        ).pack(pady=20, padx=20)
