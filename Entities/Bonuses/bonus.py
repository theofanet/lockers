class Bonus(object):

    def __init__(self):
        self._duration = None
        self._charges_max = None
        self._charges_left = None

    def set_duration(self, duration):
        self._duration = duration

    def set_max_charges(self, charges):
        self._charges_max = charges
