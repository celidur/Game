import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, stat):
        super().__init__()
        self.name = stat[0]
        self.hp_max = stat[1]
        self.hp = stat[1]
        self.attack = stat[2]
        self.defense = stat[3]
        self.boost_att = 1
        self.boost_def = 1
        self.boost_proba_crtit_enemy = 0.2
        self.boost_mult_crtit_enemy = 2
        self.gold = stat[4]
        self.xp = stat[5]
        self.size = stat[6]
        self.environment = stat[7]
        self.background = stat[8]
        self.image = stat[9]
        self.attacks = stat[10]

    def chose_attack_enemy(self):
        n = random.random()
        if n > 2:  # proba soin en plus
            return 1
        n = random.random()
        if n <= self.attacks[0]:
            return 0  # soin
        n -= self.attacks[0]
        if n <= self.attacks[1]:
            return 1  # attaque de base
        n -= self.attacks[1]
        if n <= self.attacks[2]:
            return 2  # attaque moyenne
        n -= self.attacks[2]

    def attack_enemy(self, n):
        if n == 0:  # soin
            self.change_hp(0.2 * self.hp_max)
        elif n == 1:  # attaque de base
            pass
        elif n == 2:  # attaque moyenne
            pass

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def change_hp(self, n):
        self.hp = int(self.hp + n)
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.hp_max:
            self.hp = self.hp_max

    def change_boost_att(self, n):
        self.boost_att += n
        if self.boost_att < 0.7:
            self.boost_att = 0.7
        elif self.boost_att > 1.3:
            self.boost_att = 1.3

    def change_boost_def(self, n):
        self.boost_def += n
        if self.boost_def < 0.7:
            self.boost_def = 0.7
        elif self.boost_def > 1.3:
            self.boost_def = 1.3















    #  kk
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
    # fin kk
