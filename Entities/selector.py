class Selector:

    def __init__(self, lockers_data):
        self.l = lockers_data["h"] * 1.5
        self.w = lockers_data["w"] * 3
        self.rect = None
