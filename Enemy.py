import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, gold, xp, defense, name, environment, attack, size, background, image):
        super().__init__()
        self.hp = hp
        self.gold = gold
        self.xp = xp
        self.defense = defense
        self.name = name
        self.environment = environment
        self.attack = attack
        self.background = background
        self.image = image
        self.size = size
        self.hp_max = hp
        self.boost_proba_crtit_enemy = 0.2
        self.boost_mult_crtit_enemy = 2

    def attack(self, hp_player, defense_player):
        hp_player -= (self.attack * random.randint(90, 110)) // defense_player
        return hp_player

    def defense(self, attack_player):
        self.hp -= (attack_player * random.randint(90, 110)) // self.defense
        if self.hp < 0:
            self.hp = 0

    def get_background(self):
        return self.background

    def get_name(self):
        return self.name, self.environment

    def get_image(self):
        return self.image

    def get_hp(self):
        return self.hp, self.hp_max

    def get_size(self):
        return self.size

    def change_boost_proba_crtit_enemy(self, n):
        if n:
            self.boost_proba_crtit_enemy -= 0.03
            if self.boost_proba_crtit_enemy < 0.11:
                self.boost_proba_crtit_enemy = 0.11
        else:
            self.boost_proba_crtit_enemy = 0.2

    def change_boost_mult_crtit_enemy(self, n):
        if n:
            self.boost_mult_crtit_enemy -= 0.1
            if self.boost_mult_crtit_enemy < 1.6:
                self.boost_mult_crtit_enemy = 1.6
        else:
            self.boost_mult_crtit_enemy = 2

