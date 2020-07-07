import time

import Game
import pygame


class Display:
    def __init__(self, block, block2, Width, Length, size_window, background):
        self.Width, self.Length = Width, Length
        self.block = block
        self.block2 = block2
        self.size_window = size_window
        self.frame = time.time()
        self.background = background
        self.ii = 0
        self.i1 = time.time() + 1

    @staticmethod
    def Afficher_case(block, x_case, y_case, move_x=0, move_y=0):
        Game.Screen.blit(block,
                         (int((x_case + 5) * 64 - (Game.x % 64)) + move_x,
                          int((y_case + 5) * 64 - (Game.y % 64) + move_y)))

    def Screen_update(self, n, X_case, Y_case):
        try:
            if n == 4:
                block_2 = self.block2[Game.Map[Game.x // 64 + X_case][Game.y // 64 + Y_case][4]]
                self.Afficher_case(block_2[0], X_case, Y_case, block_2[1], block_2[2])
            else:
                self.Afficher_case(self.block[Game.Map[Game.x // 64 + X_case][Game.y // 64 + Y_case][n]], X_case,
                                   Y_case)
        except KeyError:
            pass

    def management_Screen(self, X1, X2, Y1, Y2, n=0):
        for X_case in range(X1, (11 + 1) // 2 + X2):
            for Y_case in range(Y1, Y2):
                if 0 <= X_case + Game.x // 64 < self.Length and Game.y // 64 + Y_case >= 0 and Y_case + Game.y // 64 < self.Width:
                    if n == 4:
                        self.Screen_update(4, X_case, Y_case)
                    else:
                        self.Screen_update(0, X_case, Y_case)
                        self.Screen_update(1, X_case, Y_case)
                        self.Screen_update(2, X_case, Y_case)

    @staticmethod
    def house(c):
        if Game.Map[((Game.x + 32) // 64)][((Game.y + 32) // 64)][4] != c and \
                Game.Map[((Game.x + 32) // 64)][((Game.y + 32) // 64) - 1][4] != c:
            return True
        return False

    def display_game(self):
        Game.Screen.blit(self.background, (0, 0))
        self.management_Screen(-5, 3, -6, 8)
        if not self.house('h1') and self.house('h2') and self.house('h3'):
            self.management_Screen(-9, 8, -8, 13, 4)
            Game.Screen.blit(Game.player.image, (11 // 2 * 64, 5 * 64))
        else:
            Game.Screen.blit(Game.player.image, (11 // 2 * 64, 5 * 64))
            self.management_Screen(-9, 8, -8, 13, 4)
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
