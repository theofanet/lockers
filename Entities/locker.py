from Entities.selector import Selector


class Locker:

    def __init__(self, lockers_data):
        self.l = lockers_data["l"]
        self.w = lockers_data["w"]
        self.selector = Selector(lockers_data)
        self.win_position = False
        self.rect = None
        self.footprint = None
        self.discover = False
        self.position = None
        self.blocked_type = False
