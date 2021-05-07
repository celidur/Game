import pygame
import time
from game import Armor
from game.Projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, stat, inventory, game):
        super().__init__()
        self.Game = game
        self.mult_crit = 2
        self.frame = time.time()
        self.player = pygame.image.load('game/assets/mobs/player.png').convert_alpha()
        self.list, self.box, self.direction = [], 0, "down"
        for i in range(4):
            for j in range(4):
                self.list.append([i * 64, j * 64])
        self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
        self.rects = [pygame.Rect(self.Game.x + 24, self.Game.y + 38, 16, 16)]
        self.velocity = 5
        self.radius = 50
        self.hp = stat[0]
        self.hp_max = stat[1]
        self.level = stat[6] * 0 + 1  #
        self.xp = stat[7]
        self.mp = stat[2] * 0 + 50  #
        self.mp_max = stat[3]
        self.attack = stat[4]
        self.defense = stat[5]
        self.inventory = inventory
        self.inventory = [[],
                          [3, 0, 0, 0, 0,
                           1, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0,
                           0],
                          []]
        self.gold = stat[8]
        self.num_armor = stat[10]
        self.num_sword = stat[9]
        self.all_projectiles = pygame.sprite.Group()
        self.armor = Armor.Armor(Armor.armor[self.num_armor - 1][0], Armor.armor[self.num_armor - 1][1],
                                 Armor.armor[self.num_armor - 1][2],
                                 Armor.armor[self.num_armor - 1][3],
                                 Armor.armor[self.num_armor - 1][4],
                                 Armor.armor[self.num_armor - 1][5],
                                 Armor.armor[self.num_armor - 1][6])
        self.sword = Armor.Sword(Armor.sword[self.num_sword - 1][0], Armor.sword[self.num_sword - 1][1],
                                 Armor.sword[self.num_sword - 1][2],
                                 Armor.sword[self.num_sword - 1][3],
                                 Armor.sword[self.num_sword - 1][4],
                                 Armor.sword[self.num_sword - 1][5],
                                 Armor.sword[self.num_sword - 1][6])
        self.stats = (self.hp, self.hp_max, self.mp, self.mp_max, self.attack, self.defense, self.level, self.xp,
                      self.gold, self.num_sword, self.num_armor)

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))

    def reset_box(self, n1):
        if not n1 <= self.box <= n1 + 4:
            self.box = n1 + 1

    def move(self, move=True):
        if time.time() > self.frame:
            self.box += 1
            self.frame = time.time() + 0.1
            if self.direction == 'down':
                if move:
                    self.reset_box(-1)
                else:
                    self.box = 0
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'left':
                if move:
                    self.reset_box(3)
                else:
                    self.box = 4
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'up':
                if move:
                    self.reset_box(7)
                else:
                    self.box = 8
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)
            elif self.direction == 'right':
                if move:
                    self.reset_box(11)
                else:
                    self.box = 12
                self.image = self.player.subsurface(self.list[self.box][1], self.list[self.box][0], 64, 64)

    def player_move(self):
        move = False
        direction = []
        if (self.Game.pressed.get(self.Game.Settings[1]) or self.Game.pressed.get(self.Game.Settings[5])) and \
                (self.Game.pressed.get(self.Game.Settings[0]) or self.Game.pressed.get(self.Game.Settings[4])):
            pass
        elif (self.Game.pressed.get(self.Game.Settings[1]) or self.Game.pressed.get(self.Game.Settings[5])) and (
                self.Game.x + 63) // 64 > 0 and self.collision(
                pygame.Rect(self.Game.x + 24 - self.velocity, self.Game.y + 38, 16, 16)):
            self.direction = "left"
            direction.append("left")
            move = True
        elif (self.Game.pressed.get(self.Game.Settings[0]) or self.Game.pressed.get(
                self.Game.Settings[4])) and self.Game.x // 64 < self.Game.Length - 1 and self.collision(
                pygame.Rect(self.Game.x + 24 + self.velocity, self.Game.y + 38, 16, 16)):
            self.direction = "right"
            direction.append("right")
            move = True
        if (self.Game.pressed.get(self.Game.Settings[3]) or self.Game.pressed.get(self.Game.Settings[7])) and \
                (self.Game.pressed.get(self.Game.Settings[2]) or self.Game.pressed.get(self.Game.Settings[6])):
            pass
        elif (self.Game.pressed.get(self.Game.Settings[3]) or self.Game.pressed.get(self.Game.Settings[7])) and (
                self.Game.y + 63) // 64 > 0 and self.collision(
                pygame.Rect(self.Game.x + 24, self.Game.y + 38 - self.velocity, 16, 16)):
            self.direction = "up"
            direction.append("up")
            move = True
        elif (self.Game.pressed.get(self.Game.Settings[2]) or self.Game.pressed.get(
                self.Game.Settings[6])) and self.Game.y // 64 < self.Game.Width - 1 and self.collision(
                pygame.Rect(self.Game.x + 24, self.Game.y + 38 + self.velocity, 16, 16)):
            self.direction = "down"
            direction.append("down")
            move = True
        if len(direction) == 2:
            velocity = int(self.velocity / 1.4)
        else:
            velocity = self.velocity
        for d in direction:
            if d == "left":
                self.Game.x -= velocity
            elif d == "right":
                self.Game.x += velocity
            elif d == "up":
                self.Game.y -= velocity
            elif d == "down":
                self.Game.y += velocity
        self.move(move)
        self.rects = [pygame.Rect(self.Game.x + 24, self.Game.y + 38, 16, 16)]

    def collision(self, rect):
        for entity in self.Game.entities:
            if entity[2] != self:
                for j in range(len(entity[2].rects)):
                    if rect.colliderect(entity[2].rects[j]):
                        return False
        return True
