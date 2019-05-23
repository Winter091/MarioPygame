import pygame as pg


class DebugTable(object):
    """

    I don't use it anymore. This class helped me a lot on the
    develop days because it displayed some variables in real time.

    """
    def __init__(self):
        self.font = pg.font.SysFont('Consolas', 12)
        self.darkArea = pg.Surface((200, 100)).convert_alpha()
        self.darkArea.fill((0, 0, 0, 200))
        self.text = []
        self.rect = 0
        self.offsetX = 12
        self.x = 5
        self.mode = 2

    def update_text(self, core):
        if self.mode == 2:
            self.text = [
                'FPS: ' + str(int(core.clock.get_fps())),
                'Rect: ' + str(core.get_map().get_player().rect.x) + ' ' + str(core.get_map().get_player().rect.y) + ' h: ' + str(core.get_map().get_player().rect.h),
                'g: ' + str(core.get_map().get_player().on_ground) + ' LVL: ' + str(core.get_map().get_player().powerLVL) + ' inv: ' + str(core.get_map().get_player().unkillable),
                'Spr: ' + str(core.get_map().get_player().spriteTick) + ' J lock: ' + str(core.get_map().get_player().already_jumped),
                'Up  : ' + str(core.get_map().get_player().inLevelUpAnimation) + '  time: ' + str(core.get_map().get_player().inLevelUpAnimationTime),
                'Down: ' + str(core.get_map().get_player().inLevelDownAnimation) + '  time: ' + str(core.get_map().get_player().inLevelDownAnimationTime),
                'Mobs: ' + str(len(core.get_map().get_mobs())) + ' FB: ' + str(len(core.get_map().projectiles)) + ' Debris: ' + str(len(core.get_map().debris))
            ]

    def render(self, core):
        self.x = 105
        if self.mode == 2:
            core.screen.blit(self.darkArea, (0, 100))
            for string in self.text:
                self.rect = self.font.render(string, True, (255, 255, 255))
                core.screen.blit(self.rect, (5, self.x))
                self.x += self.offsetX
