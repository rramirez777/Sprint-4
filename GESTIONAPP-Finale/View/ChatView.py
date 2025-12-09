import customtkinter as ctk
from Servicios.ChatService import ChatService
from ViewModel.ChatViewModel import ChatViewModel
from Core.ThemeManager import ThemeManager  


class ChatView(ctk.CTkFrame):
    def __init__(self, parent, usuario=None, view_model=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.usuario = usuario
        self.vm = view_model  

        self.theme = ThemeManager()  
        self._apply_theme()
        self._build_ui()
        self.render_chat_history()

    def _apply_theme(self):
        t = self.theme

        self.bg_color = t.get_color("bg")
        self.text_color = t.get_color("text")
        self.card_color = t.get_color("card")
        self.border_color = t.get_color("border")
        self.button_color = t.get_color("button")

        self.configure(fg_color=self.bg_color)

    # -------------------------------------------
    # UI
    # -------------------------------------------
    def _build_ui(self):
        # HEADER
        self.header = ctk.CTkFrame(self, fg_color=self.card_color, height=50, corner_radius=8)
        self.header.pack(fill="x", padx=12, pady=(12, 6))

        self.title = ctk.CTkLabel(
            self.header,
            text="Chat — Assistant (Local)",
            anchor="w",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.text_color
        )
        self.title.pack(side="left", padx=(8,0))

        # MAIN
        self.main = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # CHAT AREA
        self.chat_area = ctk.CTkTextbox(
            self.main,
            wrap="word",
            width=800,
            height=420,
            corner_radius=10,
            fg_color=self.card_color,
            text_color=self.text_color,
            border_color=self.border_color,
            border_width=2
        )
        self.chat_area.pack(fill="both", expand=True, padx=8, pady=(8,6))
        self.chat_area.configure(state="disabled")

        # BOTTOM PANEL
        self.bottom = ctk.CTkFrame(self.main, fg_color=self.bg_color)
        self.bottom.pack(fill="x", padx=8, pady=(0,8))

        # ENTRY
        self.entry = ctk.CTkEntry(
            self.bottom,
            placeholder_text="Escribe un mensaje...",
            width=600,
            fg_color=self.card_color,
            text_color=self.text_color,
            border_color=self.border_color,
            border_width=2
        )
        self.entry.pack(side="left", padx=(8,6), pady=12, fill="x", expand=True)
        self.entry.bind("<Return>", self._on_send_clicked)

        # RIGHT BUTTON PANEL
        self.btn_frame = ctk.CTkFrame(self.bottom, fg_color=self.bg_color)
        self.btn_frame.pack(side="right", padx=8, pady=8)

        self.send_btn = ctk.CTkButton(
            self.btn_frame,
            text="Enviar",
            width=90,
            fg_color=self.button_color,
            hover_color=self.border_color,
            text_color="black"
        )
        self.send_btn.pack(pady=(6,4))
        self.send_btn.configure(command=self._on_send_clicked)

        self.clear_btn = ctk.CTkButton(
            self.btn_frame,
            text="Limpiar",
            width=90,
            fg_color=self.border_color,
            hover_color=self.button_color,
            text_color=self.text_color
        )
        self.clear_btn.pack(pady=(0,6))
        self.clear_btn.configure(command=self._on_clear)

        # STATUS LABEL
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.text_color
        )
        self.status_label.pack(anchor="w", padx=18, pady=(0,8))

        self.control_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.control_frame.pack(fill="x", padx=12, pady=(0,12))

        ctk.CTkLabel(
            self.control_frame,
            text="Creatividad (temperature):",
            text_color=self.text_color,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(8,6))

        self.temp_slider = ctk.CTkSlider(
            self.control_frame,
            from_=0.0,
            to=1.5,
            number_of_steps=15
        )
        self.temp_slider.set(0.7)
        self.temp_slider.pack(side="left", padx=(0,8))

    # -------------------------------------------
    # HELPERS
    # -------------------------------------------
    def _append_chat(self, prefix, text, prefix_color=None):
        if prefix_color is None:
            prefix_color = self.button_color

        self.chat_area.configure(state="normal")
        self.chat_area.tag_config("prefix", foreground=prefix_color)
        bold_font = ctk.CTkFont(weight="normal")
        self.chat_area.insert("end", f"{prefix}: ")
        start = "end-{}c".format(len(prefix) + 2)  
        end = "end"                              
        self.chat_area.tag_add("prefix", start, end)

        try:
            self.chat_area._textbox.tag_config("prefix", font=bold_font)
        except:
            pass  

        self.chat_area.insert("end", f"{text}\n\n")

        self.chat_area.see("end")
        self.chat_area.configure(state="disabled")

    def _set_status(self, text, color=None):
        def u():
            self.status_label.configure(text=text)
            if color:
                self.status_label.configure(text_color=color)
        self.after(0, u)

    def _set_controls_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.send_btn.configure(state=state)
        self.entry.configure(state=state)
        self.clear_btn.configure(state=state)

    # -------------------------------------------
    # EVENTOS
    # -------------------------------------------
    def _on_send_clicked(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return

        self.entry.delete(0, "end")
        self._append_chat("Tú", text, prefix_color="#6416bd")

        self._set_status("Escribiendo…")
        self._set_controls_state(False)

        temp = float(self.temp_slider.get())
        self.vm.send_message(text, on_success=self._on_response, on_error=self._on_error, temperature=temp)

    def _on_response(self, msg):
        def ui():
            self._set_status("")
            self._append_chat("Bot", msg, prefix_color=self.text_color)
            self._set_controls_state(True)
        self.after(0, ui)

    def _on_error(self, error_msg):
        def ui():
            self._set_status("")
            self._append_chat("Error", error_msg, prefix_color="#f07178")
            self._set_controls_state(True)
        self.after(0, ui)

    def _on_clear(self):
        self.vm.clear_history()
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", "end")
        self.chat_area.configure(state="disabled")
        self._set_status("Chat limpiado.", color=self.text_color)


    def _on_theme_change(self):
        self._apply_theme()

        self.configure(fg_color=self.bg_color)

        # Header
        self.header.configure(fg_color=self.card_color)
        self.title.configure(text_color=self.text_color)

        # Chat area
        self.chat_area.configure(
            fg_color=self.card_color,
            text_color=self.text_color,
            border_color=self.border_color
        )

        # Entry
        self.entry.configure(
            fg_color=self.card_color,
            text_color=self.text_color,
            border_color=self.border_color
        )

        # Bottom
        self.bottom.configure(fg_color=self.bg_color)
        self.btn_frame.configure(fg_color=self.bg_color)

        # Buttons
        self.send_btn.configure(
            fg_color=self.button_color,
            hover_color=self.border_color,
            text_color="black"
        )
        self.clear_btn.configure(
            fg_color=self.border_color,
            hover_color=self.button_color,
            text_color=self.text_color
        )

        self.status_label.configure(text_color=self.text_color)
        self.control_frame.configure(fg_color=self.bg_color)
        self.update_idletasks()  



    def render_chat_history(self):
        self.chat_area.configure(state="normal")  
        self.chat_area.delete("1.0", "end")       

        for msg in self.vm.history:
            role = msg['role']
            content = msg['content']
            if role == "user":
                self.chat_area.insert("end", f"Tú: {content}\n")
            else:
                self.chat_area.insert("end", f"Bot: {content}\n")

        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")  # Hace scroll hacia abajo

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, "end")

        self.vm.send_message(
            user_text,
            on_success=lambda resp: self.render_chat_history(),
            on_error=lambda err: self.render_chat_history()
        )