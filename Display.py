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

    def display_fight(self, background, monster, size, hp, name, player_stats, pos_inventory, change, text):
        Game.Screen.blit(background, (0, 0))
        Game.Screen.blit(monster, size)
        Game.Screen.blit(
            self.arial.render("{} : {}/{}  {} : {}/{}".format(Game.Settings.hp, player_stats[0], player_stats[1],
                                                              Game.Settings.mp, player_stats[2], player_stats[3]),
                              False, (255, 255, 255)), (430, 357))
        Game.Screen.blit(self.arial.render(name[0], False, self.colors[name[1]]), (65, 357))
        Game.Screen.blit(self.arial.render("{}/{}".format(hp[0], hp[1]), False, (255, 255, 255)), (215, 357))
        if Game.fight_mode == 0 or Game.fight_mode == 4:
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
        elif Game.fight_mode == 1:
            Game.button_attack1.display_button()
            Game.button_attack2.display_button()
            Game.button_attack3.display_button()
            Game.button_attack4.display_button()
            Game.button_back.display_button()
            Display.display_text(self, Game.Texts.description_attack.format(20, 10, 6, 3, 24, 12, 20, 20), 400, 405,
                                 'FRAMDCN.TTF',
                                 16, False,
                                 (255, 255, 255), 270)

        elif Game.fight_mode == 2:
            Game.button_magic1.display_button()
            Game.button_magic2.display_button()
            Game.button_magic3.display_button()
            Game.button_magic4.display_button()
            Game.button_back.display_button()
            Display.display_text(self, Game.Texts.description_magic.format(11, 11, 11, 11), 400, 405, 'FRAMDCN.TTF',
                                 16, False,
                                 (255, 255, 255), 270)
        elif Game.fight_mode == 3:
            objects = [[str(i)] for i in range(52)]
            for i in range(len(objects)):
                objects[i].append(pow(2 ** (i ** (i + 1) % 5) + i ** 2 % 11, 12, 6))
            inventory = [[], objects, []]
            x, y, scroll = pos_inventory
            Game.Screen.blit(pygame.image.load('assets/inventory/set_cases_fight_0.png'), (270, 420))
            for l in range(5):
                for c in range(5):
                    if [x, y] == [c, l]:
                        Game.Screen.blit(pygame.image.load('assets/inventory/case_select.png'),
                                         (270 + x * 50, 420 + y * 50))
                    if (l + scroll) * 5 + c < 52:
                        Game.Screen.blit(
                            pygame.image.load(
                                'assets/inventory/potions/{}.png'.format(str(((l + scroll) * 5 + c) % 25))),
                            (274 + c * 50, 424 + l * 50))
                        if inventory[1][(l + scroll) * 5 + c][1] == 0:
                            Game.Screen.blit(pygame.image.load('assets/inventory/black.png'),
                                             (270 + c * 50, 420 + l * 50))
                    else:
                        Game.Screen.blit(pygame.image.load('assets/inventory/black.png'),
                                         (270 + c * 50, 420 + l * 50))
                    if [x, y] == [c, l]:
                        Game.Screen.blit(pygame.image.load('assets/inventory/case_select.png'),
                                         (270 + x * 50, 420 + y * 50))
            Game.Screen.blit(
                pygame.image.load('assets/inventory/potions/{}.png'.format(str(((y + scroll) * 5 + x) % 25))),
                (540, 420))
            Display.display_text(self,
                                 '{}|{} : {}'.format(inventory[1][(y + scroll) * 5 + x][0], Game.Settings.quantity,
                                                     inventory[1][(y + scroll) * 5 + x][1]), 580, 420,
                                 'FRAMDCN.TTF', 16, False,
                                 (255, 255, 255), 150)
            Display.display_text(self, "La description de l'objet n°{} arrive bientôt...".format(
                inventory[1][(y + scroll) * 5 + x][0]), 520,
                                 470,
                                 'FRAMDCN.TTF', 16, False,
                                 (255, 255, 255), 180)
            Game.button_back.display_button(280, 670, 'center')
            if int(inventory[1][(y + scroll) * 5 + x][1]) > 0:
                Game.button_use.display_button()
                Game.use_ = [True, inventory[1][(y + scroll) * 5 + x][0]]
            else:
                Game.use_ = [False, None]
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
        if Game.fight_mode == 4:
            s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            Game.Screen.blit(s, (0, 0))
            Game.button_confirm.display_button()
            Game.button_back.display_button(433, 348, 'center')

    def display_text(self, texts, x_pos, y_pos, font, size, prog, color, length):
        font = pygame.font.Font("font/" + font, size)
        x, y = 0, 0
        texts = texts.split('|')
        for text in texts:
            text = text.split(' ')
            p, lw = '', 0
            for word in text:
                if prog:
                    for char in word:
                        Game.Screen.blit(self.dialogue.render(char, False, (255, 255, 255)), (x_pos + x, y_pos + y))
                        x += size / 2
                        if char in ['i', 'l', 'f', '.', ',']:
                            x -= size / 4
                        x = int(x)
                        pygame.display.flip()
                        time.sleep(0.05)
                    x += size // 4
                    pass
                lw += len(word) * size / 2
                for char in word:
                    if char in ['i', 'l', 'f', '.', ',']:
                        lw -= size / 4
                x = int(x)
                if x + lw < length or p == '':
                    p += word + ' '
                elif x + lw >= length or word == text[-1]:
                    Game.Screen.blit(font.render(p, False, color), (x_pos + x, y_pos + y))
                    p, lw, x, y = word + ' ', 0, 0, y + size
            Game.Screen.blit(font.render(p, False, color), (x_pos + x, y_pos + y))
            x = 0
            y += size
