collision_type = 2

size_scaling = 5
size_buffer = 0.5

offset = (50, 50)
screen_size = (1600, 900)
engine_size = (800, 800)
wall_width = 9
wall_colour = (227, 227, 227)

bg_colour = (56, 56, 56)

max_fps = 30
gravity = (0, 200)
dist_cache = 3


def hash_type(x):
    return abs(hash(x)) % (10 ** 10)
