from PyGnin import *
from Entities.grid import Grid
from Entities.progress import Progress
from Scenes.theme import *
import pygame

LOCKERS_NB = 10
LOCKERS_H = 10
LOCKERS_W = 40

MAX_TIMER = 40


class Locker1(Game.SubScene):

    def __init__(self, bonuses=[]):
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
        self.lockers_data = {"nb": LOCKERS_NB, "h": LOCKERS_H, "w": LOCKERS_W}
        self._grid = None

        # generate progress bar.
        self._progress = None

        # scene attributes.
        self._elapsed_time = 0
        self._rz = False

        # bonuses.
        self._bonuses = bonuses

    def _initiate_data(self):
        self._elapsed_time = 0
        self._set_state(STATE_WAIT)
        self._grid = Grid(self.lockers_data)
        self._grid.initiate()
        pos_data = {"x": self._grid.x, "y": self._grid.y + 110, "h": self._grid.h, "w": 10}
        self._progress = Progress(pos_data)
        self._progress.initiate()
        self._rz = False

        self._sfx["amb1"].set_volume(0.3)
        self._sfx["amb1"].play()

    def update(self):
        # ####### TIMER #######
        elapsed_time_s = self._elapsed_time / 1000

        # ####### ESC #######
        if IO.Keyboard.is_down(K_ESCAPE):
            self._scene.return_menu()
            self._sfx["amb1"].stop()
            self._sfx["rz"].stop()

        # ####### GENERAL #######
        if self._state == STATE_WAIT and MAX_TIMER > elapsed_time_s:
            self._elapsed_time += App.get_time()

            # win condition check.
            if self._grid.locker_win_nb == self.lockers_data["nb"]:
                self._set_state(STATE_WIN)
                self._sfx["clap2"].play(0)
                self._scene.level_complete(MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000)))

            # selected locker.
            i = self._grid.selected_locker
            l = self._grid.lockers_list[i]
            wl_helper = self._grid.lockers_win[i]
            old_win_status = l.win_position

            # progress bar.
            # self._progress.track_timer(elapsed_time_s, MAX_TIMER)

            # ####### UP #######
            if IO.Keyboard.is_down(K_UP):
                # set locker position.
                win_pos = l.update_position(l.direction_up, wl_helper)
                if win_pos:
                    self._grid.locker_win_nb += 1
                    self._sfx["trig"].play()
                else:
                    if old_win_status:
                        self._grid.locker_win_nb -= 1
                    self._sfx["click"].play()

                # move to next locker.
                self._grid.next_locker(i)

            # ####### DOWN #######
            elif IO.Keyboard.is_down(K_DOWN):
                # set locker position.
                win_pos = l.update_position(l.direction_down, wl_helper)
                if win_pos:
                    self._grid.locker_win_nb += 1
                    self._sfx["trig"].play()
                else:
                    if old_win_status:
                        self._grid.locker_win_nb -= 1
                    self._sfx["click"].play()

                # move to next locker.
                self._grid.next_locker(i)

    def draw(self, camera=None, screen=None):
        mid_x = self._screen_x / 2
        mid_y = self._screen_y / 2
        # game not won and timer still running.
        if self._state == STATE_WAIT and MAX_TIMER > self._elapsed_time / 1000:

            # ### DEBUG MODE #####
            if DEBUG_MODE:
                self._fonts["perm"].draw_text("%.2f" % (MAX_TIMER - (self._elapsed_time / 1000)), (self._progress.out_x - 70, self._progress.out_y - 15), COLOR_DEFAULT)
            # ####################

            # draw bonuses.
            o_x, o_y = 200, 100
            i = 0
            for bonus, check in self._bonuses:
                bonus.draw(o_x + i * 80, o_y, self._fonts["perm"], check)
                i += 1

            # draw grid.
            pygame.draw.rect(App.get_display(), COLOR_DEFAULT, self._grid, 1)

            # draw lockers / footprints / probes / selectors.
            probe_modifier = self.lockers_data["h"] * 1.5
            for index in range(len(self._grid.lockers_list)):
                # lockers.
                locker = self._grid.lockers_list[index]
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
                probe_modifier += self.lockers_data["h"] * self._grid.scale

                # selector.
                if index == self._grid.selected_locker:
                    pygame.draw.rect(App.get_display(), (0, 0, 255), locker.selector.rect, 1)

            # progress bar.
            pygame.draw.rect(App.get_display(), COLOR_DEFAULT, self._progress.rect_out, 1)
            pygame.draw.rect(App.get_display(), COLOR_DEFAULT, self._progress.rect_in)

        # winning case.
        elif self._state == STATE_WIN:
                score = MAX_TIMER - (MAX_TIMER - (self._elapsed_time / 1000))
                self._fonts["perm"].draw_text("%.2f" % score, (mid_x - (mid_x / 2), mid_y), COLOR_DEFAULT)
                self._bonuses_img["fp"].draw(mid_x - (mid_x / 2) + 60, mid_y - 40)
                self._fonts["perm"].draw_text("Footprint unlocked !", (mid_x - (mid_x / 2) + 180, mid_y), COLOR_WIN)

                # sound effects.
                self._sfx["amb1"].fadeout(6000)
        # loosing case.
        else:
            self._fonts["perm"].draw_text("Try again !", (mid_x - (mid_x / 8), mid_y), COLOR_WARNING)

            # sound effects.
            self._sfx["amb1"].fadeout(4000)
