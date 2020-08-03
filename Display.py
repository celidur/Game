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
            Game.Texts.plain: (68, 255, 0),
            Game.Texts.desert: (249, 210, 39),
            Game.Texts.snow: (152, 249, 219),
            Game.Texts.forest: (11, 109, 13),
            Game.Texts.mountain: (123, 95, 62),
            Game.Texts.volcano: (163, 41, 18)}

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
            self.arial.render("{} : {}/{}  {} : {}/{}".format(Game.Texts.hp, player_stats[0], player_stats[1],
                                                              Game.Texts.mp, player_stats[2], player_stats[3]),
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
                self.arial.render("{}   {}".format(Game.Texts.attack_stat, Game.Texts.defense_stat), False,
                                  (255, 255, 255)), (530, 420))
            # base
            Game.Screen.blit(self.arial.render("Base", False, (255, 255, 255)), (430, 460))
            Game.Screen.blit(self.arial.render(str(attack_base), False, (255, 255, 255)),
                             (585 - len(str(defense_base)) * 8, 460))
            Game.Screen.blit(self.arial.render(str(defense_base), False, (255, 255, 255)),
                             (665 - len(str(defense_base)) * 8, 460))
            # plaine
            Game.Screen.blit(self.arial.render(Game.Texts.plain, False, (68, 255, 0)), (430, 500))
            Game.Screen.blit(self.arial.render('+' + str(attack_plain), False, (255, 255, 255)),
                             (585 - len(str(attack_plain) + '+') * 8, 500))
            Game.Screen.blit(self.arial.render('+' + str(defense_plain), False, (255, 255, 255)),
                             (665 - len(str(defense_plain) + '+') * 8, 500))

            # désert
            Game.Screen.blit(self.arial.render(Game.Texts.desert, False, (249, 210, 39)), (430, 530))
            Game.Screen.blit(self.arial.render('+' + str(attack_desert), False, (255, 255, 255)),
                             (585 - len(str(attack_desert) + '+') * 8, 530))
            Game.Screen.blit(self.arial.render('+' + str(defense_desert), False, (255, 255, 255)),
                             (665 - len(str(defense_desert) + '+') * 8, 530))

            # neige
            Game.Screen.blit(self.arial.render(Game.Texts.snow, False, (152, 249, 219)), (430, 560))
            Game.Screen.blit(self.arial.render('+' + str(attack_snow), False, (255, 255, 255)),
                             (585 - len(str(attack_snow) + '+') * 8, 560))
            Game.Screen.blit(self.arial.render('+' + str(defense_snow), False, (255, 255, 255)),
                             (665 - len(str(defense_snow) + '+') * 8, 560))

            # forêt
            Game.Screen.blit(self.arial.render(Game.Texts.forest, False, (11, 109, 13)), (430, 590))
            Game.Screen.blit(self.arial.render('+' + str(attack_forest), False, (255, 255, 255)),
                             (585 - len(str(attack_forest) + '+') * 8, 590))
            Game.Screen.blit(self.arial.render('+' + str(defense_forest), False, (255, 255, 255)),
                             (665 - len(str(defense_forest) + '+') * 8, 590))

            # montagne
            Game.Screen.blit(self.arial.render(Game.Texts.mountain, False, (123, 95, 62)), (430, 620))
            Game.Screen.blit(self.arial.render('+' + str(attack_mountain), False, (255, 255, 255)),
                             (585 - len(str(attack_mountain) + '+') * 8, 620))
            Game.Screen.blit(self.arial.render('+' + str(defense_mountain), False, (255, 255, 255)),
                             (665 - len(str(defense_mountain) + '+') * 8, 620))

            # volcan
            Game.Screen.blit(self.arial.render(Game.Texts.volcano, False, (163, 41, 18)), (430, 650))
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
                                 (255, 255, 255), 270, False)

        elif Game.fight_mode == 2:
            Game.button_magic1.display_button()
            Game.button_magic2.display_button()
            Game.button_magic3.display_button()
            Game.button_magic4.display_button()
            Game.button_back.display_button()
            Display.display_text(self, Game.Texts.description_magic.format(11, 11, 11, 11), 400, 405, 'FRAMDCN.TTF',
                                 16, False,
                                 (255, 255, 255), 270, False)
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
                                 '{}|{} : {}'.format(inventory[1][(y + scroll) * 5 + x][0], Game.Texts.quantity,
                                                     inventory[1][(y + scroll) * 5 + x][1]), 580, 420,
                                 'FRAMDCN.TTF', 16, False,
                                 (255, 255, 255), 150, False)
            Display.display_text(self, "La description de l'objet n°{} arrive bientôt...".format(
                inventory[1][(y + scroll) * 5 + x][0]), 520,
                                 470,
                                 'FRAMDCN.TTF', 16, False,
                                 (255, 255, 255), 180, False)
            Game.button_back.display_button(280, 670, 'center')
            if int(inventory[1][(y + scroll) * 5 + x][1]) > 0:
                Game.button_use.display_button()
                Game.use_ = [True, inventory[1][(y + scroll) * 5 + x][0]]
            else:
                Game.use_ = [False, None]
        # zone actions
        if not Game.texts:
            text = "Selectionnez une action."
            change = True
        if change:
            if Game.texts == '':
                Game.texts = text
            else:
                Game.texts += '|'+text
        while True:
            x, y = 0, 0
            texts = Game.texts.split('|')
            for text in texts:
                text = text.split(' ')
                for word in text:
                    x += self.dialogue.size(word)[0]
                    if x >= 250:
                        y += 18
                        x = 0
                    x += self.dialogue.size(' ')[0]
                x = 0
                y += 18
            if y > 291:
                Game.texts.remove(Game.texts[0])
            else:
                break
        if change:
            Display.display_text(self, Game.texts, 35, 415, 'rpg_.FON', 16, 0.05, (255, 255, 255), 250, True)
        else:
            Display.display_text(self, Game.texts, 35, 415, 'rpg_.FON', 16, False, (255, 255, 255), 250, True)
        Game.change = False
        if Game.fight_mode == 4:
            s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            Game.Screen.blit(s, (0, 0))
            Game.button_confirm.display_button()
            Game.button_back.display_button(433, 348, 'center')

    def display_text(self, texts, x_pos, y_pos, font, size, prog, color, length, change_old):
        font = pygame.font.Font("font/" + font, size)
        x, y = 0, 0
        texts = texts.split('|')
        for i in range(len(texts)):
            texts[i] = texts[i].split(' ')
            line, lw = '', 0
            for word in texts[i]:
                if prog == False:
                    lw += font.size(word)[0]
                    if x + lw < length or line == '':
                        line += word + ' '
                    elif x + lw >= length or word == texts[i][-1]:
                        if change_old and i < len(texts):
                            Game.Screen.blit(font.render(line, False, (color[0] // 2, color[1] // 2, color[2] // 2)), (x_pos + x, y_pos + y))
                        else:
                            Game.Screen.blit(font.render(line, False, color), (x_pos + x, y_pos + y))
                        line, lw, x, y = word + ' ', 0, 0, y + size
                else:
                    if x + font.size(word)[0] >= length:
                        x = 0
                        y += size
                    for char in word:
                        if i == len(texts)-1:
                            Game.Screen.blit(self.dialogue.render(char, False, color), (x_pos + x, y_pos + y))
                            pygame.display.flip()
                            time.sleep(prog)
                        elif change_old:
                            Game.Screen.blit(self.dialogue.render(char, False, (color[0] // 2, color[1] // 2, color[2] // 2)), (x_pos + x, y_pos + y))
                        x += font.size(char)[0]
                    x += font.size(' ')[0]
                    pass
            if change_old and i < len(texts)-1:
                Game.Screen.blit(font.render(line, False, (color[0] // 2, color[1] // 2, color[2] // 2)), (x_pos + x, y_pos + y))
            else:
                Game.Screen.blit(font.render(line, False, color), (x_pos + x, y_pos + y))
            x = 0
            y += size
