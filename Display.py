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
        self.arial = pygame.font.Font("font/FRAMDCN.TTF", 20)
        self.dialogue = pygame.font.Font("font/rpg_.FON", 16)
        self.colors = {
            Game.Settings.plain: (68, 255, 0),
            Game.Settings.desert: (249, 210, 39),
            Game.Settings.snow: (152, 249, 219),
            Game.Settings.forest: (11, 109, 13),
            Game.Settings.mountain: (123, 95, 62),
            Game.Settings.volcano: (163, 41, 18)}

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

    def display_fight(self, background, monster, size, hp, name, player_stats, fight_mode, change, text):
        Game.Screen.blit(background, (0, 0))
        Game.Screen.blit(monster, size)
        Game.Screen.blit(self.arial.render(
            "{} : {}/{}  {} : {}/{}".format(Game.Settings.hp, player_stats[0], player_stats[1], Game.Settings.mp,
                                            player_stats[2], player_stats[3]), False, (255, 255, 255)), (65, 357))
        Game.Screen.blit(self.arial.render(name[0], False, self.colors[name[1]]), (420, 357))
        Game.Screen.blit(self.arial.render("{}/{}".format(hp[0], hp[1]), False, (255, 255, 255)), (560, 357))
        Game.button_attack.display_button()
        Game.button_inventory.display_button()
        Game.button_magic.display_button()
        Game.button_leave.display_button()
        # zone stats
        attack_base, defense_base = 50, 20
        attack_plain, defense_plain = 8, 0
        attack_desert, defense_desert = 2, 3
        attack_snow, defense_snow = 0, 0
        attack_forest, defense_forest = 12, 15
        attack_mountain, defense_mountain = 7, 9
        attack_volcano, defense_volcano = 14, 1
        Game.Screen.blit(
            self.arial.render("{}   {}".format(Game.Settings.attack_stat, Game.Settings.defense_stat), False,
                              (255, 255, 255)), (530, 420))
        # base
        Game.Screen.blit(self.arial.render("Base", False, (255, 255, 255)), (430, 460))
        Game.Screen.blit(self.arial.render(str(attack_base), False, (255, 255, 255)),
                         (585 - len(str(defense_base)) * 8, 460))
        Game.Screen.blit(self.arial.render(str(defense_base), False, (255, 255, 255)),
                         (665 - len(str(defense_base)) * 8, 460))
        # plaine
        Game.Screen.blit(self.arial.render(Game.Settings.plain, False, (68, 255, 0)), (430, 500))
        Game.Screen.blit(self.arial.render('+' + str(attack_plain), False, (255, 255, 255)),
                         (585 - len(str(attack_plain) + '+') * 8, 500))
        Game.Screen.blit(self.arial.render('+' + str(defense_plain), False, (255, 255, 255)),
                         (665 - len(str(defense_plain) + '+') * 8, 500))

        # désert
        Game.Screen.blit(self.arial.render(Game.Settings.desert, False, (249, 210, 39)), (430, 530))
        Game.Screen.blit(self.arial.render('+' + str(attack_desert), False, (255, 255, 255)),
                         (585 - len(str(attack_desert) + '+') * 8, 530))
        Game.Screen.blit(self.arial.render('+' + str(defense_desert), False, (255, 255, 255)),
                         (665 - len(str(defense_desert) + '+') * 8, 530))

        # neige
        Game.Screen.blit(self.arial.render(Game.Settings.snow, False, (152, 249, 219)), (430, 560))
        Game.Screen.blit(self.arial.render('+' + str(attack_snow), False, (255, 255, 255)),
                         (585 - len(str(attack_snow) + '+') * 8, 560))
        Game.Screen.blit(self.arial.render('+' + str(defense_snow), False, (255, 255, 255)),
                         (665 - len(str(defense_snow) + '+') * 8, 560))

        # forêt
        Game.Screen.blit(self.arial.render(Game.Settings.forest, False, (11, 109, 13)), (430, 590))
        Game.Screen.blit(self.arial.render('+' + str(attack_forest), False, (255, 255, 255)),
                         (585 - len(str(attack_forest) + '+') * 8, 590))
        Game.Screen.blit(self.arial.render('+' + str(defense_forest), False, (255, 255, 255)),
                         (665 - len(str(defense_forest) + '+') * 8, 590))

        # montagne
        Game.Screen.blit(self.arial.render(Game.Settings.mountain, False, (123, 95, 62)), (430, 620))
        Game.Screen.blit(self.arial.render('+' + str(attack_mountain), False, (255, 255, 255)),
                         (585 - len(str(attack_mountain) + '+') * 8, 620))
        Game.Screen.blit(self.arial.render('+' + str(defense_mountain), False, (255, 255, 255)),
                         (665 - len(str(defense_mountain) + '+') * 8, 620))

        # volcan
        Game.Screen.blit(self.arial.render(Game.Settings.volcano, False, (163, 41, 18)), (430, 650))
        Game.Screen.blit(self.arial.render('+' + str(attack_volcano), False, (255, 255, 255)),
                         (585 - len(str(attack_volcano) + '+') * 8, 650))
        Game.Screen.blit(self.arial.render('+' + str(defense_volcano), False, (255, 255, 255)),
                         (665 - len(str(defense_volcano) + '+') * 8, 650))

        # zone actions
        text = text.split(' ')
        if not Game.texts:
            text = "Voix ambiguë d'un coeur qui au zéphyr préfère les jattes de kiwis.  1234567890".split(' ')
            change = True
        if change:
            Game.texts.append(text)
        while True:
            x, y = 0, 0
            for text in Game.texts:
                for word in text:
                    x += len(word) * 8
                    for i in ['i', '1', '.', ':', ',', ';', "'", '!']:
                        x -= word.count(i) * 4
                    if x >= 250:
                        y += 18
                        x = 0
                    x += 5
                x = 0
                y += 18
            if y > 291:
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
                        Game.Screen.blit(self.dialogue.render(char, False, (255, 255, 255)), (35 + x, 415 + y))
                    else:
                        Game.Screen.blit(self.dialogue.render(char, False, (180, 180, 180)), (35 + x, 415 + y))
                    x += 8
                    if change and t == len(Game.texts) - 1:
                        pygame.display.flip()
                        time.sleep(0)
                x += 4
            x = 0
            y += 18

        Game.change = False
