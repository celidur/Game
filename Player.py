import pygame
from pygame import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player = pygame.image.load('assets/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rect = self.image.get_rect()

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def Move(self, direction):
        self.box += 1
        time.wait(42)
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
