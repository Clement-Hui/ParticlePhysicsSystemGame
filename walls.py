import pygame as pg
import pymunk

from rigid_body import RigidBody


class Wall(RigidBody):
    def __init__(self, x1, y1, x2, y2, width, colour):
        super().__init__()
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), width)
        self.shape.collision_type = 1
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.colour = colour
        self.width = width

    def draw(self, surface: pg.Surface, offset):
        offset_x, offset_y = offset
        pg.draw.line(surface, self.colour, (self.x1 + offset_x, self.y1 + offset_y),
                     (self.x2 + offset_x, self.y2 + offset_y), self.width)
