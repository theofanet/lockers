from Entities.Bonuses.bonus import *


class Clock(Bonus):

    def __init__(self, img, keyboard_key):
        super().__init__(img, keyboard_key)

    def initiate(self):
        self.active = False
        self.duration = 20
        self.charges_max = 1
        self.charges_left = 1
        self.charge_start = 0

    def update(self):
        if self.active:
            self.charge_start += App.get_time()
            if self.charge_start / 1000 >= self.duration:
                self.active = False
                self.charges_left -= 1
                self._scene.active_bonus(self)

        if IO.Keyboard.is_down(self._key):
            if not self.active and self.charges_left > 0:
                self.active = True
            else:
                self.active = False
            self._scene.active_bonus(self)

    def draw(self, x, y, font):
        self.img.set_color_t(COLOR_WIN if self.active else COLOR_DEFAULT).draw(x, y)
        font.draw_text(
            "%d" % (self.duration - (self.charge_start / 1000)),
            (x + 60, y),
            COLOR_WIN if self.active else COLOR_DEFAULT
        )
