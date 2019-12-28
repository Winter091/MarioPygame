import pygame as pg

from Const import *


class PlatformDebris(object):
    """

    Debris which appears when you destroy a brick block.

    """
    def __init__(self, x_pos, y_pos):
        self.image = pg.image.load('images/block_debris0.png').convert_alpha()

        # 4 different parts
        self.rectangles = [
            pg.Rect(x_pos - 20, y_pos + 16, 16, 16),
            pg.Rect(x_pos - 20, y_pos - 16, 16, 16),
            pg.Rect(x_pos + 20, y_pos + 16, 16, 16),
            pg.Rect(x_pos + 20, y_pos - 16, 16, 16)
        ]
        self.y_vel = -4
        self.rect = None

    def update(self, core):
        self.y_vel += GRAVITY * FALL_MULTIPLIER

        for i in range(len(self.rectangles)):
            self.rectangles[i].y += self.y_vel
            if i < 2:
                self.rectangles[i].x -= 1
            else:
                self.rectangles[i].x += 1

        if self.rectangles[1].y > core.get_map().mapSize[1] * 32:
            core.get_map().debris.remove(self)

    def render(self, core):
        for rect in self.rectangles:
            self.rect = rect
            core.screen.blit(self.image, core.get_map().get_camera().apply(self))
