class Selector:

    def __init__(self, lockers_data):
        self.l = lockers_data["l"] * 1.5
        self.w = lockers_data["w"] * 3
        self.rect = None
