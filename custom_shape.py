import pymunk


class ParticleShape(pymunk.Circle):
    def __init__(self, body, radius, parent):
        super().__init__(body, radius)
        self.parent = parent
        self.collision_type = 2
