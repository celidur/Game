import random
import time

import pygame


class Enemy(pygame.sprite.Sprite):
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

    def reset_box(self, n1):
        if not n1 <= self.box <= n1 + 4:
            self.box = n1 + 1

    def move(self, move=True):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.075
            if self.direction == 'down':
                if move:
                    self.reset_box(-1)
                else:
                    self.box = 0
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0],
                                                        self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'left':
                if move:
                    self.reset_box(3)
                else:
                    self.box = 4
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0],
                                                        self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'up':
                if move:
                    self.reset_box(7)
                else:
                    self.box = 8
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0],
                                                        self.dimension_x,
                                                        self.dimension_y)
            elif self.direction == 'right':
                if move:
                    self.reset_box(11)
                else:
                    self.box = 12
                self.image = self.image_full.subsurface(self.list[self.box][1], self.list[self.box][0],
                                                        self.dimension_x,
                                                        self.dimension_y)

    def enemy_move(self):
        self.last_direction = []
        move = False

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

        if self.a == -1:
            if True:  # collision
                self.direction = "left"
                self.last_direction.append("left")
                move = True
        elif self.a == 1:
            if True:  # collision
                self.direction = "right"
                self.last_direction.append("right")
                move = True
        if self.b == -1:
            if True:  # collision
                self.direction = "up"
                self.last_direction.append("up")
                move = True
        elif self.b == 1:
            if True:  # collision
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
