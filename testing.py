import random
import sys
import threading
import time
from math import sqrt

import numpy as np
import pygame as pg
import pymunk
from pygame import gfxdraw

pg.init()
screen_size = (1600, 900)
game_window = pg.display.set_mode(screen_size)
pg.display.set_caption("Particle Physics Engine")
clock = pg.time.Clock()
# test code
radius = 5
space = pymunk.Space()
space.gravity = (0, 300)
space.damping = 0.95
space.sleep_time_threshold = 2


def create_ball(position):
    body = pymunk.Body(mass=1, moment=0.1)
    body.position = position
    shape = pymunk.Circle(body, radius + 2)
    shape.collision_type = 1

    space.add(body, shape)

    return body, shape


def draw_ball(shape: pymunk.Shape, i):
    pos_x = int(shape.body.position.x)
    pos_y = int(shape.body.position.y)
    past_x = int(balls_coords[i][0])
    past_y = int(balls_coords[i][1])
    if sqrt((past_x - pos_x) ** 2 + (
            past_y - pos_y) ** 2) <= 4 and shape.body.velocity.x < 2.5 and shape.body.velocity.y < 2.5:
        gfxdraw.aacircle(game_window, past_x + 50, past_y + 50, radius, (255, 30, 30))
        gfxdraw.filled_circle(game_window, past_x + 50, past_y + 50, radius, (255, 30, 30))

    else:
        gfxdraw.aacircle(game_window, pos_x + 50, pos_y + 50, radius, (100, 100, 100))
        gfxdraw.filled_circle(game_window, pos_x + 50, pos_y + 50, radius, (100, 100, 100))
        balls_coords[i][0] = pos_x
        balls_coords[i][1] = pos_y


def draw_balls(list_balls, index):
    for item in zip(list_balls, index):
        draw_ball(item[0], item[1])


num_balls = 1500
balls = np.zeros((num_balls), dtype=pymunk.Circle)
balls_coords = np.zeros((num_balls, 2))
for i in range(num_balls):
    body, shape = create_ball((random.randint(20, 780), random.randint(20, 400)))
    balls[i] = shape


class Box:
    def __init__(self, p0=(10, 10), p1=(790, 790), d=20):
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, pts[i], pts[(i + 1) % 4], d)
            segment.elasticity = 1
            segment.friction = 1
            space.add(segment)


box = Box()

start = time.time()
tick = 0

mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC, mass=100)
mouse_shape = pymunk.Circle(mouse_body, radius=40)
mouse_shape.collision_type = 2
space.add(mouse_body, mouse_shape)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if pg.mouse.get_pressed()[0]:
            coord = pg.mouse.get_pos()
            mouse_pos = pymunk.Vec2d(coord[0] - 50, coord[1] - 50)
            print(coord)
            mouse_body.position = mouse_pos

        else:
            mouse_pos = pymunk.Vec2d(-100, -100)

            mouse_body.position = mouse_pos

    game_window.fill((255, 255, 255))

    pg.draw.line(game_window, (170, 170, 170), (60, 60), (60, 840), 10)
    pg.draw.line(game_window, (170, 170, 170), (60, 840), (840, 840), 10)
    pg.draw.line(game_window, (170, 170, 170), (840, 60), (840, 840), 10)
    pg.draw.line(game_window, (170, 170, 170), (60, 60), (840, 60), 10)

    threads = []
    num_thread = 8
    for i in range(num_thread):
        thread = threading.Thread(draw_balls(balls[int(i * num_balls / 8):int((i + 1) * num_balls / 8 - 1)],
                                             range(int(i * num_balls / 8), int((i + 1) * num_balls / 8 - 1))))

        thread.daemon = True
        threads.append(thread)
        thread.start()

    pg.display.update()
    clock.tick(30)
    space.step(1 / 30)
    tick += 1
    now = time.time()
    print(f"FPS = {1 / ((now - start) / tick)}")
