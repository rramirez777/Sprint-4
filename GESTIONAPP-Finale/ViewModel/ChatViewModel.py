from threading import Thread
from Servicios.ChatService import ChatService

class ChatViewModel:
    _instances = {}  

    def __new__(cls, user_id, chat_service=None):
        if user_id in cls._instances:
            return cls._instances[user_id]
        instance = super().__new__(cls)
        cls._instances[user_id] = instance
        return instance

    def __init__(self, user_id, chat_service=None):
        if hasattr(self, 'initialized'):
            return  
        self.initialized = True

        self.user_id = user_id
        self.service = chat_service if chat_service else ChatService()
        self.history = []

    def send_message(self, user_text, on_success, on_error=None, temperature=0.7, max_tokens=500):
        self.history.append({"role": "user", "content": user_text})

        def worker():
            try:
                response = self.service.send(
                    self.history,
                    user_id=self.user_id,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                self.history.append({"role": "assistant", "content": response})
                on_success(response)
            except Exception as e:
                msg = f"[Error] {str(e)}"
                if on_error:
                    on_error(msg)
                else:
                    on_success(msg)

        Thread(target=worker, daemon=True).start()

    def clear_history(self):
        self.history = []
