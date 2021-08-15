import json
import math

import pygame as pg
import pymunk
from pygame import gfxdraw

import config as Config
from custom_shape import ParticleShape
from rigid_body import RigidBody

with open("json_files/particles.json", "r") as f:
    raw = f.read()

data = json.loads(raw)


class Particle(RigidBody):
    def __init__(self, type, x, y):
        super().__init__()
        # see if type exists in json data
        try:
            self.data = data[type]
        except Exception:
            print(f"Error: {type} particle not found")
            return
        self.name = type
        self.formula = self.data["formula"]
        self.colour = self.data["colour"]
        self.density = self.data["density"]
        self.size = self.data["size"] * Config.size_scaling

        self.body = pymunk.Body()
        self.shape = ParticleShape(self.body, self.size + Config.size_buffer, self)
        self.shape.collision_type = Config.hash_type(self.name)
        self.shape.density = self.density

        self.cache_x_y = (0, 0)
        self.body.position = (x, y)

    def draw(self, surface: pg.Surface, offset):

        # if body is outside of frame
        if abs(self.body.position[0]) > 10000 or abs(self.body.position[1]) > 10000:
            return
        offset_x, offset_y = offset
        x = int(self.body.position[0] + offset_x)
        y = int(self.body.position[1] + offset_y)
        # if body did not move much
        if math.dist(self.cache_x_y, (x, y)) < self.size / 4 and self.body.velocity.x < 1 and self.body.velocity.y < 1:
            x, y = self.cache_x_y
        self.cache_x_y = (x, y)
        gfxdraw.aacircle(surface, x, y, round(self.size), self.colour)
        gfxdraw.filled_circle(surface, x, y, round(self.size), self.colour)
