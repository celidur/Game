import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, image, pos, size):
        super().__init__()
        self.Game = Game
        self.x = x
        self.y = y
        self.image = image
        self.rects = []
        for i, j in zip(pos, size):
            self.rects.append(pygame.Rect(self.x + i[0] + 32, self.y + i[1] + 32, j[0], j[1]))
