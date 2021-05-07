import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, pos, size):
        super().__init__()
        self.Game = game
        self.x = x
        self.y = y
        self.image = image
        self.rects = []
        for i, j in zip(pos, size):
            self.rects.append(pygame.Rect(self.x + i[0], self.y + i[1], j[0], j[1]))
