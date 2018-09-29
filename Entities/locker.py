from Entities.selector import Selector

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2

DIRECTION_UP = 1
DIRECTION_DOWN = 2


class Locker:

    def __init__(self, lockers_data):
        self.direction_up = DIRECTION_UP
        self.direction_down = DIRECTION_DOWN
        self.blocked_triggered = False
        self.l = lockers_data["l"]
        self.w = lockers_data["w"]
        self.selector = Selector(lockers_data)
        self.win_position = False
        self.rect = None
        self.footprint = None
        self.discover = False
        self.position = None
        self.blocked_type = False
        self.disruptor = None

    def attach(self, disruptor):
        self.disruptor = disruptor
        self.disruptor.x = self.rect.x - (self.l / 0.8)

    def update_position(self, direction, win_pos):
        self.blocked_triggered = False
        if direction == self.direction_up:
            if self.position > LOCKER_UP:
                self.rect.y -= 30
                self.position -= 1
            elif self.blocked_type:
                self.blocked_triggered = True
                return
            else:
                self.rect.y += 60
                self.position = LOCKER_DOWN

            if self.position == win_pos:
                self.win_position = True
                return True

            self.win_position = False
            return False
        elif direction == self.direction_down:
            if self.position < LOCKER_DOWN:
                self.rect.y += 30
                self.position += 1
            elif self.blocked_type:
                self.blocked_triggered = True
                return
            else:
                self.rect.y -= 60
                self.position = LOCKER_UP

            if self.position == win_pos:
                self.win_position = True
                return True

            self.win_position = False
            return False
