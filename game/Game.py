import asyncio
import random
import time

from game.Display import Display
from game.Enemy import Enemy
from game.Player import Player
from operator import itemgetter
from game.Object import Object
from game.Chest import Chest
from game.Variable import *


class Game:
    def __init__(self, nb_save, Screen, size_window):
        self.Screen = Screen
        self.block2 = block2
        self.block = block
        self.Chest = [Chest(self, 0, 0, 5)]
        self.nb_save = nb_save
        self._ = import_save(nb_save)
        self.nb_map = 0
        self.check = True
        self.display_inventory = False
        self.Map_t, self.map_object_t, self.Length_t, self.Width_t = import_map()
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
        self.Texts, self.button_exit, self.button_save, self.button_pause, self.button_setting = import_language()
        self.button_shop = Button.Button((0, 0, 0), None, [615, 734, 32, 32], None, None, 0,
                                         pygame.image.load('game/assets/icons/shop.png'))
        self.button_menu = Button.Button((0, 0, 0), None, [660, 732, 32, 32], None, None, 0,
                                         pygame.image.load('game/assets/icons/menu.png'))
        self.Map, self.map_object, self.Length, self.Width = [], [], 0, 0
        self.display = Display(size_window, self)
        self.frame = 0
        self.entities = []
        for x in range(len(self.map_object_t[self.nb_map])):
            for y in range(len(self.map_object_t[self.nb_map][0])):
                a = self.map_object_t[self.nb_map][x][y]
                if a in self.block2:
                    a = block2[a]
                    self.entities.append((x * 64, y * 64, Object(self, x * 64 + a[1], y * 64 + a[2], a[0], a[3], a[4])))
        self.fight_mode = 0
        self.enemy_map = []
        for i in range(1):
            tag = 'player'
            self.enemy_map.append(Enemy(self, 3060, 2236, tag, mob[tag]))
            self.entities.append((self.enemy_map[i].x, self.enemy_map[i].y, self.enemy_map[i]))
        self.entities.append((self.x, self.y, self.player))
        self.change = True
        self.debut_combat = True
        self.texts = ''
        self.pos_inventory = (0, 0, 0)
        self.use_obj = False
        self.prog = 1
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
        self.x_32, self.y_32 = 0, 0
        self.refresh_entities = True

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
            self.x, self.y = self.x_t[self.nb_map], self.y_t[self.nb_map]
            self.map_chunk = self.Map_chunk[self.nb_map]
            self.instance = False
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
                if self.pressed2.get(pygame.K_a):
                    self.display_inventory = not self.display_inventory
                self.entities.remove((self.x, self.y, self.player))
                self.player.player_move()
                self.entities.append((self.x, self.y, self.player))
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
                if (self.x // 64 != self.x_y_generation[0] or self.y // 64 != self.x_y_generation[1]) and \
                        self.area == 'plain':
                    self.x_y_generation = (self.x // 64, self.y // 64)
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
        self.refresh_entities = False

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
