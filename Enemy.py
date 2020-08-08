import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, stat):
        super().__init__()
        self.hp = stat[0]
        self.gold = stat[1]
        self.xp = stat[2]
        self.defense = stat[3]
        self.name = stat[4]
        self.environment = stat[5]
        self.attack = stat[6]
        self.background = stat[8]
        self.image = stat[9]
        self.size = stat[7]
        self.hp_max = stat[0]
        self.boost_proba_crtit_enemy = 0.2
        self.boost_mult_crtit_enemy = 2

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

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
