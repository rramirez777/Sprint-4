import customtkinter as ctk

class ThemeManager:
    _instance = None
    _subscribers = []
    themes = {
        "light": {
            "bg": "#f2f1d9",
            "button": "#ff751f",
            "text": "#212a3e",
            "card": "#fdf4d5",
            "border": "#d1d1c7"
        },
        "dark": {
            "bg": "#212a3e",
            "button": "#ff9933",
            "text": "#f2f1d9",
            "card": "#2d3852",
            "border": "#000D55"
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.current_theme = ctk.get_appearance_mode().lower()

    # ---------------------------------------------------
    #  SUSCRIPTORES
    # ---------------------------------------------------
    def subscribe(self, callback):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def _notify(self):
        for callback in self._subscribers:
            callback()

    # ---------------------------------------------------
    #   CAMBIO DE TEMA
    # ---------------------------------------------------
    def toggle_theme(self):
        new_mode = "dark" if self.current_theme == "light" else "light"
        self.set_theme(new_mode)

    def set_theme(self, mode: str):
        if mode.lower() not in ("light", "dark"):
            raise ValueError("El tema debe ser 'light' o 'dark'.")

        ctk.set_appearance_mode(mode)
        self.current_theme = mode.lower()

        self._notify()

    # ---------------------------------------------------
    #   GETTERS
    # ---------------------------------------------------
    def get_theme(self) -> str:
        return self.current_theme

    def get_color(self, key: str):
        return self.themes[self.current_theme].get(key)
