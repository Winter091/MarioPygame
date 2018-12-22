import pygame as pg

from Next.Const import *

TOPLEFT = (75, 75)
SIZE = (WINDOW_W - 150, WINDOW_H - 150)
ALPHA = 150
BUFFER_SIZE = 100


class ConsoleBackground(object):
    def __init__(self):
        self.rect = pg.Rect(TOPLEFT, SIZE)
        self.area = pg.Surface(self.rect.size).convert_alpha()
        self.area.fill((0, 0, 0, ALPHA))

    def render(self, screen):
        screen.blit(self.area, (self.rect.x, self.rect.y))


class Console(object):
    def __init__(self):
        self.bg = ConsoleBackground()

        self.font = pg.font.SysFont('Consolas', 12)
        self.buffer = [''] * BUFFER_SIZE
        self.mode = 0

    def update(self, core):
        if not self.buffer[-1].startswith('>'):
            self.buffer[-1] = '>'

        for key in core.pressed_this_frame:

            # Letters
            if 32 <= key <= 126:
                self.write_char(key, core)

            # Backspace
            elif key == 8:
                self.remove_last_char()

            # Enter
            elif key == 13:
                self.goto_next_line()

        # Long pressed keys handling
        for key in range(len(core.keys_duration)):
            # key is being pressed for 60 frames or more
            if core.keys_duration[key] >= 60:
                if 32 <= key <= 126:
                    self.write_char(key, core)
                elif key == 8:
                    self.remove_last_char()

    def write_char(self, key, core):
        if len(self.buffer[-1]) < 91:
            # Caps Lock or shift
            if core.keys[304] or core.keys[301]:
                self.buffer[-1] += chr(key).upper()
            else:
                self.buffer[-1] += chr(key)

    def remove_last_char(self):
        if len(self.buffer[-1]) > 1:
            self.buffer[-1] = self.buffer[-1][:-1]

    def goto_next_line(self):
        self.buffer = self.buffer[1:]
        self.buffer[-1] = self.buffer[-1][1:]
        self.buffer.append('')

    def change_mode(self):
        if self.mode:
            self.mode = 0
        else:
            self.mode = 1

    def get_mode(self):
        return self.mode

    def render(self, core):
        if self.mode == 1:
            self.bg.render(core.screen)

            for i in range(len(self.buffer) - 2, len(self.buffer) - 21, -1):
                text_rect = self.font.render(self.buffer[i], True, (255, 255, 255))
                core.screen.blit(text_rect, (self.bg.rect.x + 5,
                                             self.bg.rect.bottom - 28 - (len(self.buffer) - i) * 12))

            text_rect = self.font.render(self.buffer[-1], True, (255, 255, 255))
            core.screen.blit(text_rect, (self.bg.rect.x + 5, self.bg.rect.bottom - 15))
