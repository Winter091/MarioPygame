import pygame as pg

from Next.Const import *


class PlatformDebris(pg.sprite.Sprite):
    """

    Debris which appears when you destroy a brick block.

    """
    def __init__(self, x_pos, y_pos, world_type):
        super().__init__()

        # I don't know why I did it, but image depends on the world type: under and upper world.
        # World type 1 is never used.
        if world_type == 0:
            self.image = pg.image.load('images/block_debris0.png').convert_alpha()
        elif world_type == 1:
            self.image = pg.image.load('images/block_debris1.png').convert_alpha()

        # 4 individual small bricks
        self.rectangles = [
            pg.Rect(x_pos - 20, y_pos + 16, 16, 16),
            pg.Rect(x_pos - 20, y_pos - 16, 16, 16),
            pg.Rect(x_pos + 20, y_pos + 16, 16, 16),
            pg.Rect(x_pos + 20, y_pos - 16, 16, 16)
        ]
        self.y_vel = -4
        self.rect = None

    def update(self, core):
        self.y_vel += GRAVITY

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
