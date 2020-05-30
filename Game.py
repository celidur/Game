import pickle
import pygame
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


Map, Length, Width = import_map()
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((704, 704))
x, y, velocity, pressed = 48 * 64, 30 * 64, 10, {}
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


def Afficher_case(Block, x_case, y_case, move_x=0, move_y=0):
    Screen.blit(Block, (int((x_case + 5) * 64 - (x % 64)) + move_x, int((y_case + 5) * 64 - (y % 64) + move_y)))


def management_Screen(X1, X2, Y1, Y2, n, Block):
    for X_case in range(X1, (11 + 1) // 2 + X2):
        for Y_case in range(Y1, Y2):
            if 0 <= X_case + x // 64 < Length and y // 64 + Y_case >= 0 and Y_case + y // 64 < Width:
                if Map[x // 64 + X_case][y // 64 + Y_case][n] in Block:
                    if n == 4:
                        block_2 = Block[Map[x // 64 + X_case][y // 64 + Y_case][n]]
                        Afficher_case(block_2[0], X_case, Y_case, block_2[1], block_2[2])
                    else:
                        Afficher_case(Block[Map[x // 64 + X_case][y // 64 + Y_case][n]], X_case, Y_case)


def Afficher():
    global Width, Length, x, y
    Screen.blit(fond, (0, 0))
    management_Screen(-5, 3, -6, 7, 0, block)
    management_Screen(-5, 3, -6, 7, 1, block)
    management_Screen(-5, 3, -6, 7, 2, block)
    if Map[((x + 32) // 64)][((y + 32) // 64)][4] != "h1" and Map[((x + 32) // 64)][((y + 32) // 64) - 1][4] != "h1":
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
        management_Screen(-9, 8, -8, 12, 4, block2)
    else:
        management_Screen(-9, 8, -8, 12, 4, block2)
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
    pygame.display.flip()


def Keyboard_pressed(Pressed):
    global x, y, velocity
    move = False
    if Pressed.get(pygame.K_DOWN) and y // 64 < Width - 1:
        if not Map[((x + 32) // 64)][(y // 64) + 1][3]:
            y += velocity
            player.Move("down")
            move = True
    elif Pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
        if not Map[((x + 32) // 64)][(y // 64)][3]:
            y -= velocity
            player.Move("up")
            move = True
    if Pressed.get(pygame.K_RIGHT) and x // 64 < Length - 1:
        if not Map[(x // 64) + 1][(y + 32) // 64][3]:
            x += velocity
            if not move:
                player.Move("right")
    elif Pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
        if not Map[(x // 64)][(y + 32) // 64][3]:
            x -= velocity
            if not move:
                player.Move("left")
    elif not move:
        player.Move("same")
    Afficher()
