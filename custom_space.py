import pymunk


class CustomSpace(pymunk.Space):
    def __init__(self, threaded=False):
        super().__init__(threaded)
        self.ticks = 1

    def step(self, dt):
        super().step(dt)
        self.ticks += 1
