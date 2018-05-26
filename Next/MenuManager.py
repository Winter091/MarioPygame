from enum import Enum

import pygame as pg
from pygame.locals import *

from Next.LoadingMenu import LoadingMenu
from Next.MainMenu import MainMenu


class MenuManager(object):
    """

    That class allows to easily handle game states. Depending on the situation,
    it updates and renders different things.

    """
    def __init__(self, core):
        self.gameState = Enum('gameState', 'eMainMenu eLoading eGame')

        self.currentGameState = self.gameState.eMainMenu

        self.oMainMenu = MainMenu()
        self.oLoadingMenu = LoadingMenu(core)

    def update(self, core):
        if self.currentGameState == self.gameState.eMainMenu:
            pass

        elif self.currentGameState == self.gameState.eLoading:
            self.oLoadingMenu.update(core)

        elif self.currentGameState == self.gameState.eGame:
            core.get_map().update(core)

    def render(self, core):
        if self.currentGameState == self.gameState.eMainMenu:
            core.get_map().render_map(core)
            self.oMainMenu.render(core)

        elif self.currentGameState == self.gameState.eLoading:
            self.oLoadingMenu.render(core)

        elif self.currentGameState == self.gameState.eGame:
            core.get_map().render(core)
            core.get_map().get_ui().render(core)

        pg.display.update()

    def key_pressed(self, key, core):
        if self.currentGameState == self.gameState.eMainMenu:
            if key == K_RETURN:

                # Start load the level
                self.currentGameState = self.gameState.eLoading
                self.oLoadingMenu.update_time()

    def get_debug_table(self):
        return self.oDebugTable
