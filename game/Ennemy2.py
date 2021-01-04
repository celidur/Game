import random
import time

import pygame


class Ennemy2(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, image, dimension):
        super().__init__()
        self.Game = Game
        self.dimension_x = dimension[0]
        self.dimension_y = dimension[1]
        self.mult_crit = 2
        self.frame = time.time()
        self.image_full = pygame.image.load('game/assets/mobs/{}.png'.format(image)).convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * self.dimension_y, j * self.dimension_x])
        self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0], self.dimension_x,
                                                self.dimension_y)
        self.rect = self.image.get_rect()
        self.velocity = 3
        self.x, self.y = x, y
        self.last_direction = []
        self.nb = 0
        self.a, self.b = 0, 0
        self.time = time.time()
        self.go_to = None
        self.blocked_x = False
        self.blocked_y = False
        self.rects = [pygame.Rect(self.x + 24, self.y + 38, 16, 16)]

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def move(self, move=True):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.075
            if self.direction == 'down':
                if move:
                    self.box_change(-1)
                else:
                    self.box = 0
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0], self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'left':
                if move:
                    self.box_change(3)
                else:
                    self.box = 4
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0], self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'up':
                if move:
                    self.box_change(7)
                else:
                    self.box = 8
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0], self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'right':
                if move:
                    self.box_change(11)
                else:
                    self.box = 12
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0], self.dimension_x,
                                                        self.dimension_y)

    def enemy_move(self):
        self.last_direction = []
        move = False
        x_32, y_32 = ((self.x + 32) // 32) * 32 + 16, ((self.y + 32) // 32) * 32 + 16
        go_to = None
        d = -1
        for layer in range(0, 13):
            if (x_32, y_32) in self.Game.near_player[layer]:
                d = layer
                break

        if d > 0:
            for new_case in self.Game.near_player[d - 1]:
                if -32 <= x_32 - new_case[0] <= 32 and -32 <= y_32 - new_case[1] <= 32:
                    go_to = new_case
                    if new_case[0] == x_32 or new_case[1] == y_32:
                        break

        if d == 0:
            go_to = self.Game.near_player[0][0]
            self.a, self.b = 0, 0

        if d > 0:
            self.a, self.b = 0, 0
            if self.x - self.Game.x > 32 or self.x - self.Game.x < -32:
                if x_32 < go_to[0]:
                    self.a = 1
                if x_32 > go_to[0]:
                    self.a = -1
            if self.y - self.Game.y > 32 or self.y - self.Game.y < -32:
                if y_32 < go_to[1]:
                    self.b = 1
                if y_32 > go_to[1]:
                    self.b = -1

        if d < 0:
            if self.nb <= 0:
                r = random.randint(0, 18)
                if r in [0, 1, 2]:
                    self.a = -1
                elif r in [3, 4, 5]:
                    self.a = 1
                else:
                    self.a = 0
                if r in [0, 3, 6]:
                    self.b = -1
                elif r in [1, 4, 7]:
                    self.b = -1
                else:
                    self.b = 0
                self.nb = random.randint(10, 30)
            self.nb -= 1
        if go_to:
            if self.blocked_x:
                if self.y > go_to[1]:
                    self.b = -1
                elif self.y < go_to[1]:
                    self.b = 1
            if self.blocked_y:
                if self.x > go_to[0]:
                    self.a = -1
                elif self.x < go_to[0]:
                    self.a = 1

        self.blocked_x, self.blocked_y = False, False

        if self.a == -1:
            if self.collision(0):
                self.direction = "left"
                self.last_direction.append("left")
                move = True
            else:
                self.blocked_x = True
        elif self.a == 1:
            if self.collision(1):
                self.direction = "right"
                self.last_direction.append("right")
                move = True
            else:
                self.blocked_x = True
        if self.b == -1:
            if self.collision(2):
                self.direction = "up"
                self.last_direction.append("up")
                move = True
            else:
                self.blocked_y = True
        elif self.b == 1:
            if self.collision(3):
                self.direction = "down"
                self.last_direction.append("down")
                move = True
            else:
                self.blocked_y = True

        if len(self.last_direction) == 2:
            velocity = int(self.velocity / 1.4)
        else:
            velocity = self.velocity
        for d in self.last_direction:
            if d == "left":
                self.x -= velocity
                self.rect.x -= velocity
            elif d == "right":
                self.x += velocity
                self.rect.x += velocity
            elif d == "up":
                self.y -= velocity
                self.rect.y -= velocity
            elif d == "down":
                self.y += velocity
                self.rect.y += velocity
        self.move(move)
        """print(self.b)
        print('player :', self.Game.x, self.Game.y)
        print('enemy :', self.x, self.y)
        print(go_to)
        print()"""

        self.rects = [pygame.Rect(self.x + 24, self.y + 38, 16, 16)]

    def collision(self, d):
        l, w = len(self.Game.map_collision), len(self.Game.map_collision[0])
        x1, y1 = 0, 0
        if d == 0:
            x1, y1 = self.x - self.velocity, self.y
        elif d == 1:
            x1, y1 = self.x + self.velocity, self.y
        elif d == 2:
            x1, y1 = self.x, self.y - self.velocity
        elif d == 3:
            x1, y1 = self.x, self.y + self.velocity

        x_case, y_case = x1 // 64, y1 // 64
        x_, y_ = x1 % 64, y1 % 64

        if y_ <= 8:
            # bas case_act
            if x_ < 12:
                # bas case_act
                # gauche case_act + droite case_act
                if self.Game.map_collision[x_case][y_case][2] or self.Game.map_collision[x_case][y_case][3]:
                    return False
            elif x_ <= 20:
                # bas case_act
                # droite case_act
                if self.Game.map_collision[x_case][y_case][3]:
                    return False
            elif x_ < 44:
                # bas case_act
                # droite case_act + gauche case_droite
                if self.Game.map_collision[x_case][y_case][3] or self.Game.map_collision[(x_case + 1) % l][y_case][2]:
                    return False
            elif x_ <= 52:
                # bas case_act
                # gauche case_droite
                if self.Game.map_collision[(x_case + 1) % l][y_case][2]:
                    return False
            else:  # x_ < 64
                # bas case_act
                # gauche case_droite + droite case_droite
                if self.Game.map_collision[(x_case + 1) % l][y_case][2] or \
                        self.Game.map_collision[(x_case + 1) % l][y_case][3]:
                    return False
        elif y_ < 32:
            # bas  case_act + haut case_inf
            if x_ < 12:
                # bas  case_act + haut case_inf
                # gauche case_act + droite case_act
                if self.Game.map_collision[x_case][y_case][2] or self.Game.map_collision[x_case][y_case][3] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][0] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ <= 20:
                # bas  case_act + haut case_inf
                # droite case_act
                if self.Game.map_collision[x_case][y_case][3] or self.Game.map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ < 44:
                # bas  case_act + haut case_inf
                # droite case_act + gauche case_droite
                if self.Game.map_collision[x_case][y_case][3] or \
                        self.Game.map_collision[(x_case + 1) % l][y_case][2] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][1] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            elif x_ <= 52:
                # bas  case_act + haut case_inf
                # gauche case_droite
                if self.Game.map_collision[(x_case + 1) % l][y_case][2] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            else:  # x_ < 64
                # bas  case_act + haut case_inf
                # gauche case_droite + droite case_droite
                if self.Game.map_collision[(x_case + 1) % l][y_case][2] or \
                        self.Game.map_collision[(x_case + 1) % l][y_case][3] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][1]:
                    return False
        elif y_ <= 40:
            # haut case_inf
            if x_ < 12:
                # haut case_inf
                # gauche case_act + droite case_act
                if self.Game.map_collision[x_case][(y_case + 1) % w][0] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ <= 20:
                # haut case_inf
                # droite case_act
                if self.Game.map_collision[x_case][(y_case + 1) % w][1]:
                    return False
            elif x_ < 44:
                # haut case_inf
                # droite case_act + gauche case_droite
                if self.Game.map_collision[x_case][(y_case + 1) % w][1] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            elif x_ <= 52:
                # haut case_inf
                # gauche case_droite
                if self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0]:
                    return False
            else:  # x_ < 64
                # haut case_inf
                # gauche case_droite + droite case_droite
                if self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][1]:
                    return False
        else:  # y_ < 64
            # haut case_inf + bas case_inf
            if x_ < 12:
                # haut case_inf + bas case_inf
                # gauche case_act + droite case_act
                if self.Game.map_collision[x_case][(y_case + 1) % w][0] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][1] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][2] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][3]:
                    return False
            elif x_ <= 20:
                # haut case_inf + bas case_inf
                # droite case_act
                if self.Game.map_collision[x_case][(y_case + 1) % w][1] or \
                        self.Game.map_collision[x_case][(y_case + 1) % w][3]:
                    return False
            elif x_ < 44:
                # haut case_inf + bas case_inf
                # droite case_act + gauche case_droite
                if self.Game.map_collision[x_case][(y_case + 1) % w][1] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0] \
                        or self.Game.map_collision[x_case][(y_case + 1) % w][3] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][2]:
                    return False
            elif x_ <= 52:
                # haut case_inf + bas case_inf
                # gauche case_droite
                if self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][2]:
                    return False
            else:  # x_ < 64
                # haut case_inf + bas case_inf
                # gauche case_droite + droite case_droite
                if self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][0] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][1] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][2] or \
                        self.Game.map_collision[(x_case + 1) % l][(y_case + 1) % w][3]:
                    return False
        return True
