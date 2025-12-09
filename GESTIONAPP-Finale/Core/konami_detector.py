class KonamiDetector:
    def __init__(self, callback):
        self.callback = callback
        self.secuencia_correcta = [
            "up", "up",
            "down", "down",
            "left", "right",
            "left", "right",
            "b", "a"
        ]
        self.posicion = 0

    def key_pressed(self, key):
        if key == self.secuencia_correcta[self.posicion]:
            self.posicion += 1
            
            if self.posicion == len(self.secuencia_correcta):
                self.callback()
                self.posicion = 0

        else:
            self.posicion = 1 if key == self.secuencia_correcta[0] else 0