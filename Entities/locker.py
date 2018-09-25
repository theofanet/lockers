from Entities.selector import Selector

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2


class Locker:

    def __init__(self, lockers_data):
        self.direction_up = LOCKER_UP
        self.direction_down = LOCKER_DOWN
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

    def update_position(self, direction, win_pos, mirror=False):
        self.blocked_triggered = False
        # up or mirror down.
        if direction == self.direction_up or (mirror and direction == self.direction_down):
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
        # down or mirror up.
        elif direction == self.direction_down or (mirror and direction == self.direction_up):
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
