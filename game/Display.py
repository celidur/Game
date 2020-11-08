import time
import pygame


class Display:
    def __init__(self, size_window, Game):
        self.Game = Game
        self.list_ = []
        self.object = []
        self.size_window = size_window
        self.arial = pygame.font.Font("game/font/FRAMDCN.TTF", 20)
        self.dialogue = pygame.font.Font("game/font/rpg_.FON", 16)
        self.colors = {
            self.Game.Texts.plain: (68, 255, 0),
            self.Game.Texts.desert: (249, 210, 39),
            self.Game.Texts.snow: (152, 249, 219),
            self.Game.Texts.forest: (11, 109, 13),
            self.Game.Texts.mountain: (123, 95, 62),
            self.Game.Texts.volcano: (163, 41, 18)}

    def display_chunks(self, fight=False):
        i = (self.Game.x + 512) // 1024
        j = (self.Game.y + 512) // 1024
        image = []
        if fight:
            image.append(
                (self.Game.game_chunk[0], (0 - self.Game.x + 320 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j)))
            image.append(
                (self.Game.game_chunk[1], (0 - self.Game.x + 320 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j - 1024)))
            image.append(
                (self.Game.game_chunk[2], (0 - self.Game.x + 320 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j)))
            image.append((self.Game.game_chunk[3],
                          (0 - self.Game.x + 320 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j - 1024)))
            return 0
        if i < len(self.Game.map_chunk) and j < len(self.Game.map_chunk[0]):
            image.append((self.Game.map_chunk[i][j],
                          (0 - self.Game.x + 320 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j)))
        if i < len(self.Game.map_chunk) and j - 1 >= 0:
            image.append((self.Game.map_chunk[i][j - 1],
                          (0 - self.Game.x + 320 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j - 1024)))
        if i - 1 >= 0 and j < len(self.Game.map_chunk[0]):
            image.append((self.Game.map_chunk[i - 1][j],
                          (0 - self.Game.x + 320 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j)))
        if i - 1 >= 0 and j - 1 >= 0:
            image.append((self.Game.map_chunk[i - 1][j - 1],
                          (0 - self.Game.x + 320 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j - 1024)))
        return image

    def display_game(self):
        pygame.draw.rect(self.Game.Screen, (55, 25, 5), [0, 0, 1080, 768])
        placed = False
        self.object = self.display_chunks()
        for i in self.Game.entities:
            if (i[1] == self.Game.y and i[0] >= self.Game.x or i[1] > self.Game.y) and not placed:
                self.object.append((self.Game.player.image, (320, 320)))
                placed = True
            self.object.append((i[2].image, (i[2].x - self.Game.x + 320, i[2].y - self.Game.y + 320)))
        if not placed:
            self.object.append((self.Game.player.image, (320, 320)))
        self.Game.Screen.blits(self.object)
        """self.Game.player.all_projectiles.draw(self.Game.Screen)"""
        pygame.draw.rect(self.Game.Screen, (0, 255, 0), [704, 0, 1024, 768])
        if self.Game.menu == 0:
            if self.Game.area == 'village':
                self.Game.Screen = self.Game.button_shop.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_menu.display_button(self.Game.Screen)

    def display_pause(self):
        s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.Game.Screen.blit(s, (0, 0))
        self.Game.Screen = self.Game.button_pause.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_setting.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_save.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_exit.display_button(self.Game.Screen)

    def display_chest(self):
        s = pygame.Surface((328*2, 232*2), pygame.SRCALPHA)
        s.fill((7, 0, 0, 120))
        self.Game.Screen.blit(s, (23, 160))

    def display(self):  # #
        self.display_game()
        if self.Game.menu == 2:
            self.display_pause()
        elif self.Game.menu == 1:
            self.display_chest()
        pygame.display.flip()

    def display_fight(self):
        if self.Game.fight_mode == -2:
            if not self.Game.game_chunk:
                r = pygame.Surface((1024, 1024), pygame.SRCALPHA)
                try:
                    self.Game.game_chunk.append(
                        self.Game.map_chunk[(self.Game.x + 512) // 1024][(self.Game.y + 512) // 1024].copy())
                except IndexError:
                    self.Game.game_chunk.append(r.copy())
                try:
                    self.Game.game_chunk.append(
                        self.Game.map_chunk[(self.Game.x + 512) // 1024][(self.Game.y + 512) // 1024 - 1].copy())
                except IndexError:
                    self.Game.game_chunk.append(r.copy())
                try:
                    self.Game.game_chunk.append(
                        self.Game.map_chunk[(self.Game.x + 512) // 1024 - 1][(self.Game.y + 512) // 1024].copy())
                except IndexError:
                    self.Game.game_chunk.append(r.copy())
                try:
                    self.Game.game_chunk.append(self.Game.map_chunk[(self.Game.x + 512) // 1024 - 1]
                                                [(self.Game.y + 512) // 1024 - 1].copy())
                except IndexError:
                    self.Game.game_chunk.append(r.copy())
            if not self.list_:
                self.list_ = self.Game.list_coord.copy()
            for pxl in self.list_[:int(4 * 1024 * 1024 / 32)]:
                self.Game.game_chunk[pxl[0]].set_at((pxl[1], pxl[2]), (0, 0, 0, 0))
            del self.list_[:int(4 * 1024 * 1024 / 32)]
            self.Game.Screen.blit(self.Game.enemy_.background, (0, 0))
            Display.display_chunks(self, True)
            pygame.display.flip()
            if len(self.list_) == 0:
                self.Game.fight_mode = -1
                self.Game.game_chunk = []
            return 0
        if self.Game.fight_mode == -1:
            self.Game.fight_mode = 0
            pygame.time.delay(250)
            self.Game.Screen.blit(self.Game.enemy_.background, (0, 0))
            pygame.display.flip()
            pygame.time.delay(500)
            self.Game.Screen.blit(self.Game.enemy_.image, self.Game.enemy_.size)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.enemy_.name, False,
                                                                 self.Game.display.colors[
                                                                     self.Game.enemy_.environment]), (65, 357))
            self.Game.Screen.blit(
                self.Game.display.arial.render(
                    "{}/{}".format(self.Game.enemy_.hp, self.Game.enemy_.hp_max), False,
                    (255, 255, 255)), (215, 357))
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen = self.Game.button_attack.display_button(self.Game.Screen)
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen = self.Game.button_magic.display_button(self.Game.Screen)
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen = self.Game.button_inventory.display_button(self.Game.Screen)
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen = self.Game.button_leave.display_button(self.Game.Screen)
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen.blit(self.Game.display.arial.render(
                "{} : {}/{}  {} : {}/{}".format(self.Game.Texts.hp, self.Game.player.hp,
                                                self.Game.player.hp_max,
                                                self.Game.Texts.mp, self.Game.player.mp,
                                                self.Game.player.mp_max),
                False,
                (255, 255, 255)), (430, 357))
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen.blit(pygame.image.load('game/assets/battle/backgrounds/stats.png'), (418, 420))
            pygame.display.flip()
            pygame.time.delay(250)
            self.Game.Screen.blit(
                self.Game.display.arial.render(
                    "{}   {}".format(self.Game.Texts.attack_stat, self.Game.Texts.defense_stat), False,
                    (255, 255, 255)), (530, 440))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render("Base", False, (255, 255, 255)), (430, 480))
            self.Game.Screen.blit(
                self.Game.display.arial.render(
                    str(self.Game.player.attack + self.Game.player.sword.get_stat()[0]), False,
                    (255, 255, 255)), (585 - len(str(self.Game.player.attack +
                                                     self.Game.player.sword.get_stat()[0])) * 8, 480))
            self.Game.Screen.blit(
                self.Game.display.arial.render(
                    str(self.Game.player.defense + self.Game.player.armor.get_stat()[0]), False,
                    (255, 255, 255)), (665 - len(str(self.Game.player.defense +
                                                     self.Game.player.armor.get_stat()[0])) * 8, 480))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.plain, False, (68, 255, 0)),
                                  (430, 520))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[1]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[6]) + '+') * 8, 520))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[1]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[6]) + '+') * 8, 520))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.desert, False, (249, 210, 39)),
                                  (430, 550))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[2]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[2]) + '+') * 8, 550))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[2]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[2]) + '+') * 8, 550))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.snow, False, (152, 249, 219)),
                                  (430, 580))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[3]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[1]) + '+') * 8, 580))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[3]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[1]) + '+') * 8, 580))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.forest, False, (11, 109, 13)),
                                  (430, 610))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[4]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[3]) + '+') * 8, 610))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[4]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[3]) + '+') * 8, 610))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.mountain, False, (123, 95, 62)),
                                  (430, 640))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[5]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[5]) + '+') * 8, 640))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[5]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[5]) + '+') * 8, 640))
            pygame.display.flip()
            pygame.time.delay(100)
            self.Game.Screen.blit(self.Game.display.arial.render(self.Game.Texts.volcano, False, (163, 41, 18)),
                                  (430, 670))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.sword.get_stat()[6]), False,
                                               (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[4]) + '+') * 8, 670))
            self.Game.Screen.blit(
                self.Game.display.arial.render('+' + str(self.Game.player.armor.get_stat()[6]), False,
                                               (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[4]) + '+') * 8, 670))
            pygame.display.flip()
            pygame.time.delay(250)
        self.Game.Screen.blit(self.Game.enemy_.background, (0, 0))
        self.Game.Screen.blit(self.Game.enemy_.image, self.Game.enemy_.size)
        self.Game.Screen.blit(
            self.arial.render("{} : {}/{}  {} : {}/{}".format(self.Game.Texts.hp, self.Game.player.hp,
                                                              self.Game.player.hp_max, self.Game.Texts.mp,
                                                              self.Game.player.mp, self.Game.player.mp_max),
                              False, (255, 255, 255)), (430, 357))
        self.Game.Screen.blit(self.arial.render(self.Game.enemy_.name, False,
                                                self.colors[self.Game.enemy_.environment]), (65, 357))
        self.Game.Screen.blit(self.arial.render("{}/{}".format(self.Game.enemy_.hp, self.Game.enemy_.hp_max), False,
                                                (255, 255, 255)), (215, 357))
        if self.Game.fight_mode == 0 or self.Game.fight_mode == 4:
            self.Game.Screen = self.Game.button_attack.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_magic.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_inventory.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_leave.display_button(self.Game.Screen)
            self.Game.Screen.blit(pygame.image.load('game/assets/battle/backgrounds/stats.png'), (418, 420))
            self.Game.Screen.blit(
                self.arial.render("{}   {}".format(self.Game.Texts.attack_stat, self.Game.Texts.defense_stat), False,
                                  (255, 255, 255)), (530, 440))
            # base
            self.Game.Screen.blit(self.arial.render("Base", False, (255, 255, 255)), (430, 480))
            self.Game.Screen.blit(
                self.arial.render(
                    str(self.Game.player.attack + self.Game.player.sword.get_stat()[0]), False,
                    (255, 255, 255)),
                (
                    585 - len(
                        str(self.Game.player.attack + self.Game.player.sword.get_stat()[0])) * 8,
                    480))
            self.Game.Screen.blit(
                self.arial.render(
                    str(self.Game.player.defense + self.Game.player.armor.get_stat()[0]), False,
                    (255, 255, 255)),
                (
                    665 - len(
                        str(self.Game.player.defense + self.Game.player.armor.get_stat()[0])) * 8,
                    480))
            # plaine
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.plain, False, (68, 255, 0)), (430, 520))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[1]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[6]) + '+') * 8, 520))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[1]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[6]) + '+') * 8, 520))

            # désert
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.desert, False, (249, 210, 39)), (430, 550))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[2]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[2]) + '+') * 8, 550))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[2]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[2]) + '+') * 8, 550))

            # neige
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.snow, False, (152, 249, 219)), (430, 580))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[3]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[1]) + '+') * 8, 580))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[3]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[1]) + '+') * 8, 580))

            # forêt
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.forest, False, (11, 109, 13)), (430, 610))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[4]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[3]) + '+') * 8, 610))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[4]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[3]) + '+') * 8, 610))

            # montagne
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.mountain, False, (123, 95, 62)), (430, 640))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[5]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[5]) + '+') * 8, 640))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[5]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[5]) + '+') * 8, 640))

            # volcan
            self.Game.Screen.blit(self.arial.render(self.Game.Texts.volcano, False, (163, 41, 18)), (430, 670))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.sword.get_stat()[6]), False, (255, 255, 255)),
                (585 - len(str(self.Game.player.sword.get_stat()[4]) + '+') * 8, 670))
            self.Game.Screen.blit(
                self.arial.render('+' + str(self.Game.player.armor.get_stat()[6]), False, (255, 255, 255)),
                (665 - len(str(self.Game.player.armor.get_stat()[4]) + '+') * 8, 670))
        elif self.Game.fight_mode == 1:
            self.Game.Screen = self.Game.button_attack1.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_attack2.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_attack3.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_attack4.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_back.display_button(self.Game.Screen)
            Display.display_text(self, self.Game.Texts.description_attack.format(self.Game.attack_player(1, False),
                                                                                 self.Game.attack_player(2, False),
                                                                                 4 * self.Game.attack_player(2, False),
                                                                                 self.Game.attack_player(3, False),
                                                                                 int(self.Game.attack_player(3, False)
                                                                                     * 0.25),
                                                                                 self.Game.attack_player(4, False)),
                                 400, 415,
                                 'FRAMDCN.TTF',
                                 15, 0,
                                 (255, 255, 255), 270, False)

        elif self.Game.fight_mode == 2:
            self.Game.Screen = self.Game.button_magic1.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_magic2.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_magic3.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_magic4.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_back.display_button(self.Game.Screen)
            Display.display_text(self,
                                 self.Game.Texts.description_magic.format(
                                     self.Game.magic_player(1, False) - self.Game.player.hp, 10, 12), 400,
                                 415,
                                 'FRAMDCN.TTF', 15, 0, (255, 255, 255), 270, False)
        elif self.Game.fight_mode == 3:
            x, y, scroll = self.Game.pos_inventory
            self.Game.Screen.blit(pygame.image.load('game/assets/inventory/set_cases_fight_0.png'), (270, 420))
            for line in range(5):
                for colone in range(5):
                    if [x, y] == [colone, line]:
                        self.Game.Screen.blit(pygame.image.load('game/assets/inventory/case_select.png'),
                                              (270 + x * 50, 420 + y * 50))
                    if (line + scroll) * 5 + colone < 36:
                        self.Game.Screen.blit(
                            pygame.image.load('game/assets/inventory/potions/{}.png'.format(
                                str(((line + scroll) * 5 + colone) % 25))),
                            (274 + colone * 50, 424 + line * 50))
                        if self.Game.player.inventory[1][(line + scroll) * 5 + colone] == 0:
                            self.Game.Screen.blit(pygame.image.load('game/assets/inventory/black.png'),
                                                  (270 + colone * 50, 420 + line * 50))
                    else:
                        self.Game.Screen.blit(pygame.image.load('game/assets/inventory/black.png'),
                                              (270 + colone * 50, 420 + line * 50))
                    if [x, y] == [colone, line]:
                        self.Game.Screen.blit(pygame.image.load('game/assets/inventory/case_select.png'),
                                              (270 + x * 50, 420 + y * 50))
            self.Game.Screen.blit(
                pygame.image.load('game/assets/inventory/potions/{}.png'.format(str(((y + scroll) * 5 + x) % 25))),
                (520, 410))
            Display.display_text(self, self.Game.Texts.description_object[(y + scroll) * 5 + x][0], 560, 410,
                                 'FRAMDCN.TTF',
                                 16, 0, (255, 255, 255), 120, False)
            Display.display_text(self, "{} : {}||{}".format(
                self.Game.Texts.quantity, self.Game.player.inventory[1][(y + scroll) * 5 + x],
                self.Game.use_object((y + scroll) * 5 + x, False)), 520, 450, 'FRAMDCN.TTF', 16, 0,
                                 (255, 255, 255), 160, False)
            self.Game.Screen = self.Game.button_back.display_button(self.Game.Screen, 280, 670, 'center')
            if self.Game.player.inventory[1][(y + scroll) * 5 + x] > 0:
                self.Game.Screen = self.Game.button_use.display_button(self.Game.Screen)
                self.Game.use_obj = True
            else:
                self.Game.use_obj = False
        # zone actions
        if self.Game.texts == '':
            self.Game.texts = self.Game.Texts.select_action
            self.Game.change = True
        while True:
            x, y = 0, 0
            texts = self.Game.texts.split('|')
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
                self.Game.texts = self.Game.texts.split('|')
                del self.Game.texts[0]
                self.Game.texts = '|'.join(self.Game.texts)
            else:
                break
        if self.Game.change:
            Display.display_text(self, self.Game.texts, 35, 415, 'rpg_.FON', 16, self.Game.prog, (255, 255, 255), 230,
                                 True, True)
        else:
            Display.display_text(self, self.Game.texts, 35, 415, 'rpg_.FON', 16, 0, (255, 255, 255), 230, True, True)
        self.Game.change = False
        if self.Game.fight_mode == 4:
            s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            self.Game.Screen.blit(s, (0, 0))
            self.Game.Screen = self.Game.button_confirm.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_back.display_button(self.Game.Screen, 433, 348, 'center')

    def display_text(self, texts, x_pos, y_pos, font, size, prog, color, length, change_old, point=False):
        font_ = pygame.font.Font("game/font/" + font, size)
        x, y = 0, 0
        texts = texts.split('|')
        for i in range(len(texts)):
            if point:
                font_2 = pygame.font.Font("game/font/FRAMDCN.TTF", 32)
                if prog == 0:
                    if change_old and i < len(texts) - 1:
                        self.Game.Screen.blit(
                            font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                            (x_pos - 10, y_pos + y - 16))
                    else:
                        self.Game.Screen.blit(font_2.render('·', False, color),
                                              (x_pos - 10, y_pos + y - 16))
                else:
                    if i < len(texts) - prog:
                        self.Game.Screen.blit(
                            font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                            (x_pos - 10, y_pos + y - 16))
                    else:
                        self.Game.Screen.blit(font_2.render('·', False, color),
                                              (x_pos - 10, y_pos + y - 16))
            texts[i] = texts[i].split(' ')
            line = ''
            for word in texts[i]:
                if prog == 0:
                    if font_.size(line + word)[0] < length or line == '':
                        line += word + ' '
                    elif font_.size(line + word)[0] >= length or word == texts[i][-1]:
                        if change_old and i < len(texts) - 1:
                            self.Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7,
                                                                             color[2] // 1.7)),
                                                  (x_pos, y_pos + y))
                        else:
                            self.Game.Screen.blit(font_.render(line, False, color), (x_pos, y_pos + y))
                        line, y = word + ' ', y + size
                else:
                    if x + font_.size(word)[0] >= length:
                        x = 0
                        y += size
                    for char in word:
                        if i >= len(texts) - prog:
                            self.Game.Screen.blit(self.dialogue.render(char, False, color), (x_pos + x, y_pos + y))
                            pygame.display.flip()
                            time.sleep(0.05)
                            if char == '.':
                                time.sleep(0.5)
                        elif change_old:
                            self.Game.Screen.blit(
                                self.dialogue.render(char, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                (x_pos + x, y_pos + y))
                        x += font_.size(char)[0]
                    x += font_.size(' ')[0]
                    pass
            if change_old and i < len(texts) - 1:
                self.Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                      (x_pos + x, y_pos + y))

            else:
                self.Game.Screen.blit(font_.render(line, False, color), (x_pos + x, y_pos + y))
            x = 0
            y += size
