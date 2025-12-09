import customtkinter as ctk
from tkinter import messagebox
from View.TiendasView import TiendaView
from View.ConfigView import ConfigView
from View.MainFrameView import MainFrameView
from Core.DoomCore import DoomEasterEgg
from View.EasterEggView import EasterEggView
from Core.ThemeManager import ThemeManager
from Core.konami_detector import KonamiDetector
from Core.halo_detector import HaloCodeDetector
from Core.sdl_loader import cargar_sdl3
from Core.DoomCore import DoomEasterEgg

import os
import sdl2
import sdl2.sdlmixer as sdlmixer

class BaseView(ctk.CTk):
    fontxt = ("Segoe UI", 14)

    def __init__(self, titulo="Ventana", ancho=1000, alto=640, usuario=None):
        super().__init__()

        # === Easter egg y Halo code
        self.konami = KonamiDetector(self.activar_doom)
        self.halo_code = HaloCodeDetector(self.reproducir_halo_music)
        self.bind_all("<KeyPress>", self.detectar_tecla)

        # === Usuario y tema
        self.usuario = usuario
        self.theme = ThemeManager()
        self.bg_color = self.theme.get_color("bg")
        self.button_color = self.theme.get_color("button")
        self.text1_color = self.theme.get_color("text")

        # === Ventana
        self.title(titulo)
        self.geometry(f"{ancho}x{alto}")
        self.configure(fg_color=self.bg_color)
        self.update_idletasks()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        # === Encabezado
        self.encabezado = ctk.CTkFrame(self, fg_color=self.button_color, height=60, corner_radius=0)
        self.encabezado.pack(fill="x", side="top")

        self.btn_menu = ctk.CTkButton(
            self.encabezado, text="☰", width=40, height=40,
            fg_color=self.bg_color, text_color=self.button_color,
            font=("Segoe UI", 22, "bold"), hover_color="#e5e4cb",
            command=self.toggle_menu
        )
        self.btn_menu.pack(side="left", padx=10, pady=5)

        self.titulo_label = ctk.CTkLabel(
            self.encabezado, text=titulo,
            text_color=self.bg_color,
            font=("Segoe UI", 20, "bold")
        )
        self.titulo_label.place(relx=0.5, rely=0.5, anchor="center")

        # === Menú lateral
        self.menu_visible = True
        self.menuLateral = ctk.CTkFrame(self, fg_color=self.button_color, width=220, corner_radius=0)
        self.menuLateral.pack(fill="y", side="left")

        buttons = [
            ("Inicio", self.ir_inicio),
            ("Tiendas", self.ir_tiendas),
            ("Facturar", self.ir_facturar),
            ("Configuración", self.ir_configuracion),
            ("Chat", self.ir_chat),
            ("Salir", self.salir),
        ]
        for texto, comando in buttons:
            btn = ctk.CTkButton(
                self.menuLateral, text=texto, command=comando,
                fg_color=self.button_color, text_color=self.bg_color,
                font=("Segoe UI", 20, "bold"), hover_color="#e46816"
            )
            btn.pack(pady=10, padx=10, fill="x")

        # === Contenido principal
        self.main_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_frame.pack(side="right", expand=True, fill="both")

    # =========================
    # Temas
    # =========================
    def cambiar_tema(self):
        self.theme.toggle_theme()
        self.bg_color = self.theme.get_color("bg")
        self.button_color = self.theme.get_color("button")
        self.text1_color = self.theme.get_color("text")
        self.aplicar_tema()
        self.update_idletasks()

    def aplicar_tema(self):
        self.configure(fg_color=self.bg_color)
        self.menuLateral.configure(fg_color=self.button_color)
        self.encabezado.configure(fg_color=self.button_color)
        self.titulo_label.configure(text_color=self.bg_color)
        self.main_frame.configure(fg_color=self.bg_color)
        for widget in self.menuLateral.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=self.button_color, text_color=self.bg_color)

    # =========================
    # Navegación
    # =========================
    def toggle_menu(self):
        if self.menu_visible:
            self.menuLateral.pack_forget()
            self.menu_visible = False
        else:
            self.menuLateral.pack(fill="y", side="left")
            self.menu_visible = True

    def mostrar_vista(self, vista_class, **kwargs):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        vista = vista_class(self.main_frame, self.usuario, **kwargs)
        vista.pack(fill="both", expand=True)

    def ir_inicio(self):
        self.mostrar_vista(MainFrameView)

    def ir_tiendas(self):
        self.mostrar_vista(TiendaView)

    def ir_configuracion(self):
        self.mostrar_vista(ConfigView, cambiar_tema_callback=self.cambiar_tema, cerrar_sesion_callback=self.LogOut)

    def LogOut(self):
        self.destroy()
        from View.LoginView import LoginView
        login = LoginView()
        login.mainloop()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres cerrar la aplicación?"):
            self.destroy()

    # =========================
    # Teclas y Easter Egg
    # =========================
    def detectar_tecla(self, event):
        key = event.keysym.lower() if event.keysym.isalpha() else event.keysym
        self.konami.key_pressed(key)
        self.halo_code.key_pressed(key)
        print("Tecla:", event.keysym)


    def activar_doom(self):
        try:
            self.efecto_alerta_doom()  # hace parpadear y cambiar texto
            doom_window = DoomEasterEgg()
            doom_window.iniciar_doom()
        except Exception as e:
            print("❌ Error al activar DOOM:", e)

    def efecto_alerta_doom(self, veces=6, delay=200, texto_alerta="¡HELL IS COMING!"):
        texto_original = self.titulo_label.cget("text")  

        def parpadear(contador):
            if contador > 0:
                color = "#ff0000" if contador % 2 == 0 else self.theme.get_color("button")
                texto = texto_alerta if contador % 2 == 0 else texto_original

                self.encabezado.configure(fg_color=color)
                self.titulo_label.configure(text=texto)

                self.after(delay, parpadear, contador - 1)
            else:
                self.encabezado.configure(fg_color=self.theme.get_color("button"))
                self.titulo_label.configure(text=texto_original)

        parpadear(veces)


    def activar_easter_egg(self):
        if cargar_sdl3():
            EasterEggView()
        else:
            EasterEggView()

    # =========================
    # Reproducir Halo Theme 
    # =========================
    def reproducir_halo_music(self):
        try:
            if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
                print("Error inicializando SDL2:", sdl2.SDL_GetError())
                return

            if sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 2048) != 0:
                print("Error inicializando SDL_mixer:", sdlmixer.Mix_GetError())
                return

            ruta = os.path.join(os.path.dirname(__file__), "assets", "halo.wav")
            if not os.path.exists(ruta):
                print(f"Archivo de música no encontrado: {ruta}")
                return

            musica = sdlmixer.Mix_LoadWAV(ruta.encode("utf-8"))
            if not musica:
                print("Error cargando música:", sdlmixer.Mix_GetError())
                return

            sdlmixer.Mix_PlayChannel(-1, musica, 0)
            print("🎵 Reproduciendo Halo Theme!")

        except ImportError:
            print("PySDL2 no está instalado. Ejecuta: pip install PySDL2 pysdl2-dll==2.26.5")
        except Exception as e:
            print("Error al reproducir música:", e)

    # =========================
    # Chat
    # =========================

    def ir_chat(self):
        from View.ChatView import ChatView
        from Servicios.ChatService import ChatService
        from ViewModel.ChatViewModel import ChatViewModel

        if not hasattr(self, 'chat_vm') or self.chat_vm is None:
            self.chat_vm = ChatViewModel(self.usuario.nombre, ChatService())

        self.mostrar_vista(ChatView, view_model=self.chat_vm)



    def ir_facturar(self):
        from View.FacturarView import FacturaView
        self.mostrar_vista(FacturaView)
