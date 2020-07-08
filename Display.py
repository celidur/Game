import time

import Game
import pygame


class Display:
    def __init__(self, block, block2, width, length, size_window, background):
        self.Width, self.Length = width, length
        self.block = block
        self.block2 = block2
        self.size_window = size_window
        self.frame = time.time()
        self.background = background
        self.ii = 0
        self.i1 = time.time() + 1

    def display_update(self, n, x_case, y_case):
        try:
            if n == 4:
                block_2 = self.block2[Game.Map[Game.x // 64 + x_case][Game.y // 64 + y_case][4]]
                Game.Screen.blit(block_2[0],
                                 (int((x_case + 5) * 64 - (Game.x % 64)) + block_2[1],
                                  int((y_case + 5) * 64 - (Game.y % 64) + block_2[2])))
            else:
                Game.Screen.blit(self.block[Game.Map[Game.x // 64 + x_case][Game.y // 64 + y_case][n]],
                                 (int((x_case + 5) * 64 - (Game.x % 64)), int((y_case + 5) * 64 - (Game.y % 64))))
        except KeyError:
            pass

    def display_case(self, x1, x2, y1, y2, n=0):
        for X_case in range(x1, (11 + 1) // 2 + x2):
            for Y_case in range(y1, y2):
                if 0 <= X_case + Game.x // 64 < self.Length and Game.y // 64 + Y_case >= 0 and \
                        Y_case + Game.y // 64 < self.Width:
                    if n == 4:
                        self.display_update(4, X_case, Y_case)
                    else:
                        self.display_update(0, X_case, Y_case)
                        self.display_update(1, X_case, Y_case)
                        self.display_update(2, X_case, Y_case)

    @staticmethod
    def house(c):
        if Game.Map[((Game.x + 32) // 64)][((Game.y + 32) // 64)][4] != c and \
                Game.Map[((Game.x + 32) // 64)][((Game.y + 32) // 64) - 1][4] != c:
            return True
        return False

    def display_game(self):
        Game.Screen.blit(self.background, (0, 0))
        self.display_case(-5, 3, -6, 8)
        if not (self.house('h1') and self.house('h2') and self.house('h3')):
            self.display_case(-9, 8, -8, 13, 4)
            Game.Screen.blit(Game.player.image, (11 // 2 * 64, 5 * 64))
        else:
            Game.Screen.blit(Game.player.image, (11 // 2 * 64, 5 * 64))
            self.display_case(-9, 8, -8, 13, 4)
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

    def display(self):
        if time.time() > self.frame:
            self.display_game()
            pygame.display.flip()
            self.frame = time.time() - 10
            self.ii += 1
        if time.time() > self.i1:
            print(self.ii)
            self.i1 = time.time() + 1
            self.ii = 0
