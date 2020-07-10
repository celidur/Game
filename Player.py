import pygame
import time


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = time.time()
        self.player = pygame.image.load('assets/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rect = self.image.get_rect()
        self.velocity = 8

    def box_change(self, n1):
        if self.box > n1 + 4:
            self.box = n1 + 1
        elif self.box < n1:
            self.box = n1 + 1

    def move(self, direction):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.1
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

    def player_move(self, pressed, x, y, map_game, width, length):
        move = False
        if pressed.get(pygame.K_DOWN) and y // 64 < width - 1:
            if self.collision(map_game, 3, x, y):
                y += self.velocity
                self.move("down")
                move = True
        elif pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
            if self.collision(map_game, 2, x, y):
                y -= self.velocity
                self.move("up")
                move = True
        if pressed.get(pygame.K_RIGHT) and x // 64 < length - 1:
            if self.collision(map_game, 1, x, y):
                x += self.velocity
                if not move:
                    self.move("right")
        elif pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
            if self.collision(map_game, 0, x, y):
                x -= self.velocity
                if not move:
                    self.move("left")
        elif not move:
            self.move("same")
        return x, y

    def collision(self, map_game, d, x, y):
        if d == 0:  # gauche
            x1 = x - self.velocity
            if 12 >= x1 % 64 or x1 % 64 >= 32:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[8][7][3][2] or map_game[8][8][3][0]:
                            return False
                    else:
                        if map_game[8][7][3][2] or map_game[8][8][3][2] or map_game[8][8][3][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[8][9][3][2] or map_game[8][8][3][0]:
                            return False
                    else:
                        if map_game[8][9][3][2] or map_game[8][8][3][2] or map_game[8][8][3][0]:
                            return False
                else:
                    if map_game[8][8][3][0] or map_game[8][8][3][2]:
                        return False

            if 32 <= x1 % 64 <= 44:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[7][7][3][3] or map_game[7][8][3][1]:
                            return False
                    else:
                        if map_game[7][7][3][3] or map_game[7][8][3][3] or map_game[7][8][3][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[7][9][3][3] or map_game[7][8][3][1]:
                            return False
                    else:
                        if map_game[7][9][3][3] or map_game[7][8][3][3] or map_game[7][8][3][1]:
                            return False
                else:
                    if map_game[7][8][3][1] or map_game[7][8][3][3]:
                        return False
        elif d == 1:  # droite
            x1 = x + self.velocity
            if 32 >= x1 % 64 or x1 % 64 >= 52:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[8][7][3][3] or map_game[8][8][3][1]:
                            return False
                    else:
                        if map_game[8][7][3][3] or map_game[8][8][3][3] or map_game[8][8][3][1]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[8][9][3][3] or map_game[8][8][3][1]:
                            return False
                    else:
                        if map_game[8][9][3][3] or map_game[8][8][3][3] or map_game[8][8][3][1]:
                            return False
                else:
                    if map_game[8][8][3][1] or map_game[8][8][3][3]:
                        return False

            if 32 >= x1 % 64 >= 20:
                if 52 >= y % 64 >= 32:
                    if y % 64 < 44:
                        if map_game[9][7][3][2] or map_game[9][8][3][0]:
                            return False
                    else:
                        if map_game[9][7][3][2] or map_game[9][8][3][2] or map_game[9][8][3][0]:
                            return False
                elif 12 <= y % 64 < 32:
                    if y % 64 > 20:
                        if map_game[9][9][3][2] or map_game[9][8][3][0]:
                            return False
                    else:
                        if map_game[9][9][3][2] or map_game[9][8][3][2] or map_game[9][8][3][0]:
                            return False
                else:
                    if map_game[9][8][3][0] or map_game[9][8][3][2]:
                        return False
        elif d == 2:  # haut
            y1 = y - self.velocity
            if 32 <= y1 % 64 <= 52:
                if 32 <= x % 64 <= 44:
                    pass
                elif 44 < x % 64 < 52:
                    pass
                elif 52 <= x % 64 or x % 64 <= 12:
                    pass
                elif 12 < x % 64 < 20:
                    pass
                else:
                    pass
            if 32 <= y1 % 64 or y1 % 64 <= 20:
                if 32 <= x % 64 <= 44:
                    pass
                elif 44 < x % 64 < 52:
                    pass
                elif 52 <= x % 64 or x % 64 <= 12:
                    pass
                elif 12 < x % 64 < 20:
                    pass
                else:
                    pass
        elif d == 3:  # bas
            y1 = y + self.velocity
            if 12 <= y1 % 64 <= 32:
                if 32 <= x % 64 <= 44:
                    pass
                elif 44 < x % 64 < 52:
                    pass
                elif 52 <= x % 64 or x % 64 <= 12:
                    pass
                elif 12 < x % 64 < 20:
                    pass
                else:
                    pass
            if 32 > y1 % 64 or y1 % 64 >= 44:
                if 32 <= x % 64 <= 44:
                    pass
                elif 44 < x % 64 < 52:
                    pass
                elif 52 <= x % 64 or x % 64 <= 12:
                    pass
                elif 12 < x % 64 < 20:
                    pass
                else:
                    pass
        return True
