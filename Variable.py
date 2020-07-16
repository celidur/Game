import os
import pickle

import pygame

import Button


def import_map():
    with open('file/map.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        map1 = file.load()
    with open('file/size.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        size = file.load()
    length, width = size[0], size[1]
    return map1, length, width


Settings = None


def length(string, size, font='arial'):
    ls = None
    if font == 'rpg_':
        ls = -(size / 8)
        for char in string:
            if char in ['i', 'I', ' ', '.', ':', ',', ';', "'", '!']:
                ls += size / 3.6
            elif char in ['1', '"', '[', ']', '*']:
                ls += size / 2.4
            else:
                ls += size / 1.5
            ls = int(ls)
        ls += size / 8
        ls = int(ls)
    elif font == 'arial':
        ls = 0
        for char in string:
            if char in ['m', 'w', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z']:
                ls += size / (72 / 82)
            elif char in ['a', 'b', 'd', 'e', 'h', 'k', 'u', 'g', 'x', 'y', 'z', 'v', 's', 'p', 'q', 'o', 'n', 'J', 'L',
                          'é', 'è', 'ê', 'à', 'â', 'ù', 'û', '2', '4', '6', '5', '7', '8', '9', '0', '?', '+', '=']:
                ls += size / (72 / 56)  # 1.286
            elif char in ['c', 'ç', '1', '3']:
                ls += size / (72 / 46)  # 1.565
            elif char in ['f', 'j', 't', 'r', '(', ')', '-', '*', '/', '"']:
                ls += size / 2.4
            elif char in ['i', 'l', 'I', ' ', '.', ':', ',', ';', "'", '!']:
                ls += size / (72 / 18)  # 4
        ls = int(ls) // 2
    return ls


def import_language():
    global Settings
    with open('language/language.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        language = file.load()
    if language == "fr":
        from fr import Settings
    elif language == "en":
        from en import Settings
    button_pause = Button.Button(None, (0, 0, 0), [257, 240, 190, 65], Settings.resume, (270, 253), 32, board)
    button_setting = Button.Button(None, (0, 0, 0), [257, 320, 190, 65], Settings.settings, (271, 333), 30, board)
    button_save = Button.Button(None, (0, 0, 0), [257, 400, 190, 65], Settings.save, (264, 415), 28, board)
    button_exit = Button.Button(None, (0, 0, 0), [257, 480, 190, 65], Settings.quit_game, (290, 492), 34, board)
    button_attack = Button.Button((127, 127, 127), (255, 255, 255), [280, 430, 110, 40], Settings.attack,
                                  (285, 435), 25)
    button_magic = Button.Button((127, 127, 127), (255, 255, 255), [280, 505, 110, 40], Settings.magic,
                                 (285, 510), 25)
    button_inventory = Button.Button((127, 127, 127), (255, 255, 255), [280, 580, 110, 40], Settings.inventory,
                                     (285, 585), 25)
    button_leave = Button.Button((127, 127, 127), (255, 255, 255), [280, 655, 110, 40], Settings.leave,
                                 (285, 660), 25)
    return Settings, button_exit, button_menu, button_magic, button_leave, button_inventory, button_attack, \
           button_save, button_pause, button_setting


def change_language(language):
    try:
        os.remove("language/language.txt")
    except FileNotFoundError:
        pass
    with open("language/language.txt", 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(language)
    return import_language()


board = pygame.image.load('assets/button/board.png')

button_shop = Button.Button((0, 0, 0), None, [615, 702, 32, 32], None, None, 0,
                            pygame.image.load('assets/icons/shop.png'))
button_menu = Button.Button((0, 0, 0), None, [660, 700, 32, 32], None, None, 0,
                            pygame.image.load('assets/icons/menu.png'))
size_window = [704, 736]

# Picture

flower = pygame.image.load("assets/flower.png")
sand = pygame.image.load('assets/sand.png')
sand2 = pygame.image.load('assets/sand2.png')
dirt = pygame.image.load('assets/dirt.png')
dirt2 = pygame.image.load('assets/dirt2.png')
grass2 = pygame.image.load('assets/grass2.png')
water = pygame.image.load('assets/water.png')
water2 = pygame.image.load('assets/water2.png')
paving1 = pygame.image.load('assets/paving1.png')
paving2 = pygame.image.load('assets/paving2.png')
cliff = pygame.image.load('assets/cliff.png')
fence = pygame.image.load('assets/fence.png')
background = pygame.image.load('assets/fond.png')
block = {
    "sand_1": sand.subsurface(64, 64, 64, 64),
    "sand_dr": sand.subsurface(0, 0, 64, 64),
    "sand_cd": sand.subsurface(64, 0, 64, 64),
    "sand_dl": sand.subsurface(128, 0, 60, 64),
    "sand_cl": sand.subsurface(128, 64, 60, 64),
    "sand_ul": sand.subsurface(128, 128, 64, 64),
    "sand_cu": sand.subsurface(64, 128, 64, 64),
    "sand_ur": sand.subsurface(0, 128, 64, 64),
    "sand_cr": sand.subsurface(0, 64, 64, 64),
    "sand_dr_2": sand.subsurface(256, 64, 64, 64),
    "sand_dl_2": sand.subsurface(192, 64, 64, 64),
    "sand_ur_2": sand.subsurface(256, 0, 64, 64),
    "sand_ul_2": sand.subsurface(192, 0, 64, 64),
    "sand2_1": sand2.subsurface(64, 64, 64, 64),
    "sand2_dr": sand2.subsurface(0, 0, 64, 64),
    "sand2_cd": sand2.subsurface(64, 0, 64, 64),
    "sand2_dl": sand2.subsurface(128, 0, 64, 64),
    "sand2_cl": sand2.subsurface(128, 64, 64, 64),
    "sand2_ul": sand2.subsurface(128, 128, 64, 64),
    "sand2_cu": sand2.subsurface(64, 128, 64, 64),
    "sand2_ur": sand2.subsurface(0, 128, 64, 64),
    "sand2_cr": sand2.subsurface(0, 64, 64, 64),
    "sand2_dr_2": sand2.subsurface(256, 64, 64, 64),
    "sand2_dl_2": sand2.subsurface(192, 64, 64, 64),
    "sand2_ur_2": sand2.subsurface(256, 0, 64, 64),
    "sand2_ul_2": sand2.subsurface(192, 0, 64, 64),
    "grass2_1": grass2.subsurface(64, 64, 64, 64),
    "grass2_dr": grass2.subsurface(0, 0, 64, 64),
    "grass2_cd": grass2.subsurface(64, 0, 64, 64),
    "grass2_dl": grass2.subsurface(128, 0, 64, 64),
    "grass2_cl": grass2.subsurface(128, 64, 64, 64),
    "grass2_ul": grass2.subsurface(128, 128, 64, 64),
    "grass2_cu": grass2.subsurface(64, 128, 64, 64),
    "grass2_ur": grass2.subsurface(0, 128, 64, 64),
    "grass2_cr": grass2.subsurface(0, 64, 64, 64),
    "grass2_dr_2": grass2.subsurface(256, 64, 64, 64),
    "grass2_dl_2": grass2.subsurface(192, 64, 64, 64),
    "grass2_ur_2": grass2.subsurface(256, 0, 64, 64),
    "grass2_ul_2": grass2.subsurface(192, 0, 64, 64),
    "dirt_1": dirt.subsurface(64, 64, 64, 64),
    "dirt_dr": dirt.subsurface(0, 0, 64, 64),
    "dirt_cd": dirt.subsurface(64, 0, 64, 64),
    "dirt_dl": dirt.subsurface(128, 0, 62, 64),
    "dirt_cl": dirt.subsurface(128, 64, 62, 64),
    "dirt_ul": dirt.subsurface(128, 128, 62, 64),
    "dirt_cu": dirt.subsurface(64, 128, 64, 64),
    "dirt_ur": dirt.subsurface(0, 128, 64, 64),
    "dirt_cr": dirt.subsurface(0, 64, 64, 64),
    "dirt_dr_2": dirt.subsurface(256, 64, 64, 64),
    "dirt_dl_2": dirt.subsurface(192, 64, 64, 64),
    "dirt_ur_2": dirt.subsurface(256, 0, 64, 64),
    "dirt_ul_2": dirt.subsurface(192, 0, 64, 64),
    "dirt2_1": dirt2.subsurface(64, 64, 64, 64),
    "dirt2_dr": dirt2.subsurface(0, 0, 64, 64),
    "dirt2_cd": dirt2.subsurface(64, 0, 64, 64),
    "dirt2_dl": dirt2.subsurface(128, 0, 64, 64),
    "dirt2_cl": dirt2.subsurface(128, 64, 64, 64),
    "dirt2_ul": dirt2.subsurface(128, 128, 64, 64),
    "dirt2_cu": dirt2.subsurface(64, 128, 64, 64),
    "dirt2_ur": dirt2.subsurface(0, 128, 64, 64),
    "dirt2_cr": dirt2.subsurface(0, 64, 64, 64),
    "dirt2_dr_2": dirt2.subsurface(256, 64, 64, 64),
    "dirt2_dl_2": dirt2.subsurface(192, 64, 64, 64),
    "dirt2_ur_2": dirt2.subsurface(256, 0, 64, 64),
    "dirt2_ul_2": dirt2.subsurface(192, 0, 64, 64),
    "water_1": water.subsurface(64, 64, 64, 64),
    "water_dr": water.subsurface(0, 0, 64, 64),
    "water_cd": water.subsurface(64, 0, 64, 64),
    "water_dl": water.subsurface(128, 0, 64, 64),
    "water_cl": water.subsurface(128, 64, 64, 64),
    "water_ul": water.subsurface(128, 128, 64, 64),
    "water_cu": water.subsurface(64, 128, 64, 64),
    "water_ur": water.subsurface(0, 128, 64, 64),
    "water_cr": water.subsurface(0, 64, 64, 64),
    "water_dr_2": water.subsurface(256, 64, 64, 64),
    "water_dl_2": water.subsurface(192, 64, 64, 64),
    "water_ur_2": water.subsurface(256, 0, 64, 64),
    "water_ul_2": water.subsurface(192, 0, 64, 64),
    "water2_1": water2.subsurface(64, 64, 64, 64),
    "water2_dr": water2.subsurface(0, 0, 64, 64),
    "water2_cd": water2.subsurface(64, 0, 64, 64),
    "water2_dl": water2.subsurface(128, 0, 64, 64),
    "water2_cl": water2.subsurface(128, 64, 64, 64),
    "water2_ul": water2.subsurface(128, 128, 64, 64),
    "water2_cu": water2.subsurface(64, 128, 64, 64),
    "water2_ur": water2.subsurface(0, 128, 64, 64),
    "water2_cr": water2.subsurface(0, 64, 64, 64),
    "water2_dr_2": water2.subsurface(256, 64, 64, 64),
    "water2_dl_2": water2.subsurface(192, 64, 64, 64),
    "water2_ur_2": water2.subsurface(256, 0, 64, 64),
    "water2_ul_2": water2.subsurface(192, 0, 64, 64),
    "paving1_1": paving1.subsurface(64, 64, 64, 64),
    "paving1_2": paving1.subsurface(320, 0, 64, 64),
    "paving1_dr": paving1.subsurface(0, 0, 64, 64),
    "paving1_cd": paving1.subsurface(64, 0, 64, 64),
    "paving1_dl": paving1.subsurface(128, 0, 64, 64),
    "paving1_cl": paving1.subsurface(128, 64, 60, 64),
    "paving1_ul": paving1.subsurface(128, 128, 64, 64),
    "paving1_cu": paving1.subsurface(64, 128, 64, 64),
    "paving1_ur": paving1.subsurface(0, 128, 64, 64),
    "paving1_cr": paving1.subsurface(0, 64, 64, 64),
    "paving1_dr_2": paving1.subsurface(256, 64, 64, 64),
    "paving1_dl_2": paving1.subsurface(192, 64, 64, 64),
    "paving1_ur_2": paving1.subsurface(256, 0, 64, 64),
    "paving1_ul_2": paving1.subsurface(192, 0, 64, 64),
    "paving2_1": paving2.subsurface(64, 64, 64, 64),
    "paving2_dr": paving2.subsurface(0, 0, 64, 64),
    "paving2_cd": paving2.subsurface(64, 0, 64, 64),
    "paving2_dl": paving2.subsurface(128, 0, 64, 64),
    "paving2_cl": paving2.subsurface(128, 64, 64, 64),
    "paving2_ul": paving2.subsurface(128, 128, 64, 64),
    "paving2_cu": paving2.subsurface(64, 128, 64, 64),
    "paving2_ur": paving2.subsurface(0, 128, 64, 64),
    "paving2_cr": paving2.subsurface(0, 64, 64, 64),
    "fence_0": fence.subsurface(64, 128, 64, 64),
    "fence_1": fence.subsurface(64, 0, 64, 64),
    "fence_2": fence.subsurface(192, 0, 64, 64),
    "fence_3": fence.subsurface(256, 0, 64, 64),
    "fence_l": fence.subsurface(0, 64, 64, 64),
    "fence_l2": fence.subsurface(256, 128, 64, 64),
    "fence_l3": fence.subsurface(192, 128, 64, 64),
    "fence_ld": fence.subsurface(0, 128, 64, 64),
    "fence_lu": fence.subsurface(0, 0, 64, 64),
    "fence_r": fence.subsurface(128, 64, 64, 64),
    "fence_r2": fence.subsurface(256, 64, 64, 64),
    "fence_r3": fence.subsurface(192, 64, 64, 64),
    "fence_rd": fence.subsurface(128, 128, 64, 64),
    "fence_ru": fence.subsurface(128, 0, 64, 64),
    "stone": pygame.image.load("assets/grass/stone.png"),
    "red1": flower.subsurface(0, 0, 64, 64),
    "red2": flower.subsurface(0, 64, 64, 64),
    "red3": flower.subsurface(0, 128, 64, 64),
    "blue1": flower.subsurface(64, 0, 64, 64),
    "blue2": flower.subsurface(64, 64, 64, 64),
    "blue3": flower.subsurface(64, 128, 64, 64),
    "yellow1": flower.subsurface(128, 0, 64, 64),
    "yellow2": flower.subsurface(128, 64, 64, 64),
    "yellow3": flower.subsurface(128, 128, 64, 64),
    "1": pygame.transform.scale(pygame.image.load("assets/case.png"), (32, 32)),
    "0": pygame.image.load("assets/case.png"),
    "grass_1": cliff.subsurface(64, 64, 64, 64),
    "cliff_dr": cliff.subsurface(0, 0, 64, 64),
    "cliff_cd": cliff.subsurface(64, 0, 64, 64),
    "cliff_dl": cliff.subsurface(128, 0, 64, 64),
    "cliff_cl": cliff.subsurface(128, 64, 64, 64),
    "cliff_ul": cliff.subsurface(128, 128, 64, 64),
    "cliff_cu": cliff.subsurface(64, 128, 64, 64),
    "cliff_ur": cliff.subsurface(0, 128, 64, 64),
    "cliff_cr": cliff.subsurface(0, 64, 64, 64),
}
block2 = {
    'tree': [pygame.image.load("assets/tree/Tree.png"), -24, 15],
    'tree2': [pygame.image.load("assets/tree/Tree2.png"), 0, 0],
    'tree0': [pygame.image.load("assets/tree/Tree_r.png"), -24, 15],
    'h1': [pygame.image.load("assets/house/house1.png"), -95, -265],
    'church': [pygame.image.load("assets/house/church.png"), -128, -390],
    'h2': [pygame.image.load("assets/house/house2.png"), -96, -205],
    'h3': [pygame.image.load("assets/house/house3.png"), -95, -285]
}

Map, Length, Width = import_map()
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((size_window[0], size_window[1]))
