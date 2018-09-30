from Entities.Bonuses.bonus import *


class Hack(Bonus):

    def __init__(self, img, sound_f, sound_s, keyboard_key):
        super().__init__(img, sound_f, sound_s, keyboard_key)

    def initiate(self):
        self.active = False
        self.charges_max = 3
        self.charges_left = 3

    def update(self):
        if IO.Keyboard.is_down(self._key):
            if not self.active and self.charges_left > 0:
                    self.active = True
                    self.charges_left -= 1
                    self.charge_start = App.get_time()
            else:
                self.active = False
            self._scene.active_bonus(self)
