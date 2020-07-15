import time

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
        self.arial = pygame.font.SysFont("arial", 20)
        self.rpg = pygame.font.Font("font/rpg_.ttf", 15)

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

    def display_fight(self, background, monster, size, hp, name, player_stats, fight_mode, change):
        Game.Screen.blit(background, (0, 0))
        Game.Screen.blit(monster, size)
        Game.Screen.blit(self.arial.render("{}/{}".format(hp[0], hp[1]), False, (255, 255, 255)), (570, 438))
        Game.Screen.blit(self.arial.render(name, False, (255, 255, 255)), (430, 438))
        Game.Screen.blit(self.arial.render("PV : {}/{}  PM : {}/{}".format(player_stats[0], player_stats[1],
                                                                           player_stats[2], player_stats[3]), False,
                                           (255, 255, 255)), (60, 438))
        Game.button_attack.display_button()
        Game.button_inventory.display_button()
        Game.button_run_fight.display_button()
        Game.button_magic.display_button()
        # zone stats
        feu = '8'
        Game.Screen.blit(self.arial.render("attaque | defense", False, (255, 255, 255)), (110, 480))
        # fire
        Game.Screen.blit(self.arial.render("feu", False, (255, 255, 255)), (40, 510))
        Game.Screen.blit(self.arial.render(feu, False, (255, 255, 255)), (160 - len(feu) * 8, 510))
        Game.Screen.blit(self.arial.render(feu, False, (255, 255, 255)), (230 - len(feu) * 8, 510))

        # zone actions
        text = "Ceci est une longue phrase. En voici une autre un peu plus longue."
        text = text.split(' ')
        if change:
            Game.texts.append(text)
        while True:
            x, y = 0, 0
            for text in Game.texts:
                for word in text:
                    x += len(word) * 8
                    if x >= 250:
                        y += 18
                        x = 0
                    x += 5
                x = 0
                y += 18
            if y > 216:
                Game.texts.remove(Game.texts[0])
            else:
                break
        x, y = 0, 0
        for t in range(len(Game.texts)):
            for word in Game.texts[t]:
                lw = len(word) * 8
                if x + lw >= 250:
                    y += 18
                    x = 0
                for char in word:
                    if t == len(Game.texts) - 1:
                        Game.Screen.blit(self.rpg.render(char, False, (255, 255, 255)), (430 + x, 485 + y))
                    else:
                        Game.Screen.blit(self.rpg.render(char, False, (180, 180, 180)), (430 + x, 485 + y))
                    x += 8
                    if change and t == len(Game.texts) - 1:
                        pygame.display.flip()
                        time.sleep(0.06)
                x += 5
            x = 0
            y += 18

        Game.change = False
