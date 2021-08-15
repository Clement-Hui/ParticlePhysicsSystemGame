import json
from typing import Tuple

import config as Config
from custom_space import CustomSpace
from particle import Particle
from rigid_body import RigidBody

with open("json_files/reactions.json", "r") as f:
    raw = f.read()

reactions = json.loads(raw)["reactions"]

with open("json_files/particles.json", "r") as f:
    raw = f.read()

particles = json.loads(raw)


class Engine:
    def __init__(self, surface, offset: Tuple):
        self.space = CustomSpace(True)
        self.rigid_bodies = []
        self.surface = surface
        self.offset = offset
        self.space.gravity = Config.gravity
        self.ticks = 1

        for reaction in reactions:
            reactants = reaction.split("+")
            type_1 = Config.hash_type(reactants[0])
            type_2 = Config.hash_type(reactants[1])
            c_handler = self.space.add_collision_handler(type_1, type_2)
            c_handler.begin = self.normal_reaction(reactants)

    def add_body(self, rigid_body: RigidBody):
        self.space.add(rigid_body.body, rigid_body.shape)
        self.rigid_bodies.append(rigid_body)

    def draw(self):
        for rigid_body in self.rigid_bodies:
            rigid_body.draw(self.surface, self.offset)

    def tick(self, fps):
        self.space.step(1 / fps)
        self.ticks += 1

    def normal_reaction(self, reactants):

        def c_handler(arbiter, space, data, reactants=reactants):

            rate = reactions["+".join(reactants)]["reaction_rate"]
            if space.ticks % rate != 0:
                return True

            shape1, shape2 = arbiter.shapes

            rigid_body1 = shape1.parent
            rigid_body2 = shape2.parent
            avg_x = (shape1.body.position.x + shape2.body.position.x) / 2
            avg_y = (shape1.body.position.y + shape2.body.position.y) / 2

            products = reactions["+".join(reactants)]["product"]

            for item in products:
                rigid_body = Particle(item, avg_x, avg_y)
                self.add_body(rigid_body)

            rigid_body1.remove()
            rigid_body2.remove()
            try:
                self.rigid_bodies.remove(rigid_body1)
                self.rigid_bodies.remove(rigid_body2)
            except Exception:
                pass

            return False

        return c_handler
