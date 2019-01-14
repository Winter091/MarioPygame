import pygame as pg

from Const import *


class Camera(object):
    """

    I don't fully understand how it works. I just copied the whole class
    from the other project. Sorry.

    """
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.complex_camera(self.rect)

    def complex_camera(self, target_rect):
        x, y = target_rect.x, target_rect.y
        width, height = self.rect.width, self.rect.height
        x, y = (-x + WINDOW_W / 2 - target_rect.width / 2), (-y + WINDOW_H / 2 - target_rect.height)

        x = min(0, x)
        x = max(-(self.rect.width - WINDOW_W), x)
        y = WINDOW_H - self.rect.h

        return pg.Rect(x, y, width, height)

    def apply(self, target):
        return target.rect.x + self.rect.x, target.rect.y

    def update(self, target):
        self.rect = self.complex_camera(target)

    def reset(self):
        self.rect = pg.Rect(0, 0, self.rect.w, self.rect.h)
