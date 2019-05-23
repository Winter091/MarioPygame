import pygame as pg


class GameUI(object):
    def __init__(self):
        self.font = pg.font.Font('fonts/emulogic.ttf', 20)
        self.text = 'SCORE COINS WORLD TIME LIVES'

    def render(self, core):
        x = 10
        for word in self.text.split(' '):
            rect = self.font.render(word, False, (255, 255, 255))
            core.screen.blit(rect, (x, 0))
            x += 168

        text = self.font.render(str(core.get_map().get_player().score), False, (255, 255, 255))
        rect = text.get_rect(center=(60, 35))
        core.screen.blit(text, rect)

        text = self.font.render(str(core.get_map().get_player().coins), False, (255, 255, 255))
        rect = text.get_rect(center=(230, 35))
        core.screen.blit(text, rect)

        text = self.font.render(core.get_map().get_name(), False, (255, 255, 255))
        rect = text.get_rect(center=(395, 35))
        core.screen.blit(text, rect)

        text = self.font.render(str(core.get_map().time), False, (255, 255, 255))
        rect = text.get_rect(center=(557, 35))
        core.screen.blit(text, rect)

        text = self.font.render(str(core.get_map().get_player().numOfLives), False, (255, 255, 255))
        rect = text.get_rect(center=(730, 35))
        core.screen.blit(text, rect)
