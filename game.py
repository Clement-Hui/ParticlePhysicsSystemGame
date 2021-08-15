import sys

import pygame as pg

import config as Config
from engine import Engine
from particle import Particle
from walls import Wall


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode(Config.screen_size)
        pg.display.set_caption("Particles Game")

        self.clock = pg.time.Clock()

        self.engine = Engine(self.surface, Config.offset)
        engine_x, engine_y = Config.engine_size
        w = int(Config.wall_width / 2)
        # adding walls
        self.engine.add_body(Wall(0, 0 - w, 0, engine_y + w, Config.wall_width, Config.wall_colour))
        self.engine.add_body(Wall(0 - w, engine_y, engine_x + w, engine_y, Config.wall_width, Config.wall_colour))
        self.engine.add_body(Wall(engine_x, engine_y + w, engine_x, 0 - w, Config.wall_width, Config.wall_colour))
        self.engine.add_body(Wall(engine_x + w, 0, 0 - w, 0, Config.wall_width, Config.wall_colour))

    def game_loop(self):
        self.surface.fill(Config.bg_colour)

        self.engine.draw()
        pg.display.update()
        self.clock.tick(Config.max_fps)
        self.engine.tick(Config.max_fps)

    def start(self):
        while True:
            for event in pg.event.get():
                # check events
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # mouse clicks
            mouse_x, mouse_y = pg.mouse.get_pos()

            # left click
            if pg.mouse.get_pressed(3)[0]:
                self.engine.add_body(Particle("sodium", mouse_x, mouse_y))

            # right click
            if pg.mouse.get_pressed(3)[2]:
                self.engine.add_body(Particle("water", mouse_x, mouse_y))

            # middle click
            if pg.mouse.get_pressed(3)[1]:
                self.engine.add_body(Particle("hydrogen", mouse_x, mouse_y))

            self.game_loop()
