import pygame
import time
from armor import Armor


class Player(pygame.sprite.Sprite):
    def __init__(self, stat, inventory):
        super().__init__()
        self.mult_crit = 2
        self.frame = time.time()
        self.player = pygame.image.load('assets/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rect = self.image.get_rect()
        self.velocity = 5
        self.hp = stat[0]
        self.hp_max = stat[1]
        self.level = stat[6] * 0 + 1
        self.xp = stat[7]
        self.mp = stat[2]
        self.mp_max = stat[3]
        self.attack = stat[4]
        self.defense = stat[5]
        self.inventory = inventory
        self.inventory = [[],
                          [3, 0, 0, 0, 0,
                           1, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0],
                          []]
        self.boost_att = [1, 0, 0, 0, 0, 0, 0]
        self.boost_def = [1, 0, 0, 0, 0, 0, 0]
        self.proba_crit = 0.2
        self.mult_crtit = 2
        self.att_2 = []
        self.boost_att_2 = 0
        self.protect = 1
        self.gold = stat[8]
        self.num_armor = stat[10]
        self.num_sword = stat[9]
        self.armor = Armor.Armor(Armor.armor[self.num_armor - 1][0], Armor.armor[self.num_armor - 1][1],
                                 Armor.armor[self.num_armor - 1][2],
                                 Armor.armor[self.num_armor - 1][3],
                                 Armor.armor[self.num_armor - 1][4],
                                 Armor.armor[self.num_armor - 1][5],
                                 Armor.armor[self.num_armor - 1][6])
        self.sword = Armor.Sword(Armor.sword[self.num_sword - 1][0], Armor.sword[self.num_sword - 1][1],
                                 Armor.sword[self.num_sword - 1][2],
                                 Armor.sword[self.num_sword - 1][3],
                                 Armor.sword[self.num_sword - 1][4],
                                 Armor.sword[self.num_sword - 1][5],
                                 Armor.sword[self.num_sword - 1][6])

    def init(self):
        self.boost_att = [1, 0, 0, 0, 0, 0, 0]
        self.boost_def = [1, 0, 0, 0, 0, 0, 0]
        self.proba_crit = 0.2
        self.mult_crtit = 2
        self.att_2 = []
        self.boost_att_2 = 0
        self.protect = 1

    def get_inventory(self):
        return self.inventory

    def get_stats(self):
        return self.hp, self.hp_max, self.mp, self.mp_max, self.attack, self.defense, self.level, self.xp, self.gold, \
               self.num_sword, self.num_armor

    def change_att_2(self, damage, add=True):
        if add:
            self.att_2.append([damage, 4 + self.boost_att_2])
        else:
            self.att_2 = []

    def change_hp(self, n, use=True):
        hp = int(self.hp + n)
        if hp < 0:
            hp = 0
        elif hp > self.hp_max:
            hp = self.hp_max
        if use:
            self.hp = hp
            return "PV régénérés."
        else:
            return hp

    def change_mp(self, n, use=True):
        mp = int(self.mp + n)
        if mp > self.mp_max:
            mp = self.mp_max
        if use:
            self.mp = mp
            return "PM régénérés."
        else:
            return mp

    def get_crit(self):
        return self.proba_crit, self.mult_crtit

    def get_boost_stats(self):
        return self.boost_att, self.boost_def

    def change_boost_att(self, i, n):
        self.boost_att[i] = round(self.boost_att[i] + n, 2)
        if self.boost_att[0] < 0.7:
            self.boost_att[0] = 0.7
        elif self.boost_att[0] > 1.3:
            self.boost_att[0] = 1.3
        for i in range(1, 7):
            if self.boost_att[i] < -0.2 * self.attack + self.sword.get_stat()[0]:
                self.boost_att[i] = -int(0.2 * self.attack + self.sword.get_stat()[0])
            elif self.boost_att[i] > 0.2 * self.attack + self.sword.get_stat()[0]:
                self.boost_att[i] = int(0.2 * self.attack + self.sword.get_stat()[0])

    def change_boost_def(self, i, n):
        self.boost_def[i] = round(self.boost_def[i] + n, 2)
        if self.boost_def[0] < 0.7:
            self.boost_def[0] = 0.7
        if self.boost_def[0] > 1.3:
            self.boost_def[0] = 1.3
        for i in range(1, 7):
            if self.boost_def[i] < -0.2 * self.defense + self.armor.get_stat()[0]:
                self.boost_def[i] = -int(0.2 * self.defense + self.armor.get_stat()[0])
            elif self.boost_def[i] > 0.2 * self.defense + self.armor.get_stat()[0]:
                self.boost_def[i] = int(0.2 * self.defense + self.armor.get_stat()[0])

    def get_protect(self):
        return self.protect

    def change_protect(self, n=1):
        self.protect = n

    #  apres c du kk
    def change_proba_crit(self, n):
        if n:
            self.proba_crit += 0.05
            if self.proba_crit > 0.3:
                self.proba_crit = 0.3
        else:
            self.proba_crit = 0.2

    def change_mult_crit(self, n):
        if n:
            self.mult_crit += 0.1
            if self.mult_crit > 2.5:
                self.mult_crit = 2.5
        else:
            self.mult_crit = 2

    #  fin du kk

    def turn_att_2(self):
        length = len(self.att_2)
        if length != 0:
            for i in range(len(self.att_2)):
                self.att_2[i][1] -= 1
            if self.att_2[0][1] == 0:
                self.att_2.remove(self.att_2[0])
        if length == 0 or length == len(self.att_2):
            return 2
        elif len(self.att_2) != 0:
            return 1
        else:
            return 0

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def get_equipment(self):
        return self.sword, self.armor

    def move(self, move=True):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.1
            if self.direction == 'down':
                if move:
                    self.box_change(-1)
                else:
                    self.box = 0
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'left':
                if move:
                    self.box_change(3)
                else:
                    self.box = 4
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'up':
                if move:
                    self.box_change(7)
                else:
                    self.box = 8
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'right':
                if move:
                    self.box_change(11)
                else:
                    self.box = 12
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)

    def player_move(self, pressed, x, y, map_collision, width, length, settings):
        if (pressed.get(settings[1]) or pressed.get(settings[5])) and (x + 63) // 64 > 0 and self.collision(
                map_collision, 0, x, y):
            x -= self.velocity
            self.direction = "left"
            self.move()
        elif (pressed.get(settings[0]) or pressed.get(settings[4])) and x // 64 < length - 1 and self.collision(
                map_collision, 1, x, y):
            x += self.velocity
            self.direction = "right"
            self.move()
        elif (pressed.get(settings[3]) or pressed.get(settings[7])) and (y + 63) // 64 > 0 and self.collision(
                map_collision, 2, x, y):
            y -= self.velocity
            self.direction = "up"
            self.move()
        elif (pressed.get(settings[2]) or pressed.get(settings[6])) and y // 64 < width - 1 and self.collision(
                map_collision, 3, x, y):
            y += self.velocity
            self.direction = "down"
            self.move()
        else:
            self.move(False)
        return x, y

    def collision(self, map_collision, d, x, y):
        if d == 0:
            x1 = x - self.velocity
            if 12 >= x1 % 64 or x1 % 64 >= 32:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_collision[8][7][2] or map_collision[8][8][0]:
                            return False
                    else:
                        if map_collision[8][7][2] or map_collision[8][8][2] or map_collision[8][8][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_collision[8][9][2] or map_collision[8][8][0]:
                            return False
                    else:
                        if map_collision[8][9][2] or map_collision[8][8][2] or map_collision[8][8][0]:
                            return False
                else:
                    if map_collision[8][8][0] or map_collision[8][8][2]:
                        return False

            if 32 <= x1 % 64 <= 44:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_collision[7][7][3] or map_collision[7][8][1]:
                            return False
                    else:
                        if map_collision[7][7][3] or map_collision[7][8][3] or map_collision[7][8][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_collision[7][9][3] or map_collision[7][8][1]:
                            return False
                    else:
                        if map_collision[7][9][3] or map_collision[7][8][3] or map_collision[7][8][1]:
                            return False
                else:
                    if map_collision[7][8][1] or map_collision[7][8][3]:
                        return False
        elif d == 1:
            x1 = x + self.velocity
            if 32 >= x1 % 64 or x1 % 64 >= 52:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_collision[8][7][3] or map_collision[8][8][1]:
                            return False
                    else:
                        if map_collision[8][7][3] or map_collision[8][8][3] or map_collision[8][8][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_collision[8][9][3] or map_collision[8][8][1]:
                            return False
                    else:
                        if map_collision[8][9][3] or map_collision[8][8][3] or map_collision[8][8][1]:
                            return False
                else:
                    if map_collision[8][8][1] or map_collision[8][8][3]:
                        return False

            if 32 >= x1 % 64 >= 20:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_collision[9][7][2] or map_collision[9][8][0]:
                            return False
                    else:
                        if map_collision[9][7][2] or map_collision[9][8][2] or map_collision[9][8][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_collision[9][9][2] or map_collision[9][8][0]:
                            return False
                    else:
                        if map_collision[9][9][2] or map_collision[9][8][2] or map_collision[9][8][0]:
                            return False
                else:
                    if map_collision[9][8][0] or map_collision[9][8][2]:
                        return False
        elif d == 2:
            y1 = y - self.velocity
            if 32 <= y1 % 64 <= 52:
                if 32 <= x % 64 <= 44:
                    if map_collision[7][7][3] or map_collision[8][7][2]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_collision[8][7][2]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_collision[8][7][2] or map_collision[8][7][3]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_collision[8][7][3]:
                        return False
                else:
                    if map_collision[8][7][3] or map_collision[9][7][2]:
                        return False
            if 32 <= y1 % 64 or y1 % 64 <= 20:
                if 32 <= x % 64 <= 44:
                    if map_collision[7][8][1] or map_collision[8][8][0]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_collision[8][8][0]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_collision[8][8][0] or map_collision[8][8][1]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_collision[8][8][1]:
                        return False
                else:
                    if map_collision[8][8][1] or map_collision[9][8][0]:
                        return False
        elif d == 3:
            y1 = y + self.velocity
            if 12 <= y1 % 64 <= 32:
                if 32 <= x % 64 <= 44:
                    if map_collision[7][9][1] or map_collision[8][9][0]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_collision[8][9][0]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_collision[8][9][0] or map_collision[8][9][1]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_collision[8][9][1]:
                        return False
                else:
                    if map_collision[8][9][1] or map_collision[9][9][0]:
                        return False
            if 32 > y1 % 64 or y1 % 64 >= 44:
                if 32 <= x % 64 <= 44:
                    if map_collision[7][8][3] or map_collision[8][8][2]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_collision[8][8][2]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_collision[8][8][2] or map_collision[8][8][3]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_collision[8][8][3]:
                        return False
                else:
                    if map_collision[8][8][3] or map_collision[9][8][2]:
                        return False
        return True


'''
5 hp
10, 20, 50, 100, tout

1 hp_max
50, max:2×

5 mp
5, 10, 15, 25, tout

1 mp max
15, max:2×

1 att+def
+0.08 max:0.3

12 stat spé + 1 att + 1 def + 1 total
+0.15, +0.04, +0.04, +0.03 max:stat_spé+0.2(*att_base)

2 crit
proba 0.2 +0.05 max:0.3
mult 2 +0.1 max:2.5

1 def + 1 att + 1 total  enemy
-0.1, -0.1, -0.7 min:base*0.7

2 crit   enemy
proba 0.2 -0.03 min:base-0.09
mult 2 -0.1 min:1.6

boost_att_2
+1 tour, max:1

10_hp               20_hp               50_hp               100_hp                  all_hp
5_mp                10_mp               15_mp               25_mp                   all_mp
0.15_att_plain      0.15_def_plain      0.15_att_desert     0.15_def_desert         0.15_att_snow
0.15_def_snow       0.15_att_forest     0.15_def_forest     0.15_att_mountain       0.15_def_mountain
0.15_att_volcano    0.15_def_volcano    0.04_att_spe        0.04_def_spe            0.03_stat_spe
0.08_att_def        50_hp_max           15_mp_max           0.05_crit_proba_player  0.1_crit_mult_player
_0.1_att_enemy      _0.1_def_enemy      _0.7_stat_enemy     _0.03_crit_proba_enemy  _0.1_crit_mult_enemy
1_turn_att_2
'''
