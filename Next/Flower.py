import pygame as pg

from Entity import Entity


class Flower(Entity):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)
        self.spawned = False
        self.spawn_y_offset = 0

        self.current_image = 0
        self.image_tick = 0
        self.images = (
            pg.image.load('images/flower0.png').convert_alpha(),
            pg.image.load('images/flower1.png').convert_alpha(),
            pg.image.load('images/flower2.png').convert_alpha(),
            pg.image.load('images/flower3.png').convert_alpha()
        )

    def check_collision_with_player(self, core):
        if self.rect.colliderect(core.get_map().get_player().rect):
            core.get_map().get_player().set_powerlvl(3, core)
            core.get_map().get_mobs().remove(self)

    def update_image(self):
        self.image_tick += 1

        if self.image_tick == 60:
            self.image_tick = 0
            self.current_image = 0

        elif self.image_tick % 15 == 0:
            self.current_image += 1

    def spawn_animation(self):
        self.spawn_y_offset -= 1
        self.rect.y -= 1

        if self.spawn_y_offset == -32:
            self.spawned = True

    def update(self, core):
        if self.spawned:
            self.update_image()
        else:
            self.spawn_animation()

    def render(self, core):
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
