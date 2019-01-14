import pygame as pg

from Entity import Entity
from Const import *


class Mushroom(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)

        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.spawned = False
        self.spawn_y_offset = 0
        self.image = pg.image.load('images/mushroom.png').convert_alpha()

    def check_collision_with_player(self, core):
        if self.rect.colliderect(core.get_map().get_player().rect):
            core.get_map().get_player().set_powerlvl(2, core)
            core.get_map().get_mobs().remove(self)

    def die(self, core, instantly, crushed):
        core.get_map().get_mobs().remove(self)

    def spawn_animation(self):
        self.spawn_y_offset -= 1
        self.rect.y -= 1

        if self.spawn_y_offset == - 32:
            self.spawned = True

    def update(self, core):
        if self.spawned:
            if not self.on_ground:
                self.y_vel += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)
        else:
            self.spawn_animation()

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_camera().apply(self))