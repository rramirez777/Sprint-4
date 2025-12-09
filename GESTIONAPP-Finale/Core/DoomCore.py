import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os
import sys
import os
raiz = os.path.dirname(os.path.abspath(sys.argv[0]))  
exe_path = os.path.join(raiz, "DOOM", "chocolate-doom.exe")



class DoomEasterEgg(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("DOOM Easter Egg")
        self.geometry("600x400")
        self.configure(fg_color="#000000")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="¡DOOM!",
            font=("Wingdings", 54, "bold"),
            text_color="#ff0000"
        ).pack(pady=40)


    def iniciar_doom(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            exe_path = os.path.join(base_dir,  "DOOM", "chocolate-doom.exe")
            wad_path = os.path.join(base_dir,  "DOOM", "doom1.wad")  

            if not os.path.exists(exe_path):
                messagebox.showerror("Error", "❌ No se encontró Chocolate Doom")
                return

            if not os.path.exists(wad_path):
                messagebox.showerror("Error", "❌ No se encontró el WAD de DOOM")
                return

            subprocess.Popen([exe_path, "-iwad", wad_path])
            print("✔ Chocolate Doom iniciado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar Chocolate Doom:\n{e}")