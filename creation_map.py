import os
import pickle
import random

import pygame
from pygame import time

from Player import Player


def import_map():
    with open('file/map.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        map1 = file.load()
    with open('file/size.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        size = file.load()
    length, width = size[0], size[1]
    return map1, length, width


def generation_map(length, width):
    map1 = []
    for j in range(length):
        L = []
        for i in range(width):
            L.append(['grass_1', '', "0", ""])
        map1.append(L)
    return map1, length, width


b = "sand"
Map, Length, Width = import_map()
# Map, Length, Width = generation_map(53,36)
pygame.init()
image_size_length = 11
pygame.display.set_caption("generated")
Screen = pygame.display.set_mode((image_size_length * 64, 11 * 64 + 30))
x, y, layer, velocity, pressed, x1, y1, x2, y2 = 59 * 64, 13 * 64, 0, 15, {}, -1, -1, -1, -1
arial_font, a, x_input, y_input, layer_input = pygame.font.SysFont("arial", 14), False, False, False, False
velocity_input, b_input, user_input_value = False, False, ""
player = Player()
flower = pygame.image.load("assets/flower.png")
fond = pygame.image.load("assets/fond.png")
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
    "1": pygame.image.load("assets/case.png"),
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
    "tree": [pygame.image.load("assets/tree/Tree.png"), -24, 15],
    "tree2": [pygame.image.load("assets/tree/Tree2.png"), 0, 16],
    "tree0": [pygame.image.load("assets/tree/Tree_r.png"), -24, 15],
    "h1": [pygame.image.load("assets/house/house1.png"), -95, -265],
    "church": [pygame.image.load("assets/house/church.png"), -128, -400],
    "h2": [pygame.image.load("assets/house/house2.png"), -96, -205],
    "h3": [pygame.image.load("assets/house/house3.png"), -95, -285],
}


def Save():
    global Map
    try:
        os.remove("file/map.txt")
    except FileNotFoundError:
        pass
    try:
        os.remove("file/size.txt")
    except FileNotFoundError:
        pass
    with open('file/map.txt', 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(Map)
    with open('file/size.txt', 'wb') as file:
        size = [Length, Width]
        pickler = pickle.Pickler(file)
        pickler.dump(size)


def Afficher_case(Block, x_case, y_case, move_x=0, move_y=0):
    Screen.blit(Block, (int((x_case + 5) * 64 - (x % 64)) + move_x, int((y_case + 5) * 64 - (y % 64) + move_y)))


def management_Screen(X1, X2, Y1, Y2, n, Block):
    for X_case in range(X1, (image_size_length + 1) // 2 + X2):
        for Y_case in range(Y1, Y2):
            if 0 <= X_case + x // 64 < Length and y // 64 + Y_case >= 0 and Y_case + y // 64 < Width:
                if n == 3:
                    if Map[x // 64 + X_case][y // 64 + Y_case][n]:
                        Afficher_case(Block["1"], X_case, Y_case)
                elif Map[x // 64 + X_case][y // 64 + Y_case][n] in Block:
                    if n == 4:
                        block_2 = Block[Map[x // 64 + X_case][y // 64 + Y_case][n]]
                        Afficher_case(block_2[0], X_case, Y_case, block_2[1], block_2[2])
                    else:
                        Afficher_case(Block[Map[x // 64 + X_case][y // 64 + Y_case][n]], X_case, Y_case)


def Afficher():
    global Width, Length, x, y, x_input, user_input_value, a
    Screen.blit(fond, (0, 0))
    management_Screen(-5, 3, -6, 7, 0, block)
    management_Screen(-5, 3, -6, 7, 1, block)
    management_Screen(-5, 3, -6, 7, 2, block)
    management_Screen(-9, 8, -8, 12, 4, block2)
    if a:
        management_Screen(-5, 3, -6, 7, 3, block)
    # barre de gestion
    Screen.blit(player.image, (image_size_length // 2 * 64, 5 * 64))
    pygame.draw.rect(Screen, (99, 99, 99), [0, 704, image_size_length * 64, 30])
    Screen.blit(arial_font.render('x =', False, (255, 255, 255)), (10, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [30, 710, 25, 15])
    if not x_input:
        Screen.blit(arial_font.render(str((x + 32) // 64), False, (255, 255, 255)), (34, 708))
    else:
        Screen.blit(arial_font.render(str(user_input_value), False, (255, 255, 255)), (34, 708))
    Screen.blit(arial_font.render('y = ', False, (255, 255, 255)), (60, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [80, 710, 25, 15])
    if not y_input:
        Screen.blit(arial_font.render(str((y + 32) // 64), False, (255, 255, 255)), (84, 708))
    else:
        Screen.blit(arial_font.render(str(user_input_value), False, (255, 255, 255)), (84, 708))
    Screen.blit(arial_font.render('Velocity = ', False, (255, 255, 255)), (115, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [168, 710, 25, 15])
    if not velocity_input:
        Screen.blit(arial_font.render(str(velocity), False, (255, 255, 255)), (170, 708))
    else:
        Screen.blit(arial_font.render(str(user_input_value), False, (255, 255, 255)), (170, 708))
    Screen.blit(arial_font.render('x1 = ', False, (255, 255, 255)), (200, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [225, 710, 25, 15])
    Screen.blit(arial_font.render(str(x1), False, (255, 255, 255)), (230, 708))
    Screen.blit(arial_font.render('y1 = ', False, (255, 255, 255)), (260, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [285, 710, 25, 15])
    Screen.blit(arial_font.render(str(y1), False, (255, 255, 255)), (290, 708))
    Screen.blit(arial_font.render('x2 = ', False, (255, 255, 255)), (320, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [345, 710, 25, 15])
    Screen.blit(arial_font.render(str(x2), False, (255, 255, 255)), (350, 708))
    Screen.blit(arial_font.render('y2 = ', False, (255, 255, 255)), (380, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [405, 710, 25, 15])
    Screen.blit(arial_font.render(str(y2), False, (255, 255, 255)), (410, 708))
    Screen.blit(arial_font.render('block = ', False, (255, 255, 255)), (440, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [480, 710, 50, 15])
    if not b_input:
        Screen.blit(arial_font.render(str(b), False, (255, 255, 255)), (485, 708))
    else:
        Screen.blit(arial_font.render(str(user_input_value), False, (255, 255, 255)), (485, 708))
    Screen.blit(arial_font.render('layer =', False, (255, 255, 255)), (540, 708))
    pygame.draw.rect(Screen, (0, 0, 0), [580, 710, 21, 15])
    if not layer_input:
        Screen.blit(arial_font.render(str(layer), False, (255, 255, 255)), (587, 708))
    else:
        Screen.blit(arial_font.render(str(user_input_value), False, (255, 255, 255)), (587, 708))
    pygame.display.update()


def Keyboard_pressed(Pressed):
    global x, y, velocity, a, b
    if Pressed.get(pygame.K_NUMLOCK):
        a = True
    else:
        a = False
    move = False
    if Pressed.get(pygame.K_DOWN) and y // 64 < Width - 1:
        y += velocity
        player.Move("down")
        move = True
    elif Pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
        y -= velocity
        player.Move("up")
        move = True
    if Pressed.get(pygame.K_RIGHT) and x // 64 < Length - 1:
        x += velocity
        if not move:
            player.Move("right")
    elif Pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
        x -= velocity
        if not move:
            player.Move("left")
    elif not move:
        player.Move("same")
    if Pressed.get(pygame.K_KP1):
        change_case(b + "_ur", layer)
    elif Pressed.get(pygame.K_KP2):
        change_case(b + "_cu", layer)
    elif Pressed.get(pygame.K_KP3):
        change_case(b + "_ul", layer)
    elif Pressed.get(pygame.K_KP4):
        change_case(b + "_cr", layer)
    elif Pressed.get(pygame.K_KP5):
        if b == "cliff":
            b = "grass"
        change_case(b + "_1", layer)
        if b == "grass":
            b = "cliff"
    elif Pressed.get(pygame.K_KP6):
        change_case(b + "_cl", layer)
    elif Pressed.get(pygame.K_KP7):
        change_case(b + "_dr", layer)
    elif Pressed.get(pygame.K_KP8):
        change_case(b + "_cd", layer)
    elif Pressed.get(pygame.K_KP9):
        change_case(b + "_dl", layer)
    elif Pressed.get(pygame.K_KP_MINUS):
        change_case("", layer)
    elif Pressed.get(pygame.K_1):
        change_case("fence_0", layer)
    elif Pressed.get(pygame.K_2):
        change_case("fence_1", layer)
    elif Pressed.get(pygame.K_3):
        change_case("fence_2", layer)
    elif Pressed.get(pygame.K_4):
        change_case("fence_3", layer)
    elif Pressed.get(pygame.K_5):
        change_case("fence_l3", layer)
    elif Pressed.get(pygame.K_6):
        change_case("fence_lu", layer)
    elif Pressed.get(pygame.K_7):
        change_case("fence_ru", layer)
    elif Pressed.get(pygame.K_8):
        change_case("fence_r", layer)
    elif Pressed.get(pygame.K_9):
        change_case("fence_rd", layer)
    elif Pressed.get(pygame.K_0):
        change_case("fence_ld", layer)
    elif Pressed.get(pygame.K_o) and b != "cliff" and b != "paving2":
        change_case(b + "_dr_2", layer)
    elif Pressed.get(pygame.K_p) and b != "cliff" and b != "paving2":
        change_case(b + "_dl_2", layer)
    elif Pressed.get(pygame.K_l) and b != "cliff" and b != "paving2":
        change_case(b + "_ur_2", layer)
    elif Pressed.get(pygame.K_SEMICOLON) and b != "cliff" and b != "paving2":
        change_case(b + "_ul_2", layer)
    elif Pressed.get(pygame.K_n):
        change_case("grass_1", layer)
    elif Pressed.get(pygame.K_KP0):
        change_case("0", layer)
    elif Pressed.get(pygame.K_b):
        n = random.randint(0, 2)
        if n == 0:
            f = "red"
        elif n == 1:
            f = "yellow"
        else:
            f = "blue"
        f += str(random.randint(1, 3))
        change_case(f, layer)
        time.wait(42)
    elif Pressed.get(pygame.K_v):
        change_case("stone", layer)
    elif Pressed.get(pygame.K_F1):
        change_case("h1", 4)
    elif Pressed.get(pygame.K_F2):
        change_case("tree", 4)
    elif Pressed.get(pygame.K_F3):
        change_case("tree0", 4)
    elif Pressed.get(pygame.K_F4):
        change_case("tree2", 4)
    elif Pressed.get(pygame.K_F5):
        change_case("church", 4)
    elif Pressed.get(pygame.K_F6):
        change_case("h2", 4)
    elif Pressed.get(pygame.K_F7):
        change_case("h3", 4)
    elif Pressed.get(pygame.K_DELETE):
        change_case("", 4)
    elif Pressed.get(pygame.K_SPACE):
        change_case(True, 3)
    elif Pressed.get(pygame.K_LCTRL):
        change_case(False, 3)
    Save()
    Afficher()


def change_case(c, z):
    global x1, x2, y1, y2, x, y
    if y2 == -1 or x2 == -1 or y1 == -1 or x1 == -1:
        Map[(x + 32) // 64][(y + 32) // 64][z] = c


def input_game(size, m=0):
    Afficher()
    global user_input_value
    continued = True
    user_input_value = ""
    while continued:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                continued = False
                break
            elif Event.type == pygame.KEYDOWN:
                if Event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if m == 0:
                        if user_input_value == '':
                            user_input_value = 0
                        if int(user_input_value) > size - 1:
                            user_input_value = size - 1
                        return int(user_input_value)
                    return user_input_value
                elif Event.key == pygame.K_BACKSPACE:
                    user_input_value = user_input_value[:-1]
                else:
                    if m == 0:
                        try:
                            int(Event.unicode)
                            user_input_value += Event.unicode
                        except ValueError:
                            pass
                    else:
                        user_input_value += Event.unicode
        Afficher()


def Add_up():
    global Map, Length, Width
    for i in range(Length):
        Map[i].insert(0, ['grass_1', '', '', False, ''])
    Width += 1


def Add_down():
    global Map, Length, Width
    for i in range(Length):
        Map[i].append(['grass_1', '', '', False, ''])
    Width += 1


def Add_left():
    global Map, Length, Width
    l = []
    for i in range(Width):
        l += [['grass_1', '', '', False, '']]
    Map.insert(0, l)
    Length += 1


def Add_right():
    global Map, Length, Width
    l = []
    for i in range(Width):
        l += [['grass_1', '', '', False, '']]
    Map.append(l)
    Length += 1


def Remove_up():
    global Map, Length, Width
    for i in range(Length):
        Map[i].pop(0)
    Width -= 1


def Remove_down():
    global Map, Length, Width
    for i in range(Length):
        Map[i].pop(-1)
    Width -= 1


def Remove_left():
    global Map, Length, Width
    Map.pop(0)
    Length -= 1


def Remove_right():
    global Map, Length, Width
    Map.pop(-1)
    Length -= 1


def Modify_size(l, r, u, d):
    global Length, Width
    if l > 0:
        for i in range(l):
            Add_left()
    if l < 0 and -l < Length:
        for i in range(-l):
            Remove_left()
    if r > 0:
        for i in range(r):
            Add_right()
    if r < 0 and -r < Length:
        for i in range(-r):
            Remove_right()
    if u > 0:
        for i in range(u):
            Add_up()
    if u < 0 and -u < Width:
        for i in range(-u):
            Remove_up()
    if d > 0:
        for i in range(d):
            Add_down()
    if d < 0 and -d < Width:
        for i in range(-d):
            Remove_down()


def Remove_line(index):
    global Map, Width
    i = int(index)
    if -1 < i < Width:
        for column in Map:
            column.pop(i)
    Width -= 1


def Remove_lines(index, ranges):
    for i in range(ranges):
        Remove_line(index)


def Remove_column(index):
    global Map, Length
    i = int(index)
    if -1 < i < Length:
        Map.pop(i)
    Length -= 1


def Remove_columns(index, ranges):
    for i in range(ranges):
        Remove_column(index)
