from PyGnin import *
from Entities.grid import Grid
import pygame

DEBUG_MODE = True

LOCKERS_NB = 10
LOCKERS_L = 10
LOCKERS_W = 40

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2

STATE_WAIT = 0
STATE_WIN = 1
MAX_TIMER = 100


class Locker1(Game.SubScene):

    def __init__(self):
        super().__init__()
        # ### DEBUG MODE #####
        if DEBUG_MODE:
            App.show_cursor(True)
        # ####################

        # font.
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")

        # generate grid.
        self.lockers_data = {"nb": LOCKERS_NB, "l": LOCKERS_L, "w": LOCKERS_W}
        self._grid = Grid(self.lockers_data)

        # scene attributes.
        self._state = STATE_WAIT
        self._elapsed_time = 0

    def _initiate_data(self):
        self._grid.initiate_grid()

    def update(self):
        # ####### ESC #######
        if IO.Keyboard.is_down(K_ESCAPE):
            self._scene.return_menu()

        # game not won and timer still ok.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:
            self._elapsed_time += App.get_time()

            # isolate selected locker index and associated Locker.
            i = self._grid.selected_locker
            l = self._grid.lockers_list[i]

            # win condition.
            if self._grid.locker_win_nb == self.lockers_data["nb"]:
                self._state = STATE_WIN
                self._scene.level_complete(MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000)))

            # ####### UP #######
            if IO.Keyboard.is_down(K_UP):
                # redefine locker position.
                if l.position > LOCKER_UP:
                    l.rect.y -= 30
                    l.position -= 1
                else:
                    l.rect.y += 60
                    l.position = LOCKER_DOWN

                # update win position attributes.
                if l.position == self._grid.lockers_win[i]:
                    l.win_position = True
                    l.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    if l.win_position:
                        l.win_position = False
                        self._grid.locker_win_nb -= 1

                # update selected locker index.
                if i < len(self._grid.lockers_list) - 1:
                    self._grid.selected_locker += 1
                else:
                    self._grid.selected_locker = 0

            # ####### DOWN #######
            elif IO.Keyboard.is_down(K_DOWN):
                # redefine locker position.
                if l.position < LOCKER_DOWN:
                    l.rect.y += 30
                    l.position += 1
                else:
                    l.rect.y -=60
                    l.position = LOCKER_UP

                # update win position attributes.
                if l.position == self._grid.lockers_win[i]:
                    l.win_position = True
                    l.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    if l.win_position:
                        l.win_position = False
                        self._grid.locker_win_nb -= 1

                # update selected locker index.
                if i < len(self._grid.lockers_list) - 1:
                    self._grid.selected_locker += 1
                else:
                    self._grid.selected_locker = 0

    def draw(self, camera=None, screen=None):
        # game not won and timer still running.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:
            # print time left.
            self._font.draw_text("%.2f" % (MAX_TIMER - (self._elapsed_time / 1000)), (10, 10), (255, 0, 0))

            # draw grid.
            pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)

            # draw lockers / footprints / selectors.
            for index in range(len(self._grid.lockers_list)):
                locker = self._grid.lockers_list[index]
                if locker.discover:
                    pygame.draw.rect(App.get_display(), (91, 91, 91), locker.footprint)
                pygame.draw.rect(App.get_display(), (0, 255, 0) if locker.win_position else (0, 255, 255), locker.rect)

                if index == self._grid.selected_locker:
                    pygame.draw.rect(App.get_display(), (0, 0, 255), locker.selector.rect, 1)
        # winning case.
        elif self._state == STATE_WIN:
                score = MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000))
                self._font.draw_text("%.2f" % score, (10, 10), (255, 0, 0))
                self._font.draw_text("Win !", (330, 20), (255, 0, 0))
        # loosing case.
        else:
            self._font.draw_text("Loose ...", (330, 20), (255, 0, 0))
