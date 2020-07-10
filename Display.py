# import time

import Game
import pygame


class Display:
    def __init__(self, block, block2, width, length, size_window, background, map_game):
        self.Width, self.Length = width, length
        self.block = block
        self.block2 = block2
        self.size_window = size_window
        self.background = background
        # self.ii = 0
        self.map = map_game
        # self.i1 = time.time() + 1

    def display_update(self, n, x_case, y_case):
        try:
            if n == 4:
                block_2 = self.block2[self.map[x_case][y_case][4]]
                Game.Screen.blit(block_2[0],
                                 (x_case * 64 - 128 - (Game.x + 32) % 64 + block_2[1],
                                  y_case * 64 - 128 - (Game.y + 32) % 64 + block_2[2]))
            else:
                Game.Screen.blit(self.block[self.map[x_case][y_case][n]],
                                 (x_case * 64 - 128 - (Game.x + 32) % 64, y_case * 64 - 128 - (Game.y + 32) % 64))
        except KeyError:
            pass

    def display_game(self):
        Game.Screen.blit(self.background, (0, 0))
        for X_case in range(2, 14):
            for Y_case in range(2, 15):
                if self.map[X_case][Y_case] is not None:
                    self.display_update(0, X_case, Y_case)
                    self.display_update(1, X_case, Y_case)
                    self.display_update(2, X_case, Y_case)
        Game.Screen.blit(Game.player.image, (11 * 32, 11 * 32))
        for X_case in range(16):
            for Y_case in range(19):
                if self.map[X_case][Y_case] is not None:
                    self.display_update(4, X_case, Y_case)
        if Game.menu == 0:
            Game.button_shop.display_button()
            Game.button_menu.display_button()
        elif Game.menu == 1:
            self.display_pause()

    def display_pause(self):
        s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        Game.Screen.blit(s, (0, 0))
        Game.button_pause.display_button()
        Game.button_setting.display_button()
        Game.button_save.display_button()
        Game.button_exit.display_button()

    def display(self, map_game):
        self.map = map_game
        self.display_game()
        pygame.display.flip()
        # self.ii += 1
        # if time.time() > self.i1:
        #    print(self.ii)
        #    self.i1 = time.time() + 1
        #    self.ii = 0
