from PyGnin import *
from random import randint
from Entities.locker import Locker
import pygame


class Grid:

    def __init__(self, lockers_data):
        # screen x y.
        self._screen_x, self._screen_y = App.get_screen_size()
        self.scale = 4

        # locker const data.
        self._lockers_data = lockers_data

        # grid attributes.
        self.l = self._lockers_data["nb"] * self._lockers_data["l"] * self.scale
        self.w = self._lockers_data["w"] * 2
        self.y = (self._screen_y / 2) - (self.w / 2)
        self.x = (self._screen_x / 2) - (self.l / 2)
        self.rect = None

        # global start position.
        self.start_pos = (self._screen_x / 2) + (self.l / 2)

        # lockers grid attributes.
        self.lockers_list = [Locker(lockers_data) for _ in range(self._lockers_data["nb"])]
        self.lockers_win = [0 for _ in range(self._lockers_data["nb"])]
        self.locker_win_nb = 0
        self.selected_locker = 0

    def initiate(self, mixed=False):
        # set locker and selector modifiers.
        locker_modifier = self._lockers_data["l"] * 1.5
        selector_modifier = self._lockers_data["l"] * 1.7

        # generate initial/win/footprint lockers and associated selectors.
        for index in range(len(self.lockers_list)):
            # selected locker isolation.
            locker = self.lockers_list[index]

            # define locker positions.
            locker_pos_y = (self._screen_y / 2) - (locker.w / 2)
            locker_pos_x = self.start_pos - locker_modifier
            locker.position = randint(0, 2)
            y_modifier = 0
            if locker.position == 0:
                y_modifier -= 30
            elif locker.position == 2:
                y_modifier += 30
            locker.rect = pygame.Rect(locker_pos_x, locker_pos_y + y_modifier, locker.l, locker.w)

            # define win positions.
            self.lockers_win[index] = randint(0, 2)
            while self.lockers_win[index] == locker.position:
                self.lockers_win[index] = randint(0, 2)

            # define footprint positions.
            y_footprint = 0
            if self.lockers_win[index] == 0:
                y_footprint -= 30
            elif self.lockers_win[index] == 2:
                y_footprint += 30
            locker.footprint = pygame.Rect(locker_pos_x, locker_pos_y + y_footprint, locker.l, locker.w)

            # define selector positions.
            selector_pos_y = (self._screen_y / 2) - (locker.w * 1.5)
            selector_pos_x = self.start_pos - selector_modifier
            locker.selector.rect = pygame.Rect(selector_pos_x, selector_pos_y, locker.selector.l, locker.selector.w)

            # mixing locker type.
            if mixed:
                # odd for example.
                if index % 2:
                    locker.blocked_type = True

            # iterate next modifiers.
            locker_modifier += self._lockers_data["l"] * self.scale
            selector_modifier += self._lockers_data["l"] * self.scale

        # define grid rect.
        self.rect = pygame.Rect(self.x, self.y, self.l, self.w)

    def next_locker(self, current_index):
        if current_index < len(self.lockers_list) - 1:
            self.selected_locker += 1
        else:
            self.selected_locker = 0
