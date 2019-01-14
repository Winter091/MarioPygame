import pygame as pg

from Entity import Entity
from Const import *


class Koopa(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()
        self.rect = pg.Rect(x_pos, y_pos, 32, 46)

        self.move_direction = move_direction

        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pg.image.load('images/koopa_0.png').convert_alpha(),
            pg.image.load('images/koopa_1.png').convert_alpha(),
            pg.image.load('images/koopa_dead.png').convert_alpha()
        ]
        self.images.append(pg.transform.flip(self.images[0], 180, 0))
        self.images.append(pg.transform.flip(self.images[1], 180, 0))
        self.images.append(pg.transform.flip(self.images[2], 0, 180))

    """
    States: 
    0 - Just walking around
    1 - Hidden 
    2 - Hidden and fast moving
    -1 - Dead
    """

    def check_collision_with_player(self, core):
        if self.collision:
            if self.rect.colliderect(core.get_map().get_player().rect):
                if self.state != -1:
                    if core.get_map().get_player().y_vel > 0:
                        self.change_state(core)
                        core.get_sound().play('kill_mob', 0, 0.5)
                        core.get_map().get_player().reset_jump()
                        core.get_map().get_player().jump_on_mob()
                    else:
                        if not core.get_map().get_player().unkillable:
                            core.get_map().get_player().set_powerlvl(0, core)

    def check_collision_with_mobs(self, core):
        for mob in core.get_map().get_mobs():
            if mob is not self:
                if self.rect.colliderect(mob.rect):
                    if mob.collision:
                        mob.die(core, instantly=False, crushed=False)

    def die(self, core, instantly, crushed):
        if not instantly:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)
            self.state = -1
            self.y_vel = -4
            self.current_image = 5
        else:
            core.get_map().get_mobs().remove(self)

    def change_state(self, core):
        self.state += 1
        self.current_image = 2

        # 0 to 1 state
        if self.rect.h == 46:
            self.x_vel = 0
            self.rect.h = 32
            self.rect.y += 14
            core.get_map().get_player().add_score(100)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

        # 1 to 2
        elif self.state == 2:
            core.get_map().get_player().add_score(100)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y, score=100)

            if core.get_map().get_player().rect.x - self.rect.x <= 0:
                self.x_vel = 6
            else:
                self.x_vel = -6

        # 2 to 3
        elif self.state == 3:
            self.die(core, instantly=False, crushed=False)

    def update_image(self):
        self.image_tick += 1

        if self.x_vel > 0:
            self.move_direction = True
        else:
            self.move_direction = False

        if self.image_tick == 35:
            if self.move_direction:
                self.current_image = 4
            else:
                self.current_image = 1
        elif self.image_tick == 70:
            if self.move_direction:
                self.current_image = 3
            else:
                self.current_image = 0
            self.image_tick = 0

    def update(self, core):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.y_vel += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, (self.rect.y - 14) // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)

        elif self.state == 1:
            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)

        elif self.state == 2:
            if not self.on_ground:
                self.y_vel += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)
            self.check_collision_with_mobs(core)

        elif self.state == -1:
            self.rect.y += self.y_vel
            self.y_vel += GRAVITY

            self.check_map_borders(core)

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
