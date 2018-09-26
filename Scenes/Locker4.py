from PyGnin import *
from Entities.grid import Grid
from Entities.progress import Progress
from Scenes.theme import *
import pygame


LOCKERS_NB = 20
LOCKERS_L = 10
LOCKERS_W = 40

MAX_TIMER = 60


class Locker4(Game.SubScene):

    def __init__(self):
        super().__init__()
        # ### DEBUG MODE #####
        if DEBUG_MODE:
            App.show_cursor(True)
        # ####################

        # screen x y.
        self._screen_x, self._screen_y = App.get_screen_size()

        # assets.
        self._fonts = {}
        self._bonuses_img = {}
        self._sfx = {}
        for k, v in FONTS.items():
            self._fonts[k] = Render.Font(v, 25)
        for k, v in BONUSES_IMG.items():
            self._bonuses_img[k] = Render.Image(v, scale=1, color=COLOR_WIN)
        for k, v in SOUND_FX.items():
            self._sfx[k] = pygame.mixer.Sound(v)

        # generate grid.
        self.lockers_data = {"nb": LOCKERS_NB, "l": LOCKERS_L, "w": LOCKERS_W}
        self._grid = Grid(self.lockers_data)

        # generate progress bar.
        pos_data = {"x": self._grid.x, "y": self._grid.y + 110, "l": self._grid.l, "w": 10}
        self._progress = Progress(pos_data)

        # scene attributes.
        self._state = STATE_WAIT
        self._elapsed_time = 0
        self._rz = False

    def _initiate_data(self, **kargs):
        self._grid.initiate()
        self._progress.initiate()
        self._sfx["amb4"].play()

    def update(self):
        # ####### TIMER #######
        self._elapsed_time += App.get_time()
        elapsed_time_s = self._elapsed_time / 1000

        # ####### ESC #######
        if IO.Keyboard.is_down(K_ESCAPE):
            self._scene.return_menu()
            self._sfx["amb4"].stop()
            self._sfx["rz"].stop()

        # ####### GENERAL #######
        if self._state == STATE_WAIT and MAX_TIMER > elapsed_time_s:
            # win condition check.
            if self._grid.locker_win_nb == self.lockers_data["nb"]:
                self._set_state(STATE_WIN)
                self._scene.level_complete(MAX_TIMER - (MAX_TIMER - elapsed_time_s))

            # selected locker and mirror.
            i = self._grid.selected_locker
            l = self._grid.lockers_list[i]
            m = self._grid.lockers_list[len(self._grid.lockers_list) - 1 - i]
            wl_helper = self._grid.lockers_win[i]
            wm_helper = self._grid.lockers_win[len(self._grid.lockers_list) - 1 - i]

            # progress bar.
            self._progress.track_timer(elapsed_time_s, MAX_TIMER)

            # ####### UP #######
            if IO.Keyboard.is_down(K_UP):
                # set locker position.
                win_pos = l.update_position(l.direction_up, wl_helper)
                if win_pos:
                    l.discover = True
                    self._grid.locker_win_nb += 1
                    self._sfx["trig"].play()
                else:
                    self._grid.locker_win_nb -= 1
                    self._sfx["click"].play()

                # set mirror position.
                win_pos_m = m.update_position(m.direction_down, wm_helper)
                if win_pos_m:
                    m.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    self._grid.locker_win_nb -= 1

                # move to next locker.
                self._grid.next_locker(i)

            # ####### DOWN #######
            elif IO.Keyboard.is_down(K_DOWN):
                # set locker position.
                win_pos = l.update_position(l.direction_down, wl_helper)
                if win_pos:
                    l.discover = True
                    self._grid.locker_win_nb += 1
                    self._sfx["trig"].play()
                else:
                    self._grid.locker_win_nb -= 1
                    self._sfx["click"].play()

                # set mirror position.
                win_pos_m = m.update_position(m.direction_up, wm_helper)
                if win_pos_m:
                    m.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    self._grid.locker_win_nb -= 1

                # move to next locker.
                self._grid.next_locker(i)

    def draw(self, camera=None, screen=None):
        mid_x = self._screen_x / 2
        mid_y = self._screen_y / 2
        # game not won and timer still running.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:
            # print time left.
            if DEBUG_MODE:
                self._fonts["perm"].draw_text("%.2f" % (MAX_TIMER - (self._elapsed_time / 1000)), (self._progress.out_x - 70, self._progress.out_y - 15), COLOR_DEFAULT)

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
            if last_chance >= 0.7:
                pygame.draw.rect(App.get_display(), COLOR_WARNING, self._progress.rect_in)

                # sound effects.
                if not self._rz:
                    self._sfx["rz"].play()
                    self._rz = True
            else:
                pygame.draw.rect(App.get_display(), COLOR_WIN, self._progress.rect_in)

        # winning case.
        elif self._state == STATE_WIN:
                score = MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000))
                self._fonts["perm"].draw_text("%.2f" % score, (mid_x - (mid_x / 2), mid_y), COLOR_DEFAULT)
                self._bonuses_img["clk"].draw(mid_x - (mid_x / 2) + 60, mid_y - 40)
                self._fonts["perm"].draw_text("Stop timer unlocked !", (mid_x - (mid_x / 2) + 180, mid_y), COLOR_WIN)

                # sound effects.
                self._sfx["amb4"].fadeout(6000)
        # loosing case.
        else:
            self._fonts["perm"].draw_text("Try again !", (mid_x - (mid_x / 8), mid_y), COLOR_WARNING)

            # sound effects.
            self._sfx["amb4"].fadeout(4000)
