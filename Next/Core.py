from os import environ

import pygame as pg
from pygame.locals import *

from Next.Const import *
from Next.Map import Map
from Next.MenuManager import MenuManager
from Next.Sound import Sound


class Core(object):
    """

    Main class.

    """
    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(44100, -16, 2, 1024)
        pg.init()
        pg.display.set_caption('Mario by S&D')
        pg.display.set_mode((WINDOW_W, WINDOW_H))

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()

        self.oMap = Map('1-1')
        self.oSound = Sound()
        self.oMM = MenuManager(self)

        self.run = True
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

        self.keys = [False] * 512
        self.keys_duration = [0] * 512
        self.pressed_this_frame = []

    def main_loop(self):
        while self.run:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        if self.get_mm().currentGameState == 'Game':
            self.input_player()
        else:
            self.input_menu()

    def input_player(self):
        self.pressed_this_frame = []

        for e in pg.event.get():

            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                self.keys[e.key] = True
                self.pressed_this_frame.append(e.key)

                # F5
                if e.key == 286:
                    self.get_map().get_console().change_mode()

            elif e.type == KEYUP:
                self.keys[e.key] = False
                self.keys_duration[e.key] = 0

        # Long press
        for i in range(32, 127):
            if self.keys[i]:
                self.keys_duration[i] += 1
            else:
                self.keys_duration[i] = 0

        # Backspace
        if self.keys[8]:
            self.keys_duration[8] += 1
        else:
            self.keys_duration[8] = 0

    def input_menu(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    self.get_mm().start_loading()

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.oMap

    def get_mm(self):
        return self.oMM

    def get_sound(self):
        return self.oSound
