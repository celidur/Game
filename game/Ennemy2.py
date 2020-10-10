import random

import pygame
import time


class Ennemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.mult_crit = 2
        self.frame = time.time()
        self.player = pygame.image.load('game/assets/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rect = self.image.get_rect()
        self.velocity = 5
        self.x, self.y = x, y
        self.last_direction = []
        self.nb = 0
        self.a, self.b = 0, 0
        self.time = time.time()

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

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

    def enemy_move(self, map_collision, width, length, x, y):
        if time.time() - 0.025 > self.time:
            self.time = time.time()
            self.last_direction = []
            move = False
            if 4 * 64 > self.x - x > 4 * -64 and 4 * 64 > self.y - y > 4 * -64:  # diriger vers le joueur
                self.a, self.b = 0, 0
                self.nb = 0
                if self.x - x > 32:
                    self.a = -1
                elif self.x - x < -32:
                    self.a = 1
                if self.y - y > 32:
                    self.b = -1
                elif self.y - y < -32:
                    self.b = 1
            else:
                if self.nb <= 0:
                    a = random.randint(0, 18)
                    self.a = (a % 3)-1
                    if a < 3:
                        self.b = 0
                    elif a < 6:
                        self.b = 1
                    else:
                        self.b = -1
                    if a > 8:
                        self.a, self.b = 0, 0
                    self.nb = random.randint(10, 30)
                self.nb -= 1
            if (self.x + 63) // 64 > 0 and self.collision(map_collision, 0, self.x, self.y) and self.a == -1:
                self.direction = "left"
                self.last_direction.append("left")
                move = True
            elif self.x // 64 < length - 1 and self.collision(map_collision, 1, self.x, self.y) and self.a == 1:
                self.direction = "right"
                self.last_direction.append("right")
                move = True
            if (self.y + 63) // 64 > 0 and self.collision(map_collision, 2, self.x, self.y) and self.b == -1:
                self.direction = "up"
                self.last_direction.append("up")
                move = True
            elif self.y // 64 < width - 1 and self.collision(map_collision, 3, self.x, self.y) and self.b == 1:
                self.direction = "down"
                self.last_direction.append("down")
                move = True
            if len(self.last_direction) == 2:
                velocity = int(self.velocity / 1.4)
            else:
                velocity = self.velocity
            for d in self.last_direction:
                if d == "left":
                    self.x -= velocity
                elif d == "right":
                    self.x += velocity
                elif d == "up":
                    self.y -= velocity
                elif d == "down":
                    self.y += velocity
            self.move(move)

    def collision(self, map_collision, d, x, y):
        l, w = len(map_collision), len(map_collision[0])
        x1, y1 = 0, 0
        if d == 0:
            x1, y1 = x - self.velocity, y
        elif d == 1:
            x1, y1 = x + self.velocity, y
        elif d == 2:
            x1, y1 = x, y - self.velocity
        elif d == 3:
            x1, y1 = x, y + self.velocity

        x_case, y_case = x1 // 64, y1 // 64
        x_, y_ = x1 % 64, y1 % 64

        if y_ <= 8:
            # bas case_act
            if x_ < 12:
                # bas case_act
                # gauche case_act + droite case_act
                if map_collision[x_case][y_case][2] or map_collision[x_case][y_case][3]:
                    return False
            elif x_ <= 20:
                # bas case_act
                # droite case_act
                if map_collision[x_case][y_case][3]:
                    return False
            elif x_ < 44:
                # bas case_act
                # droite case_act + gauche case_droite
                if map_collision[x_case][y_case][3] or map_collision[(x_case + 1) % l][y_case][2]:
                    return False
            elif x_ <= 52:
                # bas case_act
                # gauche case_droite
                if map_collision[(x_case + 1) % l][y_case][2]:
                    return False
            else:  # x_ < 64
                # bas case_act
                # gauche case_droite + droite case_droite
                if map_collision[(x_case + 1) % l][y_case][2] or map_collision[(x_case + 1) % l][y_case][3]:
                    return False
        elif y_ < 32:
            # bas  case_act + haut case_inf
            if x_ < 12:
                # bas  case_act + haut case_inf
                # gauche case_act + droite case_act
                if map_collision[x_case][y_case][2] or map_collision[x_case][y_case][3] or \
                        map_collision[x_case][(y_case + 1) % w][0] or map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ <= 20:
                # bas  case_act + haut case_inf
                # droite case_act
                if map_collision[x_case][y_case][3] or map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ < 44:
                # bas  case_act + haut case_inf
                # droite case_act + gauche case_droite
                if map_collision[x_case][y_case][3] or map_collision[(x_case + 1) % l][y_case][2] or \
                        map_collision[x_case][(y_case + 1) % w][1] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            elif x_ <= 52:
                # bas  case_act + haut case_inf
                # gauche case_droite
                if map_collision[(x_case + 1) % l][y_case][2] or map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            else:  # x_ < 64
                # bas  case_act + haut case_inf
                # gauche case_droite + droite case_droite
                if map_collision[(x_case + 1) % l][y_case][2] or map_collision[(x_case + 1) % l][y_case][3] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][1]:
                    return False
        elif y_ <= 40:
            # haut case_inf
            if x_ < 12:
                # haut case_inf
                # gauche case_act + droite case_act
                if map_collision[x_case][(y_case + 1) % w][0] or map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ <= 20:
                # haut case_inf
                # droite case_act
                if map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ < 44:
                # haut case_inf
                # droite case_act + gauche case_droite
                if map_collision[x_case][(y_case + 1) % w][1] or map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            elif x_ <= 52:
                # haut case_inf
                # gauche case_droite
                if map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            else:  # x_ < 64
                # haut case_inf
                # gauche case_droite + droite case_droite
                if map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][1]:
                    return False
        else:  # y_ < 64
            # haut case_inf + bas case_inf
            if x_ < 12:
                # haut case_inf + bas case_inf
                # gauche case_act + droite case_act
                if map_collision[x_case][(y_case + 1) % w][0] or map_collision[x_case][(y_case + 1) % w][1] or \
                        map_collision[x_case][(y_case + 1) % w][2] or map_collision[x_case][(y_case + 1) % w][3]:
                    return False
            elif x_ <= 20:
                # haut case_inf + bas case_inf
                # droite case_act
                if map_collision[x_case][(y_case + 1) % w][1] or map_collision[x_case][(y_case + 1) % w][3]:
                    return False
            elif x_ < 44:
                # haut case_inf + bas case_inf
                # droite case_act + gauche case_droite
                if map_collision[x_case][(y_case + 1) % w][1] or map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        map_collision[x_case][(y_case + 1) % w][3] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][2]:
                    return False
            elif x_ <= 52:
                # haut case_inf + bas case_inf
                # gauche case_droite
                if map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][2]:
                    return False
            else:  # x_ < 64
                # haut case_inf + bas case_inf
                # gauche case_droite + droite case_droite
                if map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][1] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][2] or \
                        map_collision[(x_case + 1) % l][(y_case + 1) % w][3]:
                    return False
        return True
