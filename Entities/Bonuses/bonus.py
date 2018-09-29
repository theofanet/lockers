from PyGnin import *
from Scenes.theme import *


class Bonus(object):

    def __init__(self, img, keyboard_key):
        self.duration = 0
        self.charges_max = 0
        self.charges_left = 0
        self.charge_start = 0
        self.active = False
        self.img = img
        self._key = keyboard_key

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
                self.active = True
                self.charges_left -= 1
                self.charge_start = App.get_time()

    def draw(self, x, y, font):
        self.img.set_color_t(COLOR_WIN if self.active else COLOR_DEFAULT).draw(x, y)
        font.draw_text(
            "%s" % self.charges_left,
            (x + 60, y),
            COLOR_WIN if self.active else COLOR_DEFAULT
        )
