from Enemy import Enemy
import pygame


class Enemy1(Enemy):
    def __init__(self):
        super(Enemy1, self).__init__(100, 10, 10, 5, "monster", 10, (250, 160),
                                     pygame.image.load("assets/battle/backgrounds/background_grass.png"),
                                     pygame.image.load("assets/battle/enemies/enemy1.png"))
