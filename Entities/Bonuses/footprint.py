from Entities.Bonuses.bonus import *


class Footprint(Bonus):

    def __init__(self, img, keyboard_key):
        super().__init__(img, keyboard_key)

    def initiate(self):
        self.active = False
        self.duration = 5
        self.charges_max = 2
        self.charges_left = 2
        self.charge_start = 0

    def update(self):
        super().update()
        if self.active:
            self.charge_start += App.get_time()
            if self.charge_start / 1000 >= self.duration:
                self.active = False
