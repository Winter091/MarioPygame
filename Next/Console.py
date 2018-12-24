import pygame as pg
import types

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
        self.buffer = ['>'] * BUFFER_SIZE
        self.buffer_index = -1
        self.mode = 0

    def update(self, core):

        self.handle_pressed_keys(core)

    def handle_pressed_keys(self, core):
        shift = core.keys[304]
        caps_lock = core.keys[301]

        for key in core.pressed_this_frame:

            # Usual symbols except dash (45)
            if 32 <= key <= 44 or 46 <= key <= 126:
                if shift or caps_lock:
                    self.print_char(key, upper_case=True)
                else:
                    self.print_char(key, upper_case=False)

            # Dash and underscore
            elif key == 45:
                if shift:
                    self.print_char(95, upper_case=False)
                else:
                    self.print_char(45, upper_case=False)

            # Backspace
            elif key == 8:
                self.remove_last_char()

            # Enter
            elif key == 13:
                self.goto_next_line()
                self.process_command(core)

            # PageUp: goto buffer history, up
            elif key == 280:
                self.goto_buffer_up()

            # PageDn: goto buffer history, down
            elif key == 281:
                self.goto_buffer_down()

        # Long pressed keys handling
        for key in range(len(core.keys_duration)):

            # key is being pressed for 60 frames or more
            if core.keys_duration[key] >= 60:

                # Usual symbols except dash (45)
                if 32 <= key <= 44 or 46 <= key <= 126:
                    if shift or caps_lock:
                        self.print_char(key, upper_case=True)
                    else:
                        self.print_char(key, upper_case=False)

                # Dash and underscore
                elif key == 45:
                    if shift:
                        self.print_char(95, upper_case=False)
                    else:
                        self.print_char(45, upper_case=False)

                elif key == 8:
                    self.remove_last_char()

    def process_command(self, core):
        command, *args = self.buffer[-2].split(' ')

        if command.startswith('>'):
            command = command[1:]

        if command == 'help':
            self.command_help()
        elif command == 'print':
            self.command_print(args, core)
        elif command == 'change':
            self.command_change(args, core)
        else:
            self.print_str('Unknown command: {}'.format(command))

    def command_help(self):
        self.print_str("You're using S&D MarioPyGame console.")
        self.print_str("Commands available:")
        self.print_str('    help - print this message')
        self.print_str("    print [variable] - print variable's value")
        self.print_str('    change [variable] [new_value] - change the value of the variable')

    def command_print(self, args, core):

        obj = core

        # Check if the args are correct
        if len(args):
            args = args[0].split('.')
        else:
            self.print_str('    Usage: print [variable]')
            return 0

        # Check if the path exists
        for attr in args:
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            else:
                self.print_str("Error: '{}' doesn't have '{}'".format(obj, attr))
                return 0

        self.print_str(str(obj))

    def command_change(self, args, core):

        obj = core

        # Check if the args are correct
        if len(args) == 2:
            path = args[0].split('.')
            value = args[1]
        else:
            self.print_str('    Usage: change [variable] [new_value]')
            return 0

        # Check if the path exists
        for attr in path:
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            else:
                self.print_str("Error: '{}' doesn't have '{}'".format(obj, attr))
                return 0

        try:
            value = int(value)
        except ValueError:
            pass

        if len(path) == 2:
            upper_object = getattr(core, path[0])
            setattr(upper_object, path[1], value)
            setattr(core, path[0], upper_object)
            return 0

        # Get needed object
        obj = core
        for attr in path[:-1]:
            obj = getattr(obj, attr)

        # Change the object's value
        setattr(obj, path[-1], int(value))

        # Object where we try to find our obj
        upper_object = core

        # Для имени нашего объекта
        i = -2
        # Чтобы спускаться вниз к нашему объекту
        j = 0
        while True:

            # Если данная иерархия не имеет нашего объекта
            if not hasattr(upper_object, path[i]):
                # Спускаемся на 1 уровень вниз, к нашему объекту
                # То есть верхним объектом становится объект ниже прошлого
                upper_object = getattr(upper_object, path[j])
                j += 1

            # Если мы наконец нашли наш объект
            else:
                # Заменяем в upper_object прошлый объект нашим, уже обновлённым
                setattr(upper_object, path[i], obj)

                # Заменяем наш объект верхним
                obj = upper_object

                upper_object = core
                j = 0

                # Наш объект выше, значит его имя тоже в списке path раньше
                i -= 1

                # Если мы уже дошли до конца, то есть до core
                if path[i] == path[j]:
                    break

    def print_str(self, string):
        self.buffer[-1] = ''
        for char in string:
            if char.islower():
                self.print_char(ord(char), upper_case=False)
            else:
                self.print_char(ord(char), upper_case=True)
        self.goto_next_line()

    def print_char(self, key, upper_case):
        if len(self.buffer[-1]) < 91:
            if upper_case:
                self.buffer[-1] += chr(key).upper()
            else:
                self.buffer[-1] += chr(key)

    def remove_last_char(self):
        if len(self.buffer[-1]) > 1:
            self.buffer[-1] = self.buffer[-1][:-1]

    def goto_buffer_up(self):
        if -self.buffer_index < BUFFER_SIZE:
            self.buffer_index -= 1
            self.buffer[-1] = self.buffer[self.buffer_index]

    def goto_buffer_down(self):
        if self.buffer_index < -1:
            self.buffer_index += 1
            self.buffer[-1] = self.buffer[self.buffer_index]

    def goto_next_line(self):
        self.buffer_index = -1
        self.buffer = self.buffer[1:]
        self.buffer.append('>'.format(-self.buffer_index))

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
