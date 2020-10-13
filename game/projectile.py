import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 10
        self.player = player
        self.direction = player.direction
        if self.direction == 'right' or self.direction == 'left':
            self.image = pygame.image.load("game/assets/temp/balle.png")
        else:
            self.image = pygame.image.load("game/assets/temp/balle2.png")
        self.rect = self.image.get_rect()
        if self.direction == 'right':
            self.rect.x = 365
            self.rect.y = 355
        elif self.direction == 'left':
            self.rect.x = 330
            self.rect.y = 355
            self.velocity *= -1
        elif self.direction == 'up':
            self.rect.x = 350
            self.rect.y = 320
            self.velocity *= -1
        else:
            self.rect.x = 350
            self.rect.y = 350
        self.x = self.rect.x - 320 + self.player.x
        self.y = self.rect.y - 320 + self.player.y

    def mov(self):
        if self.direction == 'right' or self.direction == 'left':
            self.x += self.velocity
            self.rect.y = self.y - self.player.y + 320
            self.rect.x = self.x - self.player.x + 320
        else:
            self.y += self.velocity
            self.rect.x = self.x - self.player.x + 320
            self.rect.y = self.y - self.player.y + 320
