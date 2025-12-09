import customtkinter as ctk
from tkinter import messagebox
from ViewModel.UserViewModel import UserViewModel
from View.MainView import MainView

class LoginView(ctk.CTk):
    bg_color = "#f2f1d9"
    button_color = "#ff751f"
    text1_color = "#212a3e"
    fontxt = ("Segoe UI", 14)

    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("900x500")
        self.config(bg=self.bg_color)
        self.vm_usuario = UserViewModel()
        self.centrar_ventana(900, 500)

        # ====== CAMPOS DE LOGIN ======
        frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Correo electrónico:", text_color=self.text1_color, font=self.fontxt).pack(pady=15)
        self.correo_entry = ctk.CTkEntry(frame, width=300)
        self.correo_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Contraseña:", text_color=self.text1_color, font=self.fontxt).pack(pady=15)
        self.contrasena_entry = ctk.CTkEntry(frame, width=300, show="*")
        self.contrasena_entry.pack(pady=5)

        self.ver_contra = ctk.CTkCheckBox(
            frame, text="Mostrar contraseña", command=self.toggle_password,
            fg_color=self.button_color, hover_color="#e46816",
            border_color=self.button_color, text_color=self.text1_color,
        )
        self.ver_contra.pack(pady=10)

        login_btn = ctk.CTkButton(
            frame, text="Ingresar", fg_color=self.button_color,
            text_color=self.bg_color, font=("Segoe UI", 16, "bold"),
            hover_color="#e46816", command=self.login
        )
        login_btn.pack(pady=30)

        ctk.CTkButton(
            frame, text="Crear cuenta nueva", fg_color="transparent",
            border_width=2, border_color=self.button_color,
            text_color=self.button_color, font=("Segoe UI", 14),
            hover_color="#fff2e6", command=self.abrir_registro
        ).pack(pady=(0, 15))

    def centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def toggle_password(self):
        current = self.contrasena_entry.cget("show")
        self.contrasena_entry.configure(show="" if current == "*" else "*")

    def abrir_registro(self):
        from View.RegisterView import RegisterView
        self.destroy()
        registro = RegisterView()
        registro.mainloop()

    def login(self):
        correo = self.correo_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if not correo or not contrasena:
            messagebox.showwarning("Campos vacíos", "Debes ingresar ambos campos.")
            return

        usuario = self.vm_usuario.iniciar_sesion(correo, contrasena)

        if usuario:
            messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario.correo}")
            self.destroy()
            main = MainView(usuario)
            main.mainloop()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
