class Armor:
    def __init__(self, defense_base, defense_volcano, defense_mountain, defense_forest, defense_snow, defense_plain,
                 defense_desert):
        self.defense_plain = defense_plain
        self.defense_desert = defense_desert
        self.defense_snow = defense_snow
        self.defense_forest = defense_forest
        self.defense_mountain = defense_mountain
        self.defense_volcano = defense_volcano
        self.defense_base = defense_base

    def get_stat(self):
        return self.defense_base, self.defense_snow, self.defense_desert, self.defense_forest, self.defense_volcano, \
               self.defense_mountain, self.defense_plain


class Sword:
    def __init__(self, attack_base, attack_volcano, attack_mountain, attack_forest, attack_snow, attack_plain,
                 attack_desert):
        self.attack_plain = attack_plain
        self.attack_desert = attack_desert
        self.attack_snow = attack_snow
        self.attack_forest = attack_forest
        self.attack_mountain = attack_mountain
        self.attack_volcano = attack_volcano
        self.attack_base = attack_base

    def get_stat(self):
        return self.attack_base, self.attack_snow, self.attack_desert, self.attack_forest, self.attack_volcano, \
               self.attack_mountain, self.attack_plain


armor = [
    [10, 0, 0, 0, 0, 0, 0]
]
sword = [
    [10, 0, 0, 0, 0, 0, 0]
]
