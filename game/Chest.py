import pygame


class Chest(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, inventory):
        super().__init__()
        self.Game = Game
        self.x = x
        self.y = y
        self.inventory = inventory
