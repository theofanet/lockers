from PyGnin import *
from Entities.grid import Grid
from Entities.progress import Progress
from Scenes.theme import *
import pygame


LOCKERS_NB = 10
LOCKERS_L = 10
LOCKERS_W = 40

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2

STATE_WAIT = 0
STATE_WIN = 1
MAX_TIMER = 30


class Locker1(Game.SubScene):

    def __init__(self):
        super().__init__()
        # ### DEBUG MODE #####
        if DEBUG_MODE:
            App.show_cursor(True)
        # ####################

        # screen x y.
        self._screen_x, self._screen_y = App.get_screen_size()

        # font & image.
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf", 25)
        self._bonus = Render.Image("assets/Footprint.png", scale=1, color=COLOR_WIN)

        # generate grid.
        self.lockers_data = {"nb": LOCKERS_NB, "l": LOCKERS_L, "w": LOCKERS_W}
        self._grid = Grid(self.lockers_data)

        # generate progress bar.
        pos_data = {"x": self._grid.x, "y": self._grid.y + 110, "l": self._grid.l, "w": 10}
        self._progress = Progress(pos_data)

        # scene attributes.
        self._state = STATE_WAIT
        self._elapsed_time = 0

    def _initiate_data(self):
        self._grid.initiate()
        self._progress.initiate()

    def update(self):
        # ####### ESC #######
        if IO.Keyboard.is_down(K_ESCAPE):
            self._scene.return_menu()

        # game not won and timer still ok.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:
            self._elapsed_time += App.get_time()

            # update progress bar.
            percent = self._elapsed_time / 1000 / MAX_TIMER * self._progress.in_l
            self._progress.rect_in.width = self._progress.in_l - percent

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
        mid_x = self._screen_x / 2
        mid_y = self._screen_y / 2
        # game not won and timer still running.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:
            # print time left.
            if DEBUG_MODE:
                self._font.draw_text("%.2f" % (MAX_TIMER - (self._elapsed_time / 1000)), (self._progress.out_x - 70, self._progress.out_y - 15), COLOR_DEFAULT)

            # draw grid.
            pygame.draw.rect(App.get_display(), COLOR_DEFAULT, self._grid, 1)

            # draw lockers / footprints / probes / selectors.
            probe_modifier = self.lockers_data["l"] * 1.5
            for index in range(len(self._grid.lockers_list)):
                # lockers & footprints.
                locker = self._grid.lockers_list[index]
                if locker.discover:
                    pygame.draw.rect(App.get_display(), COLOR_FOOTPRINT, locker.footprint)
                pygame.draw.rect(App.get_display(), COLOR_DEFAULT, locker.rect, 1)

                # probes.
                probe_y = (self._screen_y / 2) - (locker.w * 1.7)
                probe_x = self._grid.start_pos - probe_modifier
                probe = ((probe_x, probe_y),
                         (probe_x-5, probe_y-5),
                         (probe_x-5, probe_y-15),
                         (probe_x, probe_y-20),
                         (probe_x+10, probe_y-20),
                         (probe_x+15, probe_y-15),
                         (probe_x+15, probe_y-5),
                         (probe_x+10, probe_y))
                pygame.draw.polygon(App.get_display(), COLOR_WIN if locker.win_position else COLOR_DEFAULT, probe, 1)
                probe_modifier += self.lockers_data["l"] * self._grid.scale

                # selector.
                if index == self._grid.selected_locker:
                    pygame.draw.rect(App.get_display(), (0, 0, 255), locker.selector.rect, 1)

            # progress bar.
            last_chance = self._elapsed_time / 1000 / MAX_TIMER
            pygame.draw.rect(App.get_display(), COLOR_DEFAULT, self._progress.rect_out, 1)
            pygame.draw.rect(App.get_display(), COLOR_WARNING if last_chance >= 0.7 else COLOR_WIN, self._progress.rect_in)

        # winning case.
        elif self._state == STATE_WIN:
                score = MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000))
                self._font.draw_text("%.2f" % score, (mid_x - (mid_x / 2), mid_y), COLOR_DEFAULT)
                self._bonus.draw(mid_x - (mid_x / 2) + 60, mid_y - 40)
                self._font.draw_text("Footprint unlocked !", (mid_x - (mid_x / 2) + 180, mid_y), COLOR_WIN)
        # loosing case.
        else:
            self._font.draw_text("Try again !", (mid_x - (mid_x / 8), mid_y), COLOR_WARNING)
