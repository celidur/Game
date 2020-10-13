import time
from game import Game
import pygame


class Display:
    def __init__(self, block, block2, size_window, background):
        self.block = block
        self.block2 = block2
        self.list_ = []
        self.size_window = size_window
        self.background = background
        self.ii = 0
        self.i1 = time.time() + 1
        self.arial = pygame.font.Font("game/font/FRAMDCN.TTF", 20)
        self.dialogue = pygame.font.Font("game/font/rpg_.FON", 16)
        self.colors = {
            Game.Texts.plain: (68, 255, 0),
            Game.Texts.desert: (249, 210, 39),
            Game.Texts.snow: (152, 249, 219),
            Game.Texts.forest: (11, 109, 13),
            Game.Texts.mountain: (123, 95, 62),
            Game.Texts.volcano: (163, 41, 18)}

    def display_chunks(self, fight=False):
        i = (Game.x + 512) // 1024
        j = (Game.y + 512) // 1024
        if fight:
            Game.Screen.blit(Game.game_chunk[0],
                             (0 - Game.x + 320 + 1024 * i, 0 - Game.y + 320 + 1024 * j))
            Game.Screen.blit(Game.game_chunk[1],
                             (0 - Game.x + 320 + 1024 * i, 0 - Game.y + 320 + 1024 * j - 1024))
            Game.Screen.blit(Game.game_chunk[2],
                             (0 - Game.x + 320 + 1024 * i - 1024, 0 - Game.y + 320 + 1024 * j))
            Game.Screen.blit(Game.game_chunk[3],
                             (0 - Game.x + 320 + 1024 * i - 1024, 0 - Game.y + 320 + 1024 * j - 1024))
            return 0
        if i < len(self.map_chunk) and j < len(self.map_chunk[0]):
            Game.Screen.blit(self.map_chunk[i][j],
                             (0 - Game.x + 320 + 1024 * i, 0 - Game.y + 320 + 1024 * j))
        if i < len(Game.map_chunk) and j - 1 >= 0:
            Game.Screen.blit(self.map_chunk[i][j - 1],
                             (0 - Game.x + 320 + 1024 * i, 0 - Game.y + 320 + 1024 * j - 1024))
        if i - 1 >= 0 and j < len(self.map_chunk[0]):
            Game.Screen.blit(Game.map_chunk[i - 1][j],
                             (0 - Game.x + 320 + 1024 * i - 1024, 0 - Game.y + 320 + 1024 * j))
        if i - 1 >= 0 and j - 1 >= 0:
            Game.Screen.blit(self.map_chunk[i - 1][j - 1],
                             (0 - Game.x + 320 + 1024 * i - 1024, 0 - Game.y + 320 + 1024 * j - 1024))

    def display_game(self):
        Game.Screen.blit(self.background, (0, 0))
        self.display_chunks()
        for j in range(Game.y // 64 - 10, Game.y // 64 + 2):
            for i in range(Game.x // 64 - 10, Game.x // 64 + 10):
                if not (0 <= i < len(Game.map_object)) or not (0 <= j < len(Game.map_object[0])):
                    continue
                elif Game.map_object[i][j] == '':
                    continue
                if j * 64 < Game.y:
                    Game.Screen.blit(Game.block2[Game.map_object[i][j]][0],
                                     (i * 64 + Game.block2[Game.map_object[i][j]][1] - Game.x + 320,
                                      j * 64 + Game.block2[Game.map_object[i][j]][2] - Game.y + 320))

        for i in Game.enemy_map:
            if Game.y - i.y > 0:
                Game.Screen.blit(i.image, (320 + i.x - Game.x, 320 + i.y - Game.y))
        Game.Screen.blit(Game.player.image, (320, 320))
        Game.player.all_projectiles.draw(Game.Screen)
        for i in Game.enemy_map:
            if Game.y - i.y < 0:
                Game.Screen.blit(i.image, (320 + i.x - Game.x, 320 + i.y - Game.y))
        for j in range(Game.y // 64, Game.y // 64 + 14):
            for i in range(Game.x // 64 - 10, Game.x // 64 + 10):
                if not (0 <= i < len(Game.map_object)) or not (0 <= j < len(Game.map_object[0])):
                    continue
                elif Game.map_object[i][j] == '':
                    continue
                if j * 64 >= Game.y:
                    Game.Screen.blit(Game.block2[Game.map_object[i][j]][0],
                                     (i * 64 + Game.block2[Game.map_object[i][j]][1] - Game.x + 320,
                                      j * 64 + Game.block2[Game.map_object[i][j]][2] - Game.y + 320))
        if Game.menu == 0:
            if Game.area == 'village':
                Game.button_shop.display_button()
            Game.button_menu.display_button()

    def display_pause(self):
        s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        Game.Screen.blit(s, (0, 0))
        Game.button_pause.display_button()
        Game.button_setting.display_button()
        Game.button_save.display_button()
        Game.button_exit.display_button()

    def display(self, map_chunk):  # #
        self.map_chunk = map_chunk
        self.display_game()
        if Game.menu == 2 or Game.menu == 1:
            self.display_pause()
        pygame.display.flip()
        self.ii += 1
        if time.time() > self.i1:
            print("fps : {}".format(self.ii))
            self.i1 = time.time() + 1
            self.ii = 0

    def display_fight(self, background, monster, size, hp, name, player_stats, pos_inventory):
        if Game.fight_mode == -2:
            if not Game.game_chunk:
                r = pygame.Surface((1024, 1024), pygame.SRCALPHA)
                try:
                    Game.game_chunk.append(self.map_chunk[(Game.x + 512) // 1024][(Game.y + 512) // 1024].copy())
                except IndexError:
                    Game.game_chunk.append(r.copy())
                try:
                    Game.game_chunk.append(self.map_chunk[(Game.x + 512) // 1024][(Game.y + 512) // 1024 - 1].copy())
                except IndexError:
                    Game.game_chunk.append(r.copy())
                try:
                    Game.game_chunk.append(self.map_chunk[(Game.x + 512) // 1024 - 1][(Game.y + 512) // 1024].copy())
                except IndexError:
                    Game.game_chunk.append(r.copy())
                try:
                    Game.game_chunk.append(self.map_chunk[(Game.x + 512) // 1024 - 1]
                                           [(Game.y + 512) // 1024 - 1].copy())
                except IndexError:
                    Game.game_chunk.append(r.copy())
            if not self.list_:
                self.list_ = Game.list_coord.copy()
            for pxl in self.list_[:int(4 * 1024 * 1024 / 32)]:
                Game.game_chunk[pxl[0]].set_at((pxl[1], pxl[2]), (0, 0, 0, 0))
            del self.list_[:int(4 * 1024 * 1024 / 32)]
            Game.Screen.blit(Game.enemy_.get_background(), (0, 0))
            Display.display_chunks(self, True)
            pygame.display.flip()
            if len(self.list_) == 0:
                Game.fight_mode = -1
                Game.game_chunk = []
            return 0
        if Game.fight_mode == -1:
            Game.fight_mode = 0
            pygame.time.delay(250)
            Game.Screen.blit(Game.enemy_.get_background(), (0, 0))
            pygame.display.flip()
            pygame.time.delay(500)
            Game.Screen.blit(Game.enemy_.get_image(), Game.enemy_.get_size())
            Game.Screen.blit(Game.display.arial.render(Game.enemy_.get_name()[0], False,
                                                       Game.display.colors[Game.enemy_.get_name()[1]]), (65, 357))
            Game.Screen.blit(
                Game.display.arial.render("{}/{}".format(Game.enemy_.get_hp()[0], Game.enemy_.get_hp()[1]), False,
                                          (255, 255, 255)), (215, 357))
            pygame.display.flip()
            pygame.time.delay(250)
            Game.button_attack.display_button()
            pygame.display.flip()
            pygame.time.delay(250)
            Game.button_magic.display_button()
            pygame.display.flip()
            pygame.time.delay(250)
            Game.button_inventory.display_button()
            pygame.display.flip()
            pygame.time.delay(250)
            Game.button_leave.display_button()
            pygame.display.flip()
            pygame.time.delay(250)
            Game.Screen.blit(Game.display.arial.render(
                "{} : {}/{}  {} : {}/{}".format(Game.Texts.hp, Game.player.get_stats()[0], Game.player.get_stats()[1],
                                                Game.Texts.mp, Game.player.get_stats()[2], Game.player.get_stats()[3]),
                False,
                (255, 255, 255)), (430, 357))
            pygame.display.flip()
            pygame.time.delay(250)
            Game.Screen.blit(pygame.image.load('game/assets/battle/backgrounds/stats.png'), (418, 420))
            pygame.display.flip()
            pygame.time.delay(250)
            Game.Screen.blit(
                Game.display.arial.render("{}   {}".format(Game.Texts.attack_stat, Game.Texts.defense_stat), False,
                                          (255, 255, 255)), (530, 440))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render("Base", False, (255, 255, 255)), (430, 480))
            Game.Screen.blit(
                Game.display.arial.render(
                    str(Game.player.get_stats()[4] + Game.player.get_equipment()[0].get_stat()[0]), False,
                    (255, 255, 255)),
                (585 - len(str(Game.player.get_stats()[4] + Game.player.get_equipment()[0].get_stat()[0])) * 8, 480))
            Game.Screen.blit(
                Game.display.arial.render(
                    str(Game.player.get_stats()[5] + Game.player.get_equipment()[1].get_stat()[0]), False,
                    (255, 255, 255)),
                (665 - len(str(Game.player.get_stats()[5] + Game.player.get_equipment()[1].get_stat()[0])) * 8, 480))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.plain, False, (68, 255, 0)), (430, 520))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[1]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[6]) + '+') * 8, 520))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[1]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[6]) + '+') * 8, 520))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.desert, False, (249, 210, 39)), (430, 550))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[2]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[2]) + '+') * 8, 550))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[2]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[2]) + '+') * 8, 550))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.snow, False, (152, 249, 219)), (430, 580))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[3]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[1]) + '+') * 8, 580))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[3]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[1]) + '+') * 8, 580))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.forest, False, (11, 109, 13)), (430, 610))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[4]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[3]) + '+') * 8, 610))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[4]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[3]) + '+') * 8, 610))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.mountain, False, (123, 95, 62)), (430, 640))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[5]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[5]) + '+') * 8, 640))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[5]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[5]) + '+') * 8, 640))
            pygame.display.flip()
            pygame.time.delay(100)
            Game.Screen.blit(Game.display.arial.render(Game.Texts.volcano, False, (163, 41, 18)), (430, 670))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[6]), False,
                                          (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[4]) + '+') * 8, 670))
            Game.Screen.blit(
                Game.display.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[6]), False,
                                          (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[4]) + '+') * 8, 670))
            pygame.display.flip()
            pygame.time.delay(250)
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
            Game.button_magic.display_button()
            Game.button_inventory.display_button()
            Game.button_leave.display_button()
            Game.Screen.blit(pygame.image.load('game/assets/battle/backgrounds/stats.png'), (418, 420))
            Game.Screen.blit(
                self.arial.render("{}   {}".format(Game.Texts.attack_stat, Game.Texts.defense_stat), False,
                                  (255, 255, 255)), (530, 440))
            # base
            Game.Screen.blit(self.arial.render("Base", False, (255, 255, 255)), (430, 480))
            Game.Screen.blit(
                self.arial.render(str(Game.player.get_stats()[4] + Game.player.get_equipment()[0].get_stat()[0]), False,
                                  (255, 255, 255)),
                (585 - len(str(Game.player.get_stats()[4] + Game.player.get_equipment()[0].get_stat()[0])) * 8, 480))
            Game.Screen.blit(
                self.arial.render(str(Game.player.get_stats()[5] + Game.player.get_equipment()[1].get_stat()[0]), False,
                                  (255, 255, 255)),
                (665 - len(str(Game.player.get_stats()[5] + Game.player.get_equipment()[1].get_stat()[0])) * 8, 480))
            # plaine
            Game.Screen.blit(self.arial.render(Game.Texts.plain, False, (68, 255, 0)), (430, 520))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[1]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[6]) + '+') * 8, 520))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[1]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[6]) + '+') * 8, 520))

            # désert
            Game.Screen.blit(self.arial.render(Game.Texts.desert, False, (249, 210, 39)), (430, 550))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[2]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[2]) + '+') * 8, 550))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[2]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[2]) + '+') * 8, 550))

            # neige
            Game.Screen.blit(self.arial.render(Game.Texts.snow, False, (152, 249, 219)), (430, 580))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[3]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[1]) + '+') * 8, 580))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[3]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[1]) + '+') * 8, 580))

            # forêt
            Game.Screen.blit(self.arial.render(Game.Texts.forest, False, (11, 109, 13)), (430, 610))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[4]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[3]) + '+') * 8, 610))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[4]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[3]) + '+') * 8, 610))

            # montagne
            Game.Screen.blit(self.arial.render(Game.Texts.mountain, False, (123, 95, 62)), (430, 640))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[5]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[5]) + '+') * 8, 640))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[5]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[5]) + '+') * 8, 640))

            # volcan
            Game.Screen.blit(self.arial.render(Game.Texts.volcano, False, (163, 41, 18)), (430, 670))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[0].get_stat()[6]), False, (255, 255, 255)),
                (585 - len(str(Game.player.get_equipment()[0].get_stat()[4]) + '+') * 8, 670))
            Game.Screen.blit(
                self.arial.render('+' + str(Game.player.get_equipment()[1].get_stat()[6]), False, (255, 255, 255)),
                (665 - len(str(Game.player.get_equipment()[1].get_stat()[4]) + '+') * 8, 670))
        elif Game.fight_mode == 1:
            Game.button_attack1.display_button()
            Game.button_attack2.display_button()
            Game.button_attack3.display_button()
            Game.button_attack4.display_button()
            Game.button_back.display_button()
            Display.display_text(self, Game.Texts.description_attack.format(Game.attack_player(1, False),
                                                                            Game.attack_player(2, False),
                                                                            4 * Game.attack_player(2, False),
                                                                            Game.attack_player(3, False),
                                                                            int(0.25 * Game.attack_player(3, False)),
                                                                            Game.attack_player(4, False)),
                                 400, 415,
                                 'FRAMDCN.TTF',
                                 15, 0,
                                 (255, 255, 255), 270, False)

        elif Game.fight_mode == 2:
            Game.button_magic1.display_button()
            Game.button_magic2.display_button()
            Game.button_magic3.display_button()
            Game.button_magic4.display_button()
            Game.button_back.display_button()
            Display.display_text(self,
                                 Game.Texts.description_magic.format(
                                     Game.magic_player(1, False) - Game.player.get_stats()[0], 10, 12), 400, 415,
                                 'FRAMDCN.TTF', 15, 0, (255, 255, 255), 270, False)
        elif Game.fight_mode == 3:
            x, y, scroll = pos_inventory
            Game.Screen.blit(pygame.image.load('game/assets/inventory/set_cases_fight_0.png'), (270, 420))
            for line in range(5):
                for colone in range(5):
                    if [x, y] == [colone, line]:
                        Game.Screen.blit(pygame.image.load('game/assets/inventory/case_select.png'),
                                         (270 + x * 50, 420 + y * 50))
                    if (line + scroll) * 5 + colone < 36:
                        Game.Screen.blit(
                            pygame.image.load('game/assets/inventory/potions/{}.png'.format(
                                str(((line + scroll) * 5 + colone) % 25))),
                            (274 + colone * 50, 424 + line * 50))
                        if Game.player.get_inventory()[1][(line + scroll) * 5 + colone] == 0:
                            Game.Screen.blit(pygame.image.load('game/assets/inventory/black.png'),
                                             (270 + colone * 50, 420 + line * 50))
                    else:
                        Game.Screen.blit(pygame.image.load('game/assets/inventory/black.png'),
                                         (270 + colone * 50, 420 + line * 50))
                    if [x, y] == [colone, line]:
                        Game.Screen.blit(pygame.image.load('game/assets/inventory/case_select.png'),
                                         (270 + x * 50, 420 + y * 50))
            Game.Screen.blit(
                pygame.image.load('game/assets/inventory/potions/{}.png'.format(str(((y + scroll) * 5 + x) % 25))),
                (520, 410))
            Display.display_text(self, Game.Texts.description_object[(y + scroll) * 5 + x][0], 560, 410,
                                 'FRAMDCN.TTF',
                                 16, 0, (255, 255, 255), 120, False)
            Display.display_text(self, "{} : {}||{}".format(
                Game.Texts.quantity, Game.player.get_inventory()[1][(y + scroll) * 5 + x],
                Game.use_object((y + scroll) * 5 + x, False)), 520, 450, 'FRAMDCN.TTF', 16, 0,
                                 (255, 255, 255), 160, False)
            Game.button_back.display_button(280, 670, 'center')
            if Game.player.get_inventory()[1][(y + scroll) * 5 + x] > 0:
                Game.button_use.display_button()
                Game.use_obj = True
            else:
                Game.use_obj = False
        # zone actions
        if Game.texts == '':
            Game.texts = Game.Texts.select_action
            Game.change = True
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
                Game.texts = Game.texts.split('|')
                del Game.texts[0]
                Game.texts = '|'.join(Game.texts)
            else:
                break
        if Game.change:
            Display.display_text(self, Game.texts, 35, 415, 'rpg_.FON', 16, Game.prog, (255, 255, 255), 230, True, True)
        else:
            Display.display_text(self, Game.texts, 35, 415, 'rpg_.FON', 16, 0, (255, 255, 255), 230, True, True)
        Game.change = False
        if Game.fight_mode == 4:
            s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            Game.Screen.blit(s, (0, 0))
            Game.button_confirm.display_button()
            Game.button_back.display_button(433, 348, 'center')

    def display_text(self, texts, x_pos, y_pos, font, size, prog, color, length, change_old, point=False):
        font_ = pygame.font.Font("game/font/" + font, size)
        x, y = 0, 0
        texts = texts.split('|')
        for i in range(len(texts)):
            if point:
                font_2 = pygame.font.Font("game/font/FRAMDCN.TTF", 32)
                if prog == 0:
                    if change_old and i < len(texts) - 1:
                        Game.Screen.blit(font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                         (x_pos - 10, y_pos + y - 16))
                    else:
                        Game.Screen.blit(font_2.render('·', False, color),
                                         (x_pos - 10, y_pos + y - 16))
                else:
                    if i < len(texts) - prog:
                        Game.Screen.blit(font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                         (x_pos - 10, y_pos + y - 16))
                    else:
                        Game.Screen.blit(font_2.render('·', False, color),
                                         (x_pos - 10, y_pos + y - 16))
            texts[i] = texts[i].split(' ')
            line = ''
            for word in texts[i]:
                if prog == 0:
                    if font_.size(line + word)[0] < length or line == '':
                        line += word + ' '
                    elif font_.size(line + word)[0] >= length or word == texts[i][-1]:
                        if change_old and i < len(texts) - 1:
                            Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7,
                                                                        color[2] // 1.7)),
                                             (x_pos, y_pos + y))
                        else:
                            Game.Screen.blit(font_.render(line, False, color), (x_pos, y_pos + y))
                        line, y = word + ' ', y + size
                else:
                    if x + font_.size(word)[0] >= length:
                        x = 0
                        y += size
                    for char in word:
                        if i >= len(texts) - prog:
                            Game.Screen.blit(self.dialogue.render(char, False, color), (x_pos + x, y_pos + y))
                            pygame.display.flip()
                            time.sleep(0.05)
                            if char == '.':
                                time.sleep(0.5)
                        elif change_old:
                            Game.Screen.blit(
                                self.dialogue.render(char, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                (x_pos + x, y_pos + y))
                        x += font_.size(char)[0]
                    x += font_.size(' ')[0]
                    pass
            if change_old and i < len(texts) - 1:
                Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                 (x_pos + x, y_pos + y))

            else:
                Game.Screen.blit(font_.render(line, False, color), (x_pos + x, y_pos + y))
            x = 0
            y += size
