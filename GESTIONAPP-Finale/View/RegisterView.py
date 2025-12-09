import customtkinter as ctk
from tkinter import messagebox
from ViewModel.UserViewModel import UserViewModel
from View.LoginView import LoginView
import re

class RegisterView(ctk.CTk):
    bg_color = "#f2f1d9"
    button_color = "#ff751f"
    text1_color = "#212a3e"
    fontxt = ("Segoe UI", 14)

    def __init__(self):
        super().__init__()
        self.title("Registro de Usuario")
        self.geometry("900x550")
        self.config(bg=self.bg_color)
        self.vm_usuario = UserViewModel()
        self.centrar_ventana(900, 550)

        # ====== FRAME PRINCIPAL ======
        frame = ctk.CTkFrame(self, fg_color=self.bg_color, corner_radius=0)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Crear una cuenta nueva", text_color=self.text1_color,
                     font=("Segoe UI", 22, "bold")).pack(pady=20)

        # ====== CAMPOS ======
        ctk.CTkLabel(frame, text="Nombre completo:", text_color=self.text1_color,
                     font=self.fontxt).pack(pady=(10, 5))
        self.nombre_entry = ctk.CTkEntry(frame, width=300)
        self.nombre_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Correo electrónico:", text_color=self.text1_color,
                     font=self.fontxt).pack(pady=(10, 5))
        self.correo_entry = ctk.CTkEntry(frame, width=300)
        self.correo_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Contraseña:", text_color=self.text1_color,
                     font=self.fontxt).pack(pady=(10, 5))
        self.contrasena_entry = ctk.CTkEntry(frame, width=300, show="*")
        self.contrasena_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Confirmar contraseña:", text_color=self.text1_color,
                     font=self.fontxt).pack(pady=(10, 5))
        self.confirmar_entry = ctk.CTkEntry(frame, width=300, show="*")
        self.confirmar_entry.pack(pady=5)

        self.ver_contra = ctk.CTkCheckBox(
            frame, text="Mostrar contraseñas", command=self.toggle_password,
            fg_color=self.button_color, hover_color="#e46816",
            border_color=self.button_color, text_color=self.text1_color,
        )
        self.ver_contra.pack(pady=10)

        # ====== BOTONES ======
        ctk.CTkButton(
            frame, text="Registrar", fg_color=self.button_color,
            text_color=self.bg_color, font=("Segoe UI", 16, "bold"),
            hover_color="#e46816", command=self.registrar_usuario
        ).pack(pady=20)

        ctk.CTkButton(
            frame, text="Volver al inicio de sesión", fg_color="transparent",
            border_width=2, border_color=self.button_color,
            text_color=self.button_color, font=("Segoe UI", 14),
            hover_color="#fff2e6", command=self.volver_login
        ).pack(pady=(0, 15))

    def centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def toggle_password(self):
        mostrar = self.contrasena_entry.cget("show") == "*"
        nuevo_valor = "" if mostrar else "*"
        self.contrasena_entry.configure(show=nuevo_valor)
        self.confirmar_entry.configure(show=nuevo_valor)

    def registrar_usuario(self):
        nombre = self.nombre_entry.get().strip()
        correo = self.correo_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        confirmar = self.confirmar_entry.get().strip()

        # Validaciones básicas
        if not nombre or not correo or not contrasena or not confirmar:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, correo):
            messagebox.showerror("Correo inválido", "Por favor ingresa un correo electrónico válido.")
            return

        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        miss = []
        if len(contrasena) < 8:
            miss.append("Debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", contrasena):
            miss.append("Debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", contrasena):
            miss.append("Debe contener al menos una letra minúscula.")
        if not re.search(r"\d", contrasena):
            miss.append("Debe contener al menos un número.")
        if not re.search(r"[^\w\s]", contrasena):
            miss.append("Debe contener al menos un símbolo o carácter especial.")

        if miss:
            errores = "\n- ".join(miss)
            messagebox.showwarning("Contraseña débil", f"Tu contraseña no cumple con los requisitos:\n\n- {errores}")
            return

        # Registrar usuario
        usuario = self.vm_usuario.registrar_usuario(nombre, correo, contrasena)
        if usuario:
            messagebox.showinfo("Registro exitoso", f"Usuario {usuario.nombre} creado correctamente.")
            self.destroy()
            login = LoginView()
            login.mainloop()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario. Es posible que el correo ya exista.")

    def volver_login(self):
        self.destroy()
        login = LoginView()
        login.mainloop()
