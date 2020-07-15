from Enemy import Enemy
import pygame
import Game

class Enemy1(Enemy):
    def __init__(self):
        super(Enemy1, self).__init__(100, 10, 10, 5, "Monster", Game.Settings.volcano, 10, (250, 160),
                                     pygame.image.load("assets/battle/backgrounds/background_grass.png"),
                                     pygame.image.load("assets/battle/enemies/enemy1.png"))
