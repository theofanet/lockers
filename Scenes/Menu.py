from PyGnin import *
import pygame

from .Locker1 import Locker1
from .Locker2 import Locker2
from .Locker3 import Locker3
from .Locker4 import Locker4


NB_LEVELS = 4
RED_COLOR = (192, 57, 43)
GREEN_COLOR = (39, 174, 96)
YELLOW_COLOR = (241, 196, 15)
GRAY_COLOR = (149, 165, 166)
CURSOR_ANIMATION_SPEED = 30


class LockerLevel(object):
    def __init__(self, scene, index):
        self.is_done = False
        self.time = 0
        self._scene = scene
        self._index = index

    def update(self):
        if self._scene:
            self._scene.update()

    def draw(self):
        if self._scene:
            self._scene.draw()

    def init_scene(self, master_scene):
        if self._scene:
            self._scene.initiate(master_scene)

    def __str__(self):
        return "level %i %i %f" % (
            self._index,
            1 if self.is_done else 0,
            self.time
        )


class MenuCursor(object):
    def __init__(self):
        self._index = 0
        self._position = (0, 0)
        self._img = Render.Image("assets/play.png")
        self._img.set_scale(0.0488)
        self._offset_y = 0
        self._offset_direction = False
        self._speed = CURSOR_ANIMATION_SPEED

    def set_index(self, index):
        self._index = index
        return self

    def get_index(self):
        return self._index

    def update(self):
        self._offset_y += self._speed * (App.get_time() / 1000)
        if self._offset_y > 60:
            self._offset_y = 60
            self._speed = -CURSOR_ANIMATION_SPEED
        elif self._offset_y < 50:
            self._offset_y = 50
            self._speed = CURSOR_ANIMATION_SPEED

    def draw(self):
        dx, dy = App.get_screen_size()
        ddx = int(dx / 4)

        self._img.draw((ddx * self._index + ddx / 2), (dy / 2) + self._offset_y, at_center=True)


class LockersMenu(Game.Scene):
    def __init__(self):
        super().__init__()
        self._active_level = None
        self._current_level = 2
        self._levels = []
        self._elapsed_time = 0
        self._fonts = None
        self._cursor = None
        self._bonuses = []

    def return_menu(self):
        self._active_level = None

    def load_scores(self):
        try:
            with open("score") as fp:
                current_level = 0
                for line in fp:
                    if line.startswith("level"):
                        values = line.split(" ")
                        values.pop(0)
                        values = list(map(float, values))
                        index = int(values.pop(0))
                        self._levels[index].time = values[1]
                        self._levels[index].is_done = True if int(values[0])==1 else False
                        self._bonuses[index].set_color_t(YELLOW_COLOR if int(values[0])==1 else GRAY_COLOR)
                        if self._levels[index].is_done and index < NB_LEVELS - 1:
                            self._cursor.set_index(index+1)
                        current_level += 1
        except FileNotFoundError:
            pass

    def save_scores(self):
        with open("score", "w") as fp:
            fp.writelines([str(level) + "\n" for level in self._levels])

    def level_complete(self, time):
        self._levels[self._active_level].is_done = True
        self._levels[self._active_level].time = time
        self._bonuses[self._active_level].set_color_t(YELLOW_COLOR)
        index = self._cursor.get_index()
        if index < NB_LEVELS - 1:
            self._cursor.set_index(index + 1)
        self.save_scores()

    def _load_resources(self):
        App.show_cursor(True)

        self._fonts = [
            Render.Font("assets/fonts/IMPOS-30.ttf", 35),
            Render.Font("assets/fonts/IMPOS-30.ttf", 70),
            Render.Font("assets/fonts/IMPOS-30.ttf", 20)
        ]

        self._levels = [
            LockerLevel(Locker1(), 0),
            LockerLevel(Locker2(), 1),
            LockerLevel(Locker3(), 2),
            LockerLevel(Locker4(), 3)
        ]

        self._bonuses = [
            Render.Image("assets/Footprint.png", scale=0.273, color=GRAY_COLOR),
            Render.Image("assets/Lock.png", scale=0.273, color=GRAY_COLOR),
            Render.Image("assets/Clock.png", scale=0.273, color=GRAY_COLOR),
            Render.Image("assets/Clock.png", scale=0.273, color=GRAY_COLOR)
        ]

        self._cursor = MenuCursor()

        self.load_scores()

    def update(self):
        self._elapsed_time += App.get_time()

        if self._active_level is not None:
            self._levels[self._active_level].update()
        else:
            self._cursor.update()
            cursor_index = self._cursor.get_index()
            if IO.Keyboard.is_down(K_LEFT):
                if cursor_index > 0:
                    self._cursor.set_index(cursor_index - 1)
            elif IO.Keyboard.is_up(K_RIGHT):
                if cursor_index < NB_LEVELS - 1 and self._levels[cursor_index].is_done:
                    self._cursor.set_index(cursor_index + 1)
            elif IO.Keyboard.is_down(K_RETURN):
                self.activate_level(cursor_index, self)

        if IO.Keyboard.is_down(K_ESCAPE):
            App.exit()

    def activate_level(self, index, master_scene):
        self._active_level = index
        self._levels[self._active_level].init_scene(master_scene)

    def draw(self):
        if self._active_level is None:
            # Title
            dx, dy = App.get_screen_size()
            ddx = int(dx / 4)
            bx, by, bw, bh = (int(dx / 4), int(dy - 100), int(dx / 2), 80)
            bdx = int(bw / 4)

            self._fonts[1].draw_text("Bichnel's lockerS", (dx / 2, 50), YELLOW_COLOR, center_x=True)
            self._fonts[0].draw_text("level %i" % (self._cursor.get_index() + 1), (dx / 2, (dy / 2) + 80), YELLOW_COLOR, center_x=True)

            for i in range(NB_LEVELS):
                level = self._levels[i]
                x = ddx * i + ddx / 2
                x2 = ddx * (i + 1) + ddx / 2
                bxx = bdx * i + bdx / 2

                # Drawing level circles
                if level.is_done:
                    self._fonts[2].draw_text("%.2fs" % level.time, (int(x), int(dy / 2) - 70), YELLOW_COLOR, center_x=True)

                pygame.draw.circle(App.get_display(), RED_COLOR if not level.is_done else GREEN_COLOR, (int(x), int(dy / 2)), 25, 1 if not level.is_done else 0)
                if i < NB_LEVELS - 1:
                    pygame.draw.line(App.get_display(), RED_COLOR if not level.is_done else GREEN_COLOR, (int(x + 25), int(dy / 2)), (int(x2 - 25), int(dy / 2)))

                # Drawing Bonus circles
                pygame.draw.circle(App.get_display(), GRAY_COLOR if not level.is_done else YELLOW_COLOR, (bx + int(bxx), by + int(bh / 2)), 25, 1)

                self._bonuses[i].draw(bx + int(bxx), by + int(bh / 2), at_center=True)

            self._cursor.draw()
            pygame.draw.circle(App.get_display(), YELLOW_COLOR, (int(ddx * self._cursor.get_index() + ddx / 2), int(dy / 2)), 35, 1)

        else:
            self._levels[self._active_level].draw()