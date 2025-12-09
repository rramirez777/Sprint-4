import customtkinter as ctk

class EasterEggView(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Easter Egg 🎮")
        self.geometry("400x300")

        ctk.CTkLabel(
            self,
            text="¡Konami Code activado!\nSDL3 cargado correctamente 🎉",
            font=("Segoe UI", 20, "bold")
        ).pack(expand=True)
