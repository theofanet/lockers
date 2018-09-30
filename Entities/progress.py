import pygame


class Progress:

    def __init__(self, pos_data):
        # grid data.
        self._pos_data = pos_data

        # progress attributes.
        self.diff = 2
        # out rect.
        self.out_y = self._pos_data["y"]
        self.out_x = self._pos_data["x"]
        self.out_h = self._pos_data["h"]
        self.out_w = self._pos_data["w"]
        self.rect_out = None
        # in rect.
        self.in_y = self._pos_data["y"] + (self.diff / 2)
        self.in_x = self._pos_data["x"] + (self.diff / 2)
        self.in_h = self._pos_data["h"] - self.diff
        self.in_w = self._pos_data["w"] - self.diff
        self.rect_in = None

    def initiate(self):
        self.rect_out = pygame.Rect(self.out_x, self.out_y, self.out_h, self.out_w)
        self.rect_in = pygame.Rect(self.in_x, self.in_y, self.in_h, self.in_w)

    def track_timer(self, current, max_t):
        percent = current / max_t * self.in_h
        self.rect_in.width = self.in_h - percent
