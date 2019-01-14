import pygame as pg

from LoadingMenu import LoadingMenu
from MainMenu import MainMenu


class MenuManager(object):
    """

    That class allows to easily handle game states. Depending on the situation,
    it updates and renders different things.

    """
    def __init__(self, core):

        self.currentGameState = 'MainMenu'

        self.oMainMenu = MainMenu()
        self.oLoadingMenu = LoadingMenu(core)

    def update(self, core):
        if self.currentGameState == 'MainMenu':
            pass

        elif self.currentGameState == 'Loading':
            self.oLoadingMenu.update(core)

        elif self.currentGameState == 'Game':
            core.get_map().update(core)

    def render(self, core):
        if self.currentGameState == 'MainMenu':
            core.get_map().render_map(core)
            self.oMainMenu.render(core)

        elif self.currentGameState == 'Loading':
            self.oLoadingMenu.render(core)

        elif self.currentGameState == 'Game':
            core.get_map().render(core)
            core.get_map().get_ui().render(core)

        pg.display.update()

    def start_loading(self):
            # Start to load the level
            self.currentGameState = 'Loading'
            self.oLoadingMenu.update_time()
