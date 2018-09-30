from PyGnin import *
from Scenes.theme import *

import pygame


class Bonus(object):

    def __init__(self, img, sound_f, sound_s, keyboard_key):
        self.duration = 0
        self.charges_max = 0
        self.charges_left = 0
        self.charge_start = 0
        self.active = False
        self.img = img
        self._sound_f = pygame.mixer.Sound(sound_f) if sound_f else None
        self._sound_s = pygame.mixer.Sound(sound_s) if sound_s else None
        self._key = keyboard_key
        self._scene = None

    def set_scene(self, scene):
        self._scene = scene
        return self

    def initiate(self):
        self.active = False
        self.duration = 0
        self.charges_max = 0
        self.charges_left = 0
        self.charge_start = 0

    def set_charge_duration(self, duration):
        self.duration = duration

    def set_charges_max(self, charges):
        self.charges_max = charges

    def set_charges_left(self, charges):
        self.charges_left = charges

    def update(self):
        if not self.active:
            if IO.Keyboard.is_down(self._key) and self.charges_left > 0:
                if self._sound_f:
                    self._sound_f.play()
                self.active = True
                self.charges_left -= 1
                self.charge_start = App.get_time()
                self._scene.active_bonus(self)

    def draw(self, x, y, font, check):
        if check:
            self.img.set_color_t(COLOR_WIN if self.active else COLOR_DEFAULT).draw(x, y)
            font.draw_text(
                "%s" % self.charges_left,
                (x + 60, y),
                COLOR_WIN if self.active else COLOR_DEFAULT
            )
        else:
            self.img.set_color_t(COLOR_GRAY).draw(x, y)
