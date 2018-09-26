class Bonus(object):

    def __init__(self):
        self.duration = 0
        self.charges_max = 0
        self.charges_left = 0
        self.active = False

    def set_charge_duration(self, duration):
        self.duration = duration

    def set_charges_max(self, charges):
        self.charges_max = charges

    def set_charges_left(self, charges):
        self.charges_left = charges
