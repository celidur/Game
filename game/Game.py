import asyncio
import random
import time
from game.Variable import *
from game.Display import Display
from game.Enemy import Enemy
from game.Ennemy2 import Ennemy2
from game.Player import Player
from operator import itemgetter
from game.Object import Object
from game.Chest import Chest


class Game:
    def __init__(self, nb_save, Screen, size_window):
        self.Screen = Screen
        self.block2 = block2
        self.block = block
        self.Chest = [Chest(self,0,0,5)]
        self.nb_save = nb_save
        self._ = import_save(nb_save)
        self.nb_map = 0
        self.check = True
        self.Map_t, self.map_object_t, self.map_collision_t, self.Length_t, self.Width_t = import_map()
        if self._:
            self.x_t, self.y_t, self.menu, self.temp = self._[3], self._[4], 0, time.time()
            self.Settings = self._[2]
            self.area = self._[5]
            while len(self.x_t) < len(self.Map_t):
                self.x_t.append(0)
            while len(self.y_t) < len(self.Map_t):
                self.y_t.append(0)
            self.x_t[1] = 47 * 64
            self.y_t[1] = 47 * 64
            self.x, self.y = self.x_t[self.nb_map], self.y_t[self.nb_map]
            self.player = Player(self._[0], self._[1], self)
            self.x_y_generation = (self.x_t[self.nb_map] % 64, self.y_t[self.nb_map] % 64)
        else:
            self.check = False
        self.volume = 0.2
        self.fade = [False, self.volume, 0, 0]  # fade, volume, début, durée
        self.Texts, self.button_exit, self.button_magic, self.button_leave, self.button_inventory, self.button_attack, \
            self.button_save, self.button_pause, self.button_setting, self.button_attack1, self.button_attack2, \
            self.button_attack4, self.button_attack3, self.button_back, self.button_magic1, self.button_magic2, \
            self.button_magic3, self.button_magic4, self.button_confirm, self.button_use, self.enemy = import_language()
        self.button_shop = Button.Button((0, 0, 0), None, [615, 734, 32, 32], None, None, 0,
                                         pygame.image.load('game/assets/icons/shop.png'))
        self.button_menu = Button.Button((0, 0, 0), None, [660, 732, 32, 32], None, None, 0,
                                         pygame.image.load('game/assets/icons/menu.png'))
        self.Map, self.map_object, self.map_collision, self.Length, self.Width = [], [], [], 0, 0
        self.display = Display(size_window, self)
        self.frame = 0
        self.entities = []
        for x in range(len(self.map_object_t[self.nb_map])):
            for y in range(len(self.map_object_t[self.nb_map][0])):
                a = self.map_object_t[self.nb_map][x][y]
                if a in self.block2:
                    a = block2[a]
                    self.entities.append((x * 64, y * 64, Object(self, x * 64 + a[1], y * 64 + a[2], a[0])))
        self.fight_mode = 0
        self.enemy_map = []
        for i in range(1):
            self.enemy_map.append(Ennemy2(self, 3060, 2236, 'deer', mob['deer']))
            self.entities.append((self.enemy_map[i].x, self.enemy_map[i].y, self.enemy_map[i]))
        self.enemy_ = Enemy(self.enemy[0])
        self.change = True
        self.debut_combat = True
        self.texts = ''
        self.pos_inventory = (0, 0, 0)
        self.use_obj = False
        self.prog = 1
        self.nb_case = 0
        self.end_ = True
        self.nb_chest = 0
        self.instance = True
        self.game_chunk = []
        self.list_coord = []
        self.Map_chunk = []
        self.map_chunk = []
        self.pressed2 = {}
        self.time_temp = time.time()
        self.onclick, self.running, self.pressed, self.pos = False, True, {}, [0, 0]
        self.ready = False
        self.loading_text = "Creating a flat Earth"
        self.loading_pos = [(0, -40), (-20, -35), (-35, -20), (-40, 0), (-35, 20), (-20, 35), (0, 40), (20, 35),
                            (35, 20), (40, 0), (35, -20), (20, -35)]
        self.font_ = pygame.font.Font("game/font/FRAMDCN.TTF", 16)
        self.progress = 0
        self.near_player = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        self.x_32, self.y_32 = 0, 0
        self.refresh_entities = True

    def check_save(self):
        return self.check

    def fadeout(self):
        if self.fade[0]:
            vol = self.fade[1] - ((time.time() - self.fade[2]) / self.fade[3]) * self.fade[1]
            if vol <= 0:
                self.fade = [False, self.volume, 0, 0]
                pygame.mixer_music.stop()
                pygame.mixer_music.set_volume(self.volume)
                if self.fight_mode != 0:
                    pygame.mixer_music.load(music['combat'])
                    pygame.mixer_music.play(loops=-1)
                else:
                    pygame.mixer_music.load(music[self.area])
                    pygame.mixer_music.play(loops=-1)
            else:
                pygame.mixer_music.set_volume(vol)

    def refresh_near_player(self):
        n_p = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        x_p, y_p = ((self.x + 32) // 32) * 32 - 16, ((self.y + 32) // 32) * 32 - 16
        n_p[0].append((x_p, y_p))
        for i in range(12):
            for case in n_p[i]:
                for a in [-32, 0, 32]:
                    for b in [-32, 0, 32]:
                        if (a, b) == (0, 0):
                            continue
                        new_case = (case[0] + a, case[1] + b)
                        placed = False
                        if new_case in n_p[i - 1] or new_case in n_p[i] or new_case in n_p[i + 1]:
                            placed = True
                        if placed:
                            continue

                        if ((new_case[1] + 32) % 64) // 32 == 0:
                            n = 0
                        else:
                            n = 2
                        if ((new_case[0] + 32) % 64) // 32 == 0:
                            pass
                        else:
                            n += 1
                        if not self.map_collision[(new_case[0] + 32) // 64][(new_case[1] + 32) // 64][n]:
                            n_p[i + 1].append(new_case)
        return n_p

    def loading(self):
        while not self.ready:
            v = import_temp()
            if v:
                self.list_coord = v
                asyncio.run(self.prepare_map(False))
            else:
                asyncio.run(self.prepare_map(True))

    def get_pressed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.menu != 5:
                    self.running = False
                    return False
            elif event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True
                self.pressed2[event.key] = True
            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.onclick = True
                self.pos = pygame.mouse.get_pos()

    def running_game(self):
        self.fadeout()
        # x, y = (3280//64)*64 - 200, (2000//64)*64 - 200
        if self.instance:
            self.Map, self.map_object, self.Length, self.Width = self.Map_t[self.nb_map], \
                                                                 self.map_object_t[self.nb_map], \
                                                                 self.Length_t[self.nb_map], \
                                                                 self.Width_t[self.nb_map]
            self.map_collision = self.map_collision_t[self.nb_map]
            self.x, self.y = self.x_t[self.nb_map], self.y_t[self.nb_map]
            self.map_chunk = self.Map_chunk[self.nb_map]
            self.instance = False
        x_32_, y_32_ = self.x // 32, self.y // 32
        if (self.x_32, self.y_32) != (x_32_, y_32_):
            self.x_32, self.y_32 = x_32_, y_32_
            self.near_player = self.refresh_near_player()
        if self.pressed2.get(pygame.K_KP_PLUS):
            self.pressed2[pygame.K_KP_PLUS], self.instance = False, True
            self.nb_map = (self.nb_map + 1) % len(self.map_object_t)
            return
        if self.menu == 0 or self.menu == 1:
            for enemy__ in self.enemy_map:
                self.entities.remove((enemy__.x, enemy__.y, enemy__))
                enemy__.enemy_move()
                self.entities.append((enemy__.x, enemy__.y, enemy__))
                self.refresh_entities = True
            for projectile in self.player.all_projectiles:
                projectile.mov()
        if self.menu == 0:
            if self.onclick:
                if self.button_menu.button_clicked(self.pos[0], self.pos[1]):
                    self.menu = 2
                elif self.button_shop.button_clicked(self.pos[0], self.pos[1]) and self.area == 'village':
                    pass
                # ajouter test bouton iventaire
            else:
                self.frame = time.time()
                if self.pressed2.get(pygame.K_ESCAPE):
                    self.menu = 2
                if self.pressed2.get(pygame.K_SPACE):
                    self.player.launch_projectile()
                if self.pressed2.get(pygame.K_e):
                    self.menu = 1
                self.player.player_move()
                self.x_t[self.nb_map], self.y_t[self.nb_map] = self.x, self.y
                if self.y // 64 == 31 and 45 <= self.x // 64 <= 50:
                    if self.area != 'plain':
                        if not self.fade[0]:
                            self.fade = [True, self.volume, time.time(), 1]
                        self.area = 'plain'
                elif self.y // 64 == 30 and 45 <= self.x // 64 <= 50:
                    if self.area != 'village':
                        if not self.fade[0]:
                            self.fade = [True, self.volume, time.time(), 1]
                        self.area = 'village'
                        self.nb_case = 0
                if (self.x // 64 != self.x_y_generation[0] or self.y // 64 != self.x_y_generation[1]) and \
                        self.area == 'plain':
                    self.nb_case += 1
                    self.x_y_generation = (self.x // 64, self.y // 64)
                    if random.random() == self.nb_case * (2 + self.player.level / 100) / 5000:  # <=
                        self.menu = 4
                        self.nb_case = 0
                        self.debut_combat = True
                        self.fight_mode = -2
        elif self.menu == 1:
            if self.pressed2.get(pygame.K_ESCAPE):
                self.menu = 0
        elif self.menu == 2:  # mode pause
            if self.onclick:
                if self.button_pause.button_clicked(self.pos[0], self.pos[1]):
                    self.menu = 0
                elif self.button_exit.button_clicked(self.pos[0], self.pos[1]):
                    self.running = False
                    return
                elif self.button_save.button_clicked(self.pos[0], self.pos[1]):
                    self.save()
                elif self.button_setting.button_clicked(self.pos[0], self.pos[1]):
                    pass
            else:
                if self.pressed2.get(pygame.K_ESCAPE):
                    self.menu = 0
        elif self.menu == 3:  # menu shop
            pass
        elif self.menu == 4:
            self.end_ = True
            if self.onclick:
                if self.fight_mode == 0:
                    if self.button_attack.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 1
                        self.add_text(self.Texts.select_attack)
                        self.prog = 1
                    elif self.button_magic.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 2
                        self.add_text(self.Texts.select_spell)
                        self.prog = 1
                    elif self.button_inventory.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 3
                        self.add_text(self.Texts.select_object)
                        self.prog = 1
                        self.pos_inventory = (0, 0, 0)
                    elif self.button_leave.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 4
                elif self.fight_mode == 1 or self.fight_mode == 2:
                    if self.button_back.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 0
                        self.remove_text()
                    elif self.fight_mode == 1:
                        if self.button_attack1.button_clicked(self.pos[0], self.pos[1]):
                            self.attack_player(1)
                            self.end_turn()
                        elif self.button_attack2.button_clicked(self.pos[0], self.pos[1]):
                            self.attack_player(2)
                            self.end_turn()
                        elif self.button_attack3.button_clicked(self.pos[0], self.pos[1]):
                            self.attack_player(3)
                            self.end_turn()
                        elif self.button_attack4.button_clicked(self.pos[0], self.pos[1]):
                            self.attack_player(4)
                            self.end_turn()
                    else:
                        if self.button_magic1.button_clicked(self.pos[0], self.pos[1]):
                            self.magic_player(1)
                            self.end_turn()
                        elif self.button_magic2.button_clicked(self.pos[0], self.pos[1]):
                            self.magic_player(2)
                            self.end_turn()
                        elif self.button_magic3.button_clicked(self.pos[0], self.pos[1]):
                            self.magic_player(3)
                            self.end_turn()
                        elif self.button_magic4.button_clicked(self.pos[0], self.pos[1]):
                            self.magic_player(4)
                            self.end_turn()
                elif self.fight_mode == 3:
                    if self.button_back.button_clicked(self.pos[0], self.pos[1], 280, 670):
                        self.fight_mode = 0
                        self.remove_text()
                    elif self.button_use.button_clicked(self.pos[0], self.pos[1]) and self.use_obj:
                        self.remove_text(2)
                        self.add_text(self.use_object((self.pos_inventory[1] + self.pos_inventory[2]) * 5 +
                                                      self.pos_inventory[0]), True, True)
                        self.end_turn()
                elif self.fight_mode == 4:
                    if self.button_back.button_clicked(self.pos[0], self.pos[1], 433, 348):
                        self.fight_mode = 0
                    elif self.button_confirm.button_clicked(self.pos[0], self.pos[1]):
                        self.fight_mode = 0
                        self.fade = [True, self.volume, time.time(), 1]
                        self.menu = 0
            elif self.pressed2.get(pygame.K_ESCAPE):
                if self.fight_mode != 0:
                    if self.fight_mode != 4:
                        self.remove_text()
                    self.fight_mode = 0
                else:
                    self.fight_mode = 4
            elif self.pressed2.get(pygame.K_RETURN) and self.fight_mode == 4:
                self.fight_mode = 0
                self.fade = [True, self.volume, time.time(), 1]
                self.menu = 0
            if self.debut_combat:
                self.init_fight()
                self.debut_combat = False
            self.frame = time.time()
            if self.fight_mode == 3:
                if ((self.pressed.get(self.Settings[0]) or self.pressed.get(self.Settings[4])) and
                    time.time() > self.temp + 1 / 7) or self.pressed2.get(self.Settings[0]) or \
                        self.pressed2.get(self.Settings[4]):
                    self.pos_inventory = (
                        ((self.pos_inventory[0] + 1) % 5),
                        (self.pos_inventory[1] * 5 + self.pos_inventory[0] + 1) // 5,
                        self.pos_inventory[2])
                    if self.pos_inventory[1] >= 5:
                        self.pos_inventory = (self.pos_inventory[0], 4, self.pos_inventory[2] + 1)
                    if (self.pos_inventory[1] + self.pos_inventory[2]) * 5 + self.pos_inventory[0] >= 36:
                        self.pos_inventory = (0, 0, 0)
                    self.temp = time.time()
                elif ((self.pressed.get(self.Settings[1]) or self.pressed.get(self.Settings[5])) and
                      time.time() > self.temp + 1 / 7) or self.pressed2.get(self.Settings[0]) or \
                        self.pressed2.get(self.Settings[4]):
                    self.pos_inventory = (
                        (self.pos_inventory[1] * 5 + self.pos_inventory[0] - 1) % 5,
                        (self.pos_inventory[1] * 5 + self.pos_inventory[0] - 1) // 5,
                        self.pos_inventory[2])
                    if self.pos_inventory[1] < 0:
                        self.pos_inventory = (self.pos_inventory[0], 0, self.pos_inventory[2] - 1)
                    if self.pos_inventory[2] < 0:
                        self.pos_inventory = (36 % 5 - 1, 4, 36 // 5 - 4)
                    self.temp = time.time()
                elif ((self.pressed.get(self.Settings[2]) or self.pressed.get(self.Settings[6])) and
                      time.time() > self.temp + 1 / 7) or self.pressed2.get(self.Settings[0]) or \
                        self.pressed2.get(self.Settings[4]):
                    self.pos_inventory = (self.pos_inventory[0], self.pos_inventory[1] + 1, self.pos_inventory[2])
                    if self.pos_inventory[1] >= 5:
                        self.pos_inventory = (self.pos_inventory[0], 4, self.pos_inventory[2] + 1)
                    if (self.pos_inventory[1] + self.pos_inventory[2]) * 5 + self.pos_inventory[0] >= 36:
                        self.pos_inventory = (self.pos_inventory[0], 0, 0)
                    self.temp = time.time()
                elif ((self.pressed.get(self.Settings[3]) or self.pressed.get(self.Settings[7])) and
                      time.time() > self.temp + 1 / 7) or self.pressed2.get(self.Settings[0]) or \
                        self.pressed2.get(self.Settings[4]):
                    self.pos_inventory = (self.pos_inventory[0], self.pos_inventory[1] - 1, self.pos_inventory[2])
                    if self.pos_inventory[1] < 0:
                        self.pos_inventory = (self.pos_inventory[0], 0, self.pos_inventory[2] - 1)
                    if self.pos_inventory[2] < 0:
                        if self.pos_inventory[0] >= 36 % 5:
                            self.pos_inventory = (self.pos_inventory[0], 3, 36 // 5 - 4)
                        else:
                            self.pos_inventory = (self.pos_inventory[0], 4, 36 // 5 - 4)
                    self.temp = time.time()

            pygame.display.flip()
        self.onclick, self.pressed2 = False, {}
        if self.menu != 4:
            self.fight_mode = 0
        return

    def refresh_screen(self):
        if self.refresh_entities:
            for key in [0, 1]:
                self.entities.sort(key=itemgetter(key))
        if self.menu == 0:
            self.display.display()
        elif self.menu == 1:
            self.display.display()
        elif self.menu == 2:
            self.display.display()
        elif self.menu == 3:
            pass
        elif self.menu == 4:
            self.display.display_fight()
        self.refresh_entities = False

    def add_text(self, text, c=True, add=False):
        self.texts = self.texts.split('|')
        self.texts.append(text)
        self.change = c
        self.texts = '|'.join(self.texts)
        if add:
            self.prog += 1
        if self.texts[0] == '|':
            self.texts = self.texts[1:]

    def init_fight(self):
        self.player.init()
        if self.area == 'plain':
            index = 0
        else:
            index = 0
        self.enemy_ = Enemy(self.enemy[index])
        self.texts = '{} sauvage apparaît.|{}'.format(self.enemy_.name, self.Texts.select_action)
        self.prog = 2
        self.fade = [True, self.volume, time.time(), 3]

    def save(self):
        save_game = [self.player.stats, self.player.inventory, self.Settings, self.x_t, self.y_t, self.area]
        if not os.path.exists('game/save/{}'.format(self.nb_save)):
            os.makedirs('game/save/{}'.format(self.nb_save))
        with open('game/save/{}/save_game_'.format(self.nb_save), 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(save_game)
        try:
            os.remove('game/save/{}/save_game'.format(self.nb_save))
        except FileNotFoundError:
            pass
        os.rename('game/save/{}/save_game_'.format(self.nb_save), 'game/save/{}/save_game'.format(self.nb_save))

    async def loading_animation(self, x_, y_):
        n = 0
        while not self.ready:
            self.Screen.blit(pygame.image.load("game/assets/temp/loading_background.png"), (0, 0))
            pygame.draw.rect(self.Screen, (0, 255, 0), [252, 650, int(self.progress * 200), 16])
            self.Screen.blit(self.font_.render('{} %'.format(int(self.progress * 100)), False, (255, 255, 255)),
                             (262 + int(self.progress * 200), 650))
            self.Screen.blit(self.font_.render(self.loading_text, False, (255, 255, 255)),
                             (352 - self.font_.size(self.loading_text)[0] // 2, 670))
            self.Screen.blit(self.font_.render('.' * (n // 3), False, (255, 255, 255)),
                             (352 + self.font_.size(self.loading_text)[0] // 2, 670))
            for z in range(12):
                self.Screen.blit(pygame.image.load("game/assets/icons/loading/{}.png".format((z + n) % 12)),
                                 (self.loading_pos[z][0] + x_ - 9, self.loading_pos[z][1] + y_ - 9))
            pygame.display.flip()
            n += 1
            n %= 12
            await asyncio.sleep(1 / 12)

    async def loading_map(self, a):
        for i in self.Map_t:
            map_split = []
            temp_ = []
            for lines in range((len(i) + 15) // 16):
                strip = []
                for columns in range((len(i[0]) + 15) // 16):
                    mini_map = []
                    for line in range(16):
                        mini_lines = []
                        for column in range(16):
                            if lines * 16 + line > len(i) - 1 or columns * 16 + column > len(i[0]) - 1:
                                mini_lines.append([None, None, None])
                            else:
                                mini_lines.append(i[lines * 16 + line][columns * 16 + column][:3])
                            await asyncio.sleep(0)
                        mini_map.append(mini_lines)
                    strip.append(mini_map)
                map_split.append(strip)
            for x_chunk in range(len(map_split)):
                strip = []
                for y_chunk in range(len(map_split[0])):
                    chunk = pygame.Surface((16 * 64, 16 * 64), pygame.SRCALPHA, 32)
                    for x_temp in range(16):
                        self.progress = (((y_chunk + (x_temp / 16)) / len(map_split[0])) + x_chunk) / len(map_split)
                        for y_temp in range(16):
                            for layer in range(3):
                                try:
                                    chunk.blit(self.block[map_split[x_chunk][y_chunk][x_temp][y_temp][layer]],
                                               (x_temp * 64, y_temp * 64))
                                except KeyError:
                                    continue
                            await asyncio.sleep(0)
                    strip.append(chunk)
                temp_.append(strip)
            self.Map_chunk.append(temp_)
        if a:
            self.loading_text = "Shuffling random numbers"
            self.progress = 0
            for i_1 in range(4 * 1024):
                for j2 in range(1024):
                    self.list_coord.append((i_1 // 1024, i_1 % 1024, j2))
                await asyncio.sleep(0)
            for i_1 in reversed(range(1, len(self.list_coord))):
                j2 = int(random.random() * (i_1 + 1))
                self.list_coord[i_1], self.list_coord[j2] = self.list_coord[j2], self.list_coord[i_1]
                if i_1 % 1024 == 0:
                    self.progress = 1 - i_1 / (4 * 1024 * 1024)
                    await asyncio.sleep(0)
            self.progress = 1
            try:
                os.remove("game/file/temp")
            except FileNotFoundError:
                pass
            await asyncio.sleep(0)
            with open("game/file/temp", 'wb') as file:
                pickler = pickle.Pickler(file)
                pickler.dump(self.list_coord)
        await asyncio.sleep(0.5)
        self.ready = True
        pygame.mixer_music.load(music[self.area])
        pygame.mixer_music.set_volume(self.volume)
        pygame.mixer_music.play(loops=-1)

    async def prepare_map(self, a):
        t1 = asyncio.create_task(self.loading_animation(352, 580))
        t2 = asyncio.create_task(self.loading_map(a))
        await asyncio.gather(t1, t2)

    def remove_text(self, n=1):
        for i in range(n):
            self.texts = self.texts.split('|')
            del self.texts[-1]
            self.texts = '|'.join(self.texts)

    def attack_player(self, n, use=True):
        env = 6
        if self.enemy_.environment == self.Texts.plain:
            env = 1
        elif self.enemy_.environment == self.Texts.desert:
            env = 2
        elif self.enemy_.environment == self.Texts.snow:
            env = 3
        elif self.enemy_.environment == self.Texts.forest:
            env = 4
        elif self.enemy_.environment == self.Texts.mountain:
            env = 5

        if random.random() != self.player.get_crit()[0] and use:  # <
            crit = self.player.get_crit()[1]
        else:
            crit = 1
        damage = 0
        if n == 1:
            damage = 7 * crit * (self.player.attack + self.player.get_equipment()[0].get_stat()[0] +
                                 self.player.get_equipment()[0].get_stat()[env]) / self.enemy_.get_defense()
        elif n == 2:
            damage = 2 * crit * (self.player.attack + self.player.get_equipment()[0].get_stat()[0] +
                                 self.player.get_equipment()[0].get_stat()[env]) / self.enemy_.get_defense()
        elif n == 3:
            damage = 12 * crit * (self.player.attack + self.player.get_equipment()[0].get_stat()[0] +
                                  self.player.get_equipment()[0].get_stat()[env]) / self.enemy_.get_defense()
        elif n == 4:
            damage = 7 * crit * ((self.player.attack + self.player.get_equipment()[0].get_stat()[0]) / 2 +
                                 self.player.get_equipment()[0].get_stat()[env] * 5) / self.enemy_.get_defense()
        if use:
            self.remove_text()
            self.fight_mode = 0
            if n == 1:
                self.remove_text()
                if crit != 1:
                    self.add_text("Coup critique !", True, True)
                self.enemy_.change_hp(-int(damage))
                self.add_text(
                    "Vous frappez {} de votre épée et lui infligez {} dégats.".format(self.enemy_.name(),
                                                                                      int(damage)), True, True)
            elif n == 2:
                self.remove_text()
                if crit != 1:
                    self.add_text("Coup critique !", True, True)
                self.player.change_att_2(int(damage))
                self.add_text("Vous avez blessé {}. Il saigne.".format(self.enemy_.name()), True, True)
            elif n == 3:
                self.remove_text()
                if crit != 1:
                    self.add_text("Coup critique !", True, True)
                self.enemy_.change_hp(-int(damage))
                self.player.change_hp(-int(0.25 * damage / crit))
                self.add_text("Vous chargez {} et lui infligez {} dégats.".format(self.enemy_.name,
                                                                                  int(damage)), True, True)
                self.add_text("Vous avez également été blessé par le choc. Vous subissez {} dégats.".format(
                    int(0.25 * damage / crit)), True, True)
            elif n == 4:
                if self.player.mp < 10:
                    self.end_ = False
                    self.add_text("Mana insuffisant." + ' ' + "Sélectionnez un autre sort ou une autre action.")
                    self.fight_mode = 1
                else:
                    self.remove_text()
                    if crit != 1:
                        self.add_text("Coup critique !", True, True)
                    self.enemy_.change_hp(-int(damage))
                    self.add_text("Vous mobilisez votre attaque spéciale pour infliger {} dégats à {}.".format(
                        int(damage), self.enemy_.name), True, True)
        else:
            return int(damage)

    def magic_player(self, n, use=True):
        if use:
            self.remove_text()
            self.fight_mode = 0
        if n == 1:
            heal = self.player.change_hp(0.2 * self.player.hp_max, False)
            if use:
                if self.player.mp < 10:
                    self.end_ = False
                    self.add_text("Mana insuffisant." + ' ' + "Sélectionnez autre action.")
                    self.fight_mode = 2
                elif self.player.hp == self.player.hp_max:
                    self.end_ = False
                    self.add_text("Vous avez déjà tous vos PV." + ' ' + "Sélectionnez une autre action.")
                else:
                    self.remove_text()
                    self.player.change_mp(-10)
                    self.player.change_hp(0.2 * self.player.hp_max)
                    if self.player.hp == self.player.hp_max:
                        self.add_text("PV entièrement régénérés.", True, True)
                    else:
                        self.add_text("{} PV régénérés.".format(heal - self.player.hp), True, True)

            else:
                return heal
        elif n == 2:
            if self.player.mp < 10:
                self.end_ = False
                self.add_text("Mana insuffisant." + ' ' + "Sélectionnez une autre action.")
                self.fight_mode = 2
            else:
                self.player.change_mp(-10)
                self.player.change_protect(1.5)
                self.add_text(
                    "Vous formez un bouclier magique de force {} autour de vous pour vous protéger.".format(1.5),
                    True, True)
        elif n == 3:
            if self.player.mp < 10:
                self.end_ = False
                self.add_text("Mana insuffisant." + ' ' + "Sélectionnez une autre action.")
                self.fight_mode = 2
            else:
                self.player.change_boost_def(0, 0.15)
                self.add_text(
                    'Votre défense de base est désormais multipliée par {}.'.format(
                        self.player.get_boost_stats()[1][0]), True, True)
                if self.player.get_boost_stats()[1][0] == 1.3:
                    self.add_text('Votre défense de base est boostée à son maximum. (×1.3)', True, True)
        elif n == 4:
            if self.player.mp < 10:
                self.end_ = False
                self.add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' +
                              "Sélectionnez une autre action.")
                self.fight_mode = 2
            else:
                self.player.change_boost_att(0, 0.15)
                self.add_text(
                    'Votre attaque de base est désormais multipliée par {}.'.format(
                        self.player.get_boost_stats()[0][0]), True, True)
                if self.player.get_boost_stats()[0][0] == 1.3:
                    self.add_text('Votre attaque de base est boostée à son maximum. (×1.3)', True, True)

    def end_turn(self):
        if not self.end_:
            return None
        if self.player.att_2:
            damage = 0
            for __ in range(len(self.player.att_2)):
                damage += self.player.att_2[__][0]
            self.enemy_.change_hp(-int(damage))
            self.add_text("L'ennemi souffre. Il subit {} dégats.".format(damage), True, True)
        n = self.player.turn_att_2()
        if n == 0:
            self.add_text("l'ennemi ne souffre plus.", True, True)
        elif n == 1:
            self.add_text("L'ennemi souffre de moins en moins.", True, True)
        self.player.change_protect()
        v = self.enemy_.chose_attack_enemy()
        if v == 0:
            hp = self.enemy_.hp
            self.enemy_.attack_enemy(v)
            self.add_text("L'ennemi se soigne et récupère {} PV.".format(self.enemy_.hp - hp), True, True)
        self.add_text(self.Texts.select_action)

    def use_object(self, index_object, use=True):
        if use:
            self.fight_mode = 0
            self.player.inventory[1][index_object] -= 1
        if index_object == 0:
            return self.Texts.description_object[index_object][1].format(self.player.change_hp(10, use))
        elif index_object == 1:
            return self.Texts.description_object[index_object][1].format(self.player.change_hp(20, use))
        elif index_object == 2:
            return self.Texts.description_object[index_object][1].format(self.player.change_hp(50, use))
        elif index_object == 3:
            return self.Texts.description_object[index_object][1].format(self.player.change_hp(100, use))
        elif index_object == 4:
            return self.Texts.description_object[index_object][1].format(self.player.change_hp(self.player.hp_max, use))
        elif index_object == 5:
            return self.Texts.description_object[index_object][1].format(self.player.change_mp(10, use))
        elif index_object == 6:
            return self.Texts.description_object[index_object][1].format(self.player.change_mp(20, use))
        elif index_object == 7:
            return self.Texts.description_object[index_object][1].format(self.player.change_mp(50, use))
        elif index_object == 8:
            return self.Texts.description_object[index_object][1].format(self.player.change_mp(100, use))
        elif index_object == 9:
            return self.Texts.description_object[index_object][1].format(self.player.change_mp(self.player.mp_max, use))
        elif index_object == 10:  #
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 11:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 12:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 13:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 14:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 15:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 16:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 17:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 18:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 19:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 20:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 21:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 22:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 23:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 24:
            return self.Texts.description_object[index_object][1].format(0, 0)
        elif index_object == 25:
            return self.Texts.description_object[index_object][1]
        elif index_object == 26:
            return self.Texts.description_object[index_object][1]
        elif index_object == 27:
            return self.Texts.description_object[index_object][1]
        elif index_object == 28:
            return self.Texts.description_object[index_object][1]
        elif index_object == 29:
            return self.Texts.description_object[index_object][1]
        elif index_object == 30:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 31:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 32:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 33:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 34:
            return self.Texts.description_object[index_object][1].format(0)
        elif index_object == 35:
            return self.Texts.description_object[index_object][1].format(0)
