import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, decallage_x, decallage_y):
        super().__init__()
        self.Game = Game
        self.x = x
        self.y = y
        self.decallage_x = decallage_x
        self.decallage_y = decallage_y
