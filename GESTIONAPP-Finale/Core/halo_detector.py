class HaloCodeDetector:
    def __init__(self, callback):
        self.sequence = ["w", "o", "r", "t"]
        self.position = 0
        self.callback = callback

    def key_pressed(self, key):
        if key == self.sequence[self.position]:
            self.position += 1
            if self.position == len(self.sequence):
                self.position = 0
                self.callback()
        else:
            self.position = 0
