import os
import pickle

import pygame

from game import Button


def import_map():
    with open('game/file/map.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        map1 = file.load()
    return map1[0][0], map1[0][1], map1[1][0], map1[1][1]


Texts = None


def import_save(nb_save):
    try:
        os.rename('game/save/{}/save_game_'.format(nb_save), 'game/save/{}/save_game'.format(nb_save))
    except FileNotFoundError:
        pass
    try:
        with open('game/save/{}/save_game'.format(nb_save), 'rb') as file:
            file = pickle.Unpickler(file)
            _ = file.load()
    except pickle.UnpicklingError and FileNotFoundError:
        _ = [(100, 100, 50, 50, 10, 10, 1, 0, 5, 1, 1), [[], [3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], []],
             [275, 276, 274, 273, 100, 97, 115, 119], 2941, 3455, 'plain']
    return _


def import_language():
    global Texts
    with open('game/language/language.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        language = file.load()
    if language == "fr":
        from game.fr import Texts
    elif language == "en":
        from game.en import Texts
    button_pause = Button.Button(None, (0, 0, 0), [417, 240, 190, 65], Texts.resume, 'center', 32, board,
                                 'FRAMDCN.TTF')
    button_setting = Button.Button(None, (0, 0, 0), [417, 320, 190, 65], Texts.settings, 'center', 30, board,
                                   'FRAMDCN.TTF')
    button_save = Button.Button(None, (0, 0, 0), [417, 400, 190, 65], Texts.save, 'center', 28, board, 'FRAMDCN.TTF')
    button_exit = Button.Button(None, (0, 0, 0), [417, 480, 190, 65], Texts.quit_game, 'center', 34, board,
                                'FRAMDCN.TTF')
    return Texts, button_exit, button_save, button_pause, button_setting


def change_language(language):
    try:
        os.remove("game/language/language.txt")
    except FileNotFoundError:
        pass
    with open("game/language/language.txt", 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(language)
    return import_language()


board = pygame.image.load('game/assets/button/board.png')

# Picture

flower = pygame.image.load("game/assets/flower.png")
bunker = pygame.image.load('game/assets/bunker.png')
sand = pygame.image.load('game/assets/sand.png')
sand2 = pygame.image.load('game/assets/sand2.png')
dirt = pygame.image.load('game/assets/dirt.png')
dirt2 = pygame.image.load('game/assets/dirt2.png')
grass2 = pygame.image.load('game/assets/grass2.png')
water = pygame.image.load('game/assets/water.png')
water2 = pygame.image.load('game/assets/water2.png')
paving1 = pygame.image.load('game/assets/paving1.png')
paving2 = pygame.image.load('game/assets/paving2.png')
cliff = pygame.image.load('game/assets/cliff.png')
fence = pygame.image.load('game/assets/fence.png')
background = pygame.Surface((10000, 10000))
background.fill((31, 16, 2))
block = {
    "bunker_1": bunker.subsurface(64, 64, 64, 64),
    "bunker_dr": bunker.subsurface(0, 0, 64, 64),
    "bunker_cd": bunker.subsurface(64, 0, 64, 64),
    "bunker_dl": bunker.subsurface(128, 0, 64, 64),
    "bunker_cl": bunker.subsurface(128, 64, 64, 64),
    "bunker_ul": bunker.subsurface(128, 128, 64, 64),
    "bunker_cu": bunker.subsurface(64, 128, 64, 64),
    "bunker_ur": bunker.subsurface(0, 128, 64, 64),
    "bunker_cr": bunker.subsurface(0, 64, 64, 64),
    "bunker_dr_2": bunker.subsurface(256, 64, 64, 64),
    "bunker_dl_2": bunker.subsurface(192, 64, 64, 64),
    "bunker_ur_2": bunker.subsurface(256, 0, 64, 64),
    "bunker_ul_2": bunker.subsurface(192, 0, 64, 64),
    "bunker_u": bunker.subsurface(0, 192, 64, 64),
    "bunker_ur_3": bunker.subsurface(64, 192, 64, 64),
    "bunker_ul_3": bunker.subsurface(128, 192, 64, 64),
    "bunker_ur_4": bunker.subsurface(192, 192, 64, 64),
    "bunker_ul_4": bunker.subsurface(256, 192, 64, 64),
    "bunker_area_8": bunker.subsurface(256, 128, 64, 64),
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
    "stone": pygame.image.load("game/assets/grass/stone.png"),
    "red1": flower.subsurface(0, 0, 64, 64),
    "red2": flower.subsurface(0, 64, 64, 64),
    "red3": flower.subsurface(0, 128, 64, 64),
    "blue1": flower.subsurface(64, 0, 64, 64),
    "blue2": flower.subsurface(64, 64, 64, 64),
    "blue3": flower.subsurface(64, 128, 64, 64),
    "yellow1": flower.subsurface(128, 0, 64, 64),
    "yellow2": flower.subsurface(128, 64, 64, 64),
    "yellow3": flower.subsurface(128, 128, 64, 64),
    "1": pygame.transform.scale(pygame.image.load("game/assets/case.png"), (32, 32)),
    "0": pygame.image.load("game/assets/case.png"),
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
    'tree': [pygame.image.load("game/assets/tree/Tree.png"), -55, -150, [[0, 0]], [[128, 128]]],  #
    'tree2': [pygame.image.load("game/assets/temp/tree.png"), -190, -280, [[0, 0]], [[128, 128]]],
    # "assets/tree/Tree2.png"#
    'tree0': [pygame.image.load("game/assets/tree/Tree_r.png"), -55, -150, [[0, 0]], [[128, 128]]],  #
    'h1_l': [pygame.image.load("game/assets/house/house1.png"), -95, -265, [[52, 196]], [[216, 160]]],
    'h1': [pygame.image.load("game/assets/house/house1_2.png"), -95, -265, [[52, 196], [188, 196], [52, 196]],
           [[82, 160], [82, 160], [218, 128]]],
    'church': [pygame.image.load("game/assets/house/church.png"), -128, -390, [[0, 0]], [[128, 128]]],  #
    'h2': [pygame.image.load("game/assets/house/house2.png"), -96, -205, [[52, 132]], [[216, 160]]],
    'h3': [pygame.image.load("game/assets/house/house3.png"), -95, -285, [[52, 196]], [[216, 160]]],
    "locker": [pygame.image.load("game/assets/casier.png"), -16, 16, [[48, 32]], [[32, 64]]],  #
    "fence_0": [fence.subsurface(64, 128, 64, 64), 0, 0, [[0, 0]], [[128, 128]]],  #
    "fence_1": [fence.subsurface(64, 0, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_2": [fence.subsurface(192, 0, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_3": [fence.subsurface(256, 0, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_l": [fence.subsurface(0, 64, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_l2": [fence.subsurface(256, 128, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_l3": [fence.subsurface(192, 128, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_ld": [fence.subsurface(0, 128, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_lu": [fence.subsurface(0, 0, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_r": [fence.subsurface(128, 64, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_r2": [fence.subsurface(256, 64, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_r3": [fence.subsurface(192, 64, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_rd": [fence.subsurface(128, 128, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
    "fence_ru": [fence.subsurface(128, 0, 64, 64), 0, 0, [[0, 0]], [[16, 16]]],  #
}
del flower, bunker, sand, sand2, dirt, dirt2, grass2, water, water2, paving1, paving2, cliff, fence
music = {
    'village': 'game/sound/electropoze.wav',
    'plain': 'game/sound/speice.wav',
    'combat': 'game/sound/synthey.wav'
}
mob = {
    'boar': (48, 48),
    'player': (64, 64),
    'deer': (48, 56),
    'fallen': (48, 48)
}
