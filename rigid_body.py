class RigidBody:

    def __init__(self):
        self.shape = None
        self.body = None

    def remove(self):
        self.shape.space.remove(self.shape)
        self.body.space.remove(self.body)

    def draw(self, surface, offset):
        pass
