import pygame
import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
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

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def Move(self, direction):
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

    def Player_move(self, Pressed, x, y, Map, Width, Length):
        move = False
        if Pressed.get(pygame.K_DOWN) and y // 64 < Width - 1:
            d = self.Collision(y + 14, x + 17, x + 50, y + 50, y + 50, 1, 0, 3, 2, 0, -32, Map)
            if d:
                y += self.velocity
                self.Move("down")
                move = True
        elif Pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
            d = self.Collision(y + 16, x + 17, x + 50, y + 4, y + 4, 3, 2, 1, 0, 0, +32, Map)
            if d:
                y -= self.velocity
                self.Move("up")
                move = True
        if Pressed.get(pygame.K_RIGHT) and x // 64 < Length - 1:
            d = self.Collision(x + 14, x + 56, x + 56, y + 42, y + 10, 0, 2, 1, 3, -32, 0, Map)
            if d:
                x += self.velocity
                if not move:
                    self.Move("right")
        elif Pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
            d = self.Collision(x + 16, x + 10, x + 10, y + 42, y + 10, 1, 3, 0, 2, +32, 0, Map)
            if d:
                x -= self.velocity
                if not move:
                    self.Move("left")
        elif not move:
            self.Move("same")
        return x, y

    @staticmethod
    def Collision(a, b, c, d, e, f, g, h, i, j, k, Map):
        if (a // 32) % 2 == 0:
            b, c, d, e = b // 64, c // 64, d // 64, e // 64
            if (not Map[b][d][3][f]) and (not Map[c][e][3][g]):
                return True
        else:
            b, c, d, e = (b + j) // 64, (c + j) // 64, (d + k) // 64, (e + k) // 64
            if (not Map[b][d][3][h]) and (not Map[c][e][3][i]):
                return True
        return False
