import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, image):
        super().__init__()
        self.Game = Game
        self.x = x
        self.y = y
        self.image = image
