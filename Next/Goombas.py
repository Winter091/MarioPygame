import pygame as pg

from Entity import Entity
from Const import *


class Goombas(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()
        self.rect = pg.Rect(x_pos, y_pos, 32, 32)

        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.crushed = False

        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pg.image.load('images/goombas_0.png').convert_alpha(),
            pg.image.load('images/goombas_1.png').convert_alpha(),
            pg.image.load('images/goombas_dead.png').convert_alpha()
        ]
        self.images.append(pg.transform.flip(self.images[0], 0, 180))

    def die(self, core, instantly, crushed):
        if not instantly:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            if crushed:
                self.crushed = True
                self.image_tick = 0
                self.current_image = 2
                self.state = -1
                core.get_sound().play('kill_mob', 0, 0.5)
                self.collision = False

            else:
                self.y_vel = -4
                self.current_image = 3
                core.get_sound().play('shot', 0, 0.5)
                self.state = -1
                self.collision = False

        else:
            core.get_map().get_mobs().remove(self)

    def check_collision_with_player(self, core):
        if self.collision:
            if self.rect.colliderect(core.get_map().get_player().rect):
                if self.state != -1:
                    if core.get_map().get_player().y_vel > 0:
                        self.die(core, instantly=False, crushed=True)
                        core.get_map().get_player().reset_jump()
                        core.get_map().get_player().jump_on_mob()
                    else:
                        if not core.get_map().get_player().unkillable:
                            core.get_map().get_player().set_powerlvl(0, core)

    def update_image(self):
        self.image_tick += 1
        if self.image_tick == 14:
            self.current_image = 1
        elif self.image_tick == 28:
            self.current_image = 0
            self.image_tick = 0

    def update(self, core):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.y_vel += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)

        elif self.state == -1:
            if self.crushed:
                self.image_tick += 1
                if self.image_tick == 50:
                    core.get_map().get_mobs().remove(self)
            else:
                self.y_vel += GRAVITY
                self.rect.y += self.y_vel
                self.check_map_borders(core)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
