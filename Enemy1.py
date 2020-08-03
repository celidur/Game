from Enemy import Enemy
import pygame
import Game


class Enemy1(Enemy):
    def __init__(self):
        super(Enemy1, self).__init__(100, 10, 10, 5, "Monster", Game.Texts.volcano, 10, (218, 42),
                                     pygame.image.load("assets/battle/backgrounds/plain.png"),
                                     pygame.image.load("assets/battle/enemies/enemy1.png"))
