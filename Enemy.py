import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, gold, xp, defense, name, attack):
        super().__init__()
        self.hp = hp
        self.gold = gold
        self.xp = xp
        self.defense = defense
        self.name = name
        self.attack = attack

    def attack(self, hp_player, defense_player):
        hp_player -= (self.attack * random.randint(90, 110)) // defense_player

    def defense(self, attack_player):
        self.hp -= (attack_player * random.randint(90, 110)) // self.defense
        if self.hp < 0:
            self.hp = 0

