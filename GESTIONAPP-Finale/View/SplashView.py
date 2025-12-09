import customtkinter as ctk
import threading
import time
from View.LoginView import LoginView


class SplashView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GestiónApp")
        self.geometry("600x350")
        self.config(bg="#f2f1d9")
        self.overrideredirect(True)  # Sin barra de título

        self.center_window()
        self.create_ui()
        self.after(100, self.animate_loading)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (300)
        y = (self.winfo_screenheight() // 2) - (175)
        self.geometry(f"600x350+{x}+{y}")

    def create_ui(self):
        # Logo / título
        self.logo_label = ctk.CTkLabel(
            self,
            bg_color=("#f2f1d9"),
            text="GestiónApp",
            text_color="#ff751f",
            font=("Segoe UI", 42, "bold")
        )
        self.logo_label.pack(pady=(80, 10))

        # Subtítulo
        self.text_label = ctk.CTkLabel(
            self,
            bg_color=("#f2f1d9"),
            text="Cargando sistema...",
            text_color="#212a3e",
            font=("Segoe UI", 18)
        )
        self.text_label.pack(pady=(0, 30))

        # Barra de carga
        self.progress = ctk.CTkProgressBar(
            self, width=400, height=16, progress_color="#ff751f", corner_radius=0
        )
        self.progress.set(0)
        self.progress.pack(pady=(0, 10))

        # Porcentaje
        self.percent_label = ctk.CTkLabel(
            self,
            bg_color=("#f2f1d9"),
            text="0%",
            text_color="#212a3e",
            font=("Segoe UI", 14)
        )
        self.percent_label.pack()

    def animate_loading(self):
        def run():
            for i in range(100):
                time.sleep(0.02)
                self.progress.set(i / 100)
                self.percent_label.configure(text=f"{min(i, 99)}%")
            time.sleep(1.5)
            self.after(0, self.GoToLogin)
        threading.Thread(target=run, daemon=True).start()
    
    def GoToLogin(self):
        self.destroy()
        login = LoginView()
        login.mainloop()
