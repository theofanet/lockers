from PyGnin import *
import pygame
import random

from .Locker1 import Locker1
from .Locker2 import Locker2
from .Locker3 import Locker3
from .Locker4 import Locker4
from .Final import Final

from Entities.Bonuses.footprint import Footprint
from Entities.Bonuses.block import Block
from Entities.Bonuses.clock import Clock
from Scenes.theme import BONUSES_IMG

from Entities.Particles import ParticleEmitter


NB_LEVELS = 4
RED_COLOR = (192, 57, 43)
GREEN_COLOR = (39, 174, 96)
YELLOW_COLOR = (241, 196, 15)
GRAY_COLOR = (149, 165, 166)
CURSOR_ANIMATION_SPEED = 30


PENTA = [
    (0, -1),
    (-0.588, 0.809),
    (0.951, -0.309),
    (-0.951, -0.309),
    (0.588, 0.809)
]

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

    def draw(self, x_offset=0, y_offset=0):
        dx, dy = App.get_screen_size()
        ddx = int(dx / 4)

        self._img.draw((ddx * self._index + ddx / 2) + x_offset, (dy / 2) + self._offset_y + y_offset, at_center=True)


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
        self._launch_final_animation = False
        self._final_animation_y_offset = 0
        self._final_animation_first_line_height = 0
        self._final_animation_second_line_width = 0
        self._final_animation_circle_radius = 0
        self._current_penta_line = 0
        self._current_penta_point = (0, 0)
        self._animation_time = 0
        dx, dy = App.get_screen_size()
        self._emitter = ParticleEmitter((-20, dy + 20), 500, (0, -80), life=4, size=30)
        self._emitter.set_ranges(x_range=(0, dx+20), life=(-2, 2), size=(-10, 10), y_range=(-80, 0))

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
            LockerLevel(Locker2([
                Footprint(Render.Image(BONUSES_IMG['fp'], scale=0.5, color=GRAY_COLOR), K_q)
            ]), 1),
            LockerLevel(Locker3([
                Footprint(Render.Image(BONUSES_IMG['fp'], scale=0.5, color=GRAY_COLOR), K_q),
                Block(Render.Image(BONUSES_IMG['blk'], scale=0.5, color=GRAY_COLOR), K_w)
            ]), 2),
            # LockerLevel(Locker4([
            #     Footprint(Render.Image(BONUSES_IMG['fp'], scale=0.5, color=GRAY_COLOR), K_q),
            #     Block(Render.Image(BONUSES_IMG['blk'], scale=0.5, color=GRAY_COLOR), K_w),
            #     Clock(Render.Image(BONUSES_IMG['clk'], scale=0.5, color=GRAY_COLOR), K_e)
            # ]), 3),
            LockerLevel(Final([
                Footprint(Render.Image(BONUSES_IMG['fp'], scale=0.5, color=GRAY_COLOR), K_q),
                Block(Render.Image(BONUSES_IMG['blk'], scale=0.5, color=GRAY_COLOR), K_w),
                Clock(Render.Image(BONUSES_IMG['clk'], scale=0.5, color=GRAY_COLOR), K_e)
            ]), 3)
        ]

        self._bonuses = [
            Render.Image(BONUSES_IMG['fp'], scale=0.273, color=GRAY_COLOR),
            Render.Image(BONUSES_IMG['blk'], scale=0.273, color=GRAY_COLOR),
            Render.Image(BONUSES_IMG['clk'], scale=0.273, color=GRAY_COLOR),
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

            self._emitter.update()

            if self._launch_final_animation:
                self._animation_time += App.get_time()
                dx, dy = App.get_screen_size()
                y_offset_max = int(dy / 2) - int(dy / 3)
                ddx = int(dx / 4)
                w = ddx * 3 + int(ddx / 2) - int(dx / 2) - 150
                h = y_offset_max + 70
                if self._final_animation_y_offset < y_offset_max:
                    self._final_animation_y_offset += 150 * (self._animation_time / 1000)
                    if self._final_animation_y_offset >= y_offset_max:
                        self._animation_time = 0
                elif self._final_animation_first_line_height < h:
                    self._final_animation_first_line_height += 100 * (self._animation_time / 1000)
                    if self._final_animation_first_line_height >= h:
                        self._animation_time = 0
                        self._final_animation_first_line_height = h
                elif self._final_animation_second_line_width < w:
                    self._final_animation_second_line_width += 150 * (self._animation_time / 1000)
                    if self._final_animation_second_line_width >= w:
                        self._animation_time = 0
                        self._final_animation_second_line_width = w
                elif self._final_animation_circle_radius < 150:
                    self._final_animation_circle_radius += 150 * (self._animation_time / 1000)
                    if self._final_animation_circle_radius >= 150:
                        self._animation_time = 0
                        self._final_animation_circle_radius = 150
                        self._current_penta_line = 1
                        self._current_penta_point = (150*PENTA[0][0], 150*PENTA[0][1])
                elif self._current_penta_line < 6:
                    x, y = (int(dx / 2), int(dy / 2) + 70)
                    lpx, lpy = PENTA[self._current_penta_line-1]
                    px, py = self._current_penta_point
                    npx, npy = PENTA[self._current_penta_line if self._current_penta_line < 5 else 0]
                    lp = Game.Vector(x + 150*lpx, y + 150*lpy)
                    p = Game.Vector(x + px, y + py)
                    np = Game.Vector(x + 150*npx, y + 150*npy)
                    nnp = lp.sub(np)
                    l = p.sub(np).length()
                    nnp.normalize()
                    if l > 15:
                        px = 150*lpx + 900 * nnp.x * (self._animation_time / 1000)
                        py = 150*lpy + 900 * nnp.y * (self._animation_time / 1000)
                        self._current_penta_point = (px, py)
                    else:
                        self._current_penta_point = (150*PENTA[self._current_penta_line if self._current_penta_line < 5 else 0][0], 150*PENTA[self._current_penta_line if self._current_penta_line < 5 else 0][1])
                        self._current_penta_line += 1
                        self._animation_time = 0
                elif self._animation_time > 700:
                    self._launch_final_animation = False

            if IO.Keyboard.is_down(K_LEFT):
                if cursor_index > 0:
                    self._cursor.set_index(cursor_index - 1)
            elif IO.Keyboard.is_up(K_RIGHT):
                if cursor_index < NB_LEVELS - 1 and self._levels[cursor_index].is_done:
                    self._cursor.set_index(cursor_index + 1)
            elif IO.Keyboard.is_down(K_RETURN):
                self.activate_level(cursor_index, self)
            elif IO.Keyboard.is_down(K_a):
                self._launch_final_animation = True
                self._final_animation_y_offset = 0
                self._animation_time = 0
                self._final_animation_first_line_height = 0
                self._final_animation_second_line_width = 0
                self._final_animation_circle_radius = 0

        if IO.Keyboard.is_down(K_ESCAPE):
            App.exit()


    def activate_level(self, index, master_scene):
        self._active_level = index
        self._levels[self._active_level].init_scene(master_scene)

    def draw(self):
        y_offset = int(self._final_animation_y_offset)

        if self._final_animation_y_offset > 0:
            self._emitter.draw()

        x_shake, y_shake = (0, 0)
        if self._launch_final_animation:
            x_shake, y_shake = (random.randint(-2, 2), random.randint(-2, 2))

        if self._active_level is None:
            # Title
            dx, dy = App.get_screen_size()
            ddx = int(dx / 4)
            bx, by, bw, bh = (int(dx / 4), int(dy - 100), int(dx / 2), 80)
            bdx = int(bw / 4)

            self._fonts[1].draw_text("Bichnel's lockerS", (dx / 2 + x_shake, 50 + y_shake), YELLOW_COLOR, center_x=True)

            for i in range(NB_LEVELS):
                level = self._levels[i]
                x = ddx * i + ddx / 2
                x2 = ddx * (i + 1) + ddx / 2
                bxx = bdx * i + bdx / 2

                # Drawing level circles
                if level.is_done:
                    self._fonts[2].draw_text("%.2fs" % level.time, (int(x) + x_shake, int(dy / 2) - 70 - y_offset + y_shake), YELLOW_COLOR, center_x=True)

                pygame.draw.circle(App.get_display(), RED_COLOR if not level.is_done else GREEN_COLOR, (int(x) + x_shake, int(dy / 2) - y_offset + y_shake), 25, 1 if not level.is_done else 0)
                if i < NB_LEVELS - 1:
                    pygame.draw.line(App.get_display(), RED_COLOR if not level.is_done else GREEN_COLOR, (int(x + 25) + x_shake, int(dy / 2) - y_offset + y_shake), (int(x2 - 25) + x_shake, int(dy / 2) - y_offset + y_shake))

                # Drawing Bonus circles
                pygame.draw.circle(App.get_display(), GRAY_COLOR if not level.is_done else YELLOW_COLOR, (bx + int(bxx) + x_shake, by + int(bh / 2) + y_shake), 25, 1)

                if level.is_done:
                    self._bonuses[i].draw(bx + int(bxx) + x_shake, by + int(bh / 2) + y_shake, at_center=True)

            if self._final_animation_first_line_height > 0:
                x = ddx * 3 + ddx / 2 + x_shake
                y = int(dy / 2) + 25 - y_offset + y_shake
                pygame.draw.line(App.get_display(), RED_COLOR, (int(x), int(y)), (int(x), int(y) + int(self._final_animation_first_line_height)))

            if self._final_animation_second_line_width > 0:
                x = ddx * 3 + ddx / 2 - self._final_animation_second_line_width + x_shake
                y = int(dy / 2) + 25 - y_offset + self._final_animation_first_line_height + y_shake
                pygame.draw.line(App.get_display(), RED_COLOR, (int(x), int(y)), (int(x + self._final_animation_second_line_width), int(y)))

            if self._final_animation_circle_radius > 0:
                pygame.draw.circle(App.get_display(), RED_COLOR, (int(dx / 2) + x_shake, int(dy / 2) + 70 + y_shake), int(self._final_animation_circle_radius), 1)

            if self._final_animation_circle_radius >= 150:
                x, y = (int(dx / 2) + x_shake, int(dy / 2) + 70 + y_shake)
                for i in range(0, self._current_penta_line - 1):
                    yy = i + 1 if i < 4 else 0
                    pygame.draw.line(App.get_display(), RED_COLOR,
                                    (x + int(150 * PENTA[i][0]), y + int(150 * PENTA[i][1])),
                                     (x + int(150 * PENTA[yy][0]), y + int(150 * PENTA[yy][1])))
                if self._current_penta_line <= 5:
                    pygame.draw.line(
                        App.get_display(), RED_COLOR,
                        (x + int(150*PENTA[self._current_penta_line-1][0]), y + int(150*PENTA[self._current_penta_line-1][1])),
                        (x + int(self._current_penta_point[0]), y + int(self._current_penta_point[1]))
                    )

            self._cursor.draw(x_shake, y_shake - y_offset)
            pygame.draw.circle(App.get_display(), YELLOW_COLOR, (int(ddx * self._cursor.get_index() + ddx / 2) + x_shake, int(dy / 2) - y_offset + y_shake), 35, 1)
        else:
            self._levels[self._active_level].draw()