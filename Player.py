import pygame
import time
from armor import Armor


class Player(pygame.sprite.Sprite):
    def __init__(self, stat, inventory):
        super().__init__()
        self.frame = time.time()
        self.player = pygame.image.load('assets/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rect = self.image.get_rect()
        self.velocity = 8
        self.hp = stat[0]
        self.hp_max = stat[1]
        self.level = stat[6]
        self.xp = stat[7]
        self.hm = stat[2]
        self.hm_max = stat[3]
        self.attack = stat[4]
        self.defense = stat[5]
        self.inventory = inventory
        self.boost_att = 1
        self.boost_def = 1
        self.gold = stat[8]
        self.num_armor = 1
        self.num_sword = 1
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

    def get_inventory(self):
        return self.inventory

    def get_boost(self):
        return self.boost_att, self.boost_def

    def change_boost_att(self, n):
        if n:
            self.boost_att += 0.15
            # équipement
        else:
            self.boost_att = 1

    def change_boost_def(self, n):
        if n:
            self.boost_def += 0.15
            # équipement
        else:
            self.boost_def = 1

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def get_equipment(self):
        return self.sword, self.armor

    def move(self, direction):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.1
            if direction == "same":
                direction = self.direction
                self.box = -2
            if direction == 'down':
                self.box_change(-1)
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif direction == 'left':
                self.box_change(3)
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif direction == 'up':
                self.box_change(7)
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif direction == 'right':
                self.box_change(11)
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            self.direction = direction

    def player_move(self, pressed, x, y, map_game, width, length, Settings):
        if pressed.get(Settings[1]) and (x + 63) // 64 > 0 and self.collision(map_game, 0, x, y):
            x -= self.velocity
            self.move("left")
        elif pressed.get(Settings[0]) and x // 64 < length - 1 and self.collision(map_game, 1, x, y):
            x += self.velocity
            self.move("right")
        elif pressed.get(Settings[3]) and (y + 63) // 64 > 0 and self.collision(map_game, 2, x, y):
            y -= self.velocity
            self.move("up")
        elif pressed.get(Settings[2]) and y // 64 < width - 1 and self.collision(map_game, 3, x, y):
            y += self.velocity
            self.move("down")
        else:
            self.move("same")
        return x, y

    def collision(self, map_game, d, x, y):
        if d == 0:
            x1 = x - self.velocity
            if 12 >= x1 % 64 or x1 % 64 >= 32:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[8][7][3][2] or map_game[8][8][3][0]:
                            return False
                    else:
                        if map_game[8][7][3][2] or map_game[8][8][3][2] or map_game[8][8][3][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[8][9][3][2] or map_game[8][8][3][0]:
                            return False
                    else:
                        if map_game[8][9][3][2] or map_game[8][8][3][2] or map_game[8][8][3][0]:
                            return False
                else:
                    if map_game[8][8][3][0] or map_game[8][8][3][2]:
                        return False

            if 32 <= x1 % 64 <= 44:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[7][7][3][3] or map_game[7][8][3][1]:
                            return False
                    else:
                        if map_game[7][7][3][3] or map_game[7][8][3][3] or map_game[7][8][3][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[7][9][3][3] or map_game[7][8][3][1]:
                            return False
                    else:
                        if map_game[7][9][3][3] or map_game[7][8][3][3] or map_game[7][8][3][1]:
                            return False
                else:
                    if map_game[7][8][3][1] or map_game[7][8][3][3]:
                        return False
        elif d == 1:
            x1 = x + self.velocity
            if 32 >= x1 % 64 or x1 % 64 >= 52:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[8][7][3][3] or map_game[8][8][3][1]:
                            return False
                    else:
                        if map_game[8][7][3][3] or map_game[8][8][3][3] or map_game[8][8][3][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[8][9][3][3] or map_game[8][8][3][1]:
                            return False
                    else:
                        if map_game[8][9][3][3] or map_game[8][8][3][3] or map_game[8][8][3][1]:
                            return False
                else:
                    if map_game[8][8][3][1] or map_game[8][8][3][3]:
                        return False

            if 32 >= x1 % 64 >= 20:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[9][7][3][2] or map_game[9][8][3][0]:
                            return False
                    else:
                        if map_game[9][7][3][2] or map_game[9][8][3][2] or map_game[9][8][3][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[9][9][3][2] or map_game[9][8][3][0]:
                            return False
                    else:
                        if map_game[9][9][3][2] or map_game[9][8][3][2] or map_game[9][8][3][0]:
                            return False
                else:
                    if map_game[9][8][3][0] or map_game[9][8][3][2]:
                        return False
        elif d == 2:
            y1 = y - self.velocity
            if 32 <= y1 % 64 <= 52:
                if 32 <= x % 64 <= 44:
                    if map_game[7][7][3][3] or map_game[8][7][3][2]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_game[8][7][3][2]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_game[8][7][3][2] or map_game[8][7][3][3]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_game[8][7][3][3]:
                        return False
                else:
                    if map_game[8][7][3][3] or map_game[9][7][3][2]:
                        return False
            if 32 <= y1 % 64 or y1 % 64 <= 20:
                if 32 <= x % 64 <= 44:
                    if map_game[7][8][3][1] or map_game[8][8][3][0]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_game[8][8][3][0]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_game[8][8][3][0] or map_game[8][8][3][1]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_game[8][8][3][1]:
                        return False
                else:
                    if map_game[8][8][3][1] or map_game[9][8][3][0]:
                        return False
        elif d == 3:
            y1 = y + self.velocity
            if 12 <= y1 % 64 <= 32:
                if 32 <= x % 64 <= 44:
                    if map_game[7][9][3][1] or map_game[8][9][3][0]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_game[8][9][3][0]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_game[8][9][3][0] or map_game[8][9][3][1]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_game[8][9][3][1]:
                        return False
                else:
                    if map_game[8][9][3][1] or map_game[9][9][3][0]:
                        return False
            if 32 > y1 % 64 or y1 % 64 >= 44:
                if 32 <= x % 64 <= 44:
                    if map_game[7][8][3][3] or map_game[8][8][3][2]:
                        return False
                elif 44 < x % 64 < 52:
                    if map_game[8][8][3][2]:
                        return False
                elif 52 <= x % 64 or x % 64 <= 12:
                    if map_game[8][8][3][2] or map_game[8][8][3][3]:
                        return False
                elif 12 < x % 64 < 20:
                    if map_game[8][8][3][3]:
                        return False
                else:
                    if map_game[8][8][3][3] or map_game[9][8][3][2]:
                        return False
        return True

    def get_stats(self):
        return self.hp, self.hp_max, self.hm, self.hm_max, self.attack, self.defense, self.level, self.xp, self.gold

    def use_object(self, i):
        self.inventory[1][i] -= 1
        if i == 0:
            pass
        elif i == 1:
            pass
        elif i == 2:
            pass
        elif i == 3:
            pass
        elif i == 4:
            pass
        elif i == 5:
            pass
        elif i == 6:
            pass
        elif i == 7:
            pass
        elif i == 8:
            pass
        elif i == 9:
            pass
        elif i == 10:
            pass
        elif i == 11:
            pass
        elif i == 12:
            pass
        elif i == 13:
            pass
        elif i == 14:
            pass
        elif i == 15:
            pass
        elif i == 16:
            pass
        elif i == 17:
            pass
        elif i == 18:
            pass
        elif i == 19:
            pass
        elif i == 20:
            pass
        elif i == 21:
            pass
        elif i == 22:
            pass
        elif i == 23:
            pass
        elif i == 24:
            pass
        elif i == 25:
            pass


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
proba base -0.03 min:base-0.09
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
