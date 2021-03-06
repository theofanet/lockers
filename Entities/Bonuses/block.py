from Entities.Bonuses.bonus import *


class Block(Bonus):

    def __init__(self, img, sound_f, sound_s, keyboard_key):
        super().__init__(img, sound_f, sound_s, keyboard_key)

    def initiate(self):
        self.active = False
        self.charges_max = 4
        self.charges_left = 4

    def update(self):
        if IO.Keyboard.is_down(self._key):
            if not self.active and self.charges_left > 0:
                    self._sound_f.play()
                    self.active = True
                    self.charges_left -= 1
                    self.charge_start = App.get_time()
            else:
                self._sound_s.play()
                self.active = False
            self._scene.active_bonus(self)
