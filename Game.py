from Enemy1 import Enemy1
from Variable import *
import time
from Display import Display
from Player import Player

Settings, Texts, button_exit, button_menu, button_magic, button_leave, button_inventory, button_attack, \
           button_save, button_pause, button_setting, button_attack1, button_attack2, button_attack4, button_attack3, \
           button_back, button_magic1, button_magic2, button_magic3, button_magic4, button_confirm, \
           button_use = import_language()
player = Player()
x, y, menu, temp = 48 * 64, 30 * 64, 4, time.time()
map_game = []
for X_case in range((x + 32) // 64 - 8, (x + 32) // 64 + 9):
    list1 = []
    for Y_case in range((y + 32) // 64 - 8, (y + 32) // 64 + 14):
        if 0 <= X_case < Length and 0 <= Y_case < Width:
            list1.append(Map[X_case][Y_case])
        else:
            list1.append(None)
    map_game.append(list1[:])
x_map_game = (x + 32) // 64
y_map_game = (y + 32) // 64
display = Display(block, block2, Width, Length, size_window, background, Map)
frame = 0
fight_mode = 0
enemy1 = Enemy1()
change = True
debut_combat = True
texts = ''
pos_inventory = (0, 0, 0)
use_ = [False, None]


def init_fight(enemy):
    global enemy1, texts
    if enemy == "enemy1":
        enemy1 = Enemy1()
    texts = ''


def save():
    pass


def game_fight(pressed):  # menu=4
    global menu, frame, player, enemy1, map_game, x_map_game, y_map_game, fight_mode, debut_combat, pos_inventory, temp
    if debut_combat:
        init_fight('enemy1')
        debut_combat = False
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if fight_mode == 3 and time.time() > temp + 1 / 3:
        if pressed.get(Settings[0]):
            pos_inventory = (
                int((pos_inventory[1] * 5 + pos_inventory[0] + 1) % 5),
                (pos_inventory[1] * 5 + pos_inventory[0] + 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 52:
                pos_inventory = (0, 0, 0)
        elif pressed.get(Settings[1]):
            pos_inventory = (
                (pos_inventory[1] * 5 + pos_inventory[0] - 1) % 5, (pos_inventory[1] * 5 + pos_inventory[0] - 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                pos_inventory = (52 % 5 - 1, 4, 52 // 5 - 4)
        elif pressed.get(Settings[2]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] + 1, pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 52:
                pos_inventory = (pos_inventory[0], 0, 0)
        elif pressed.get(Settings[3]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] - 1, pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                if pos_inventory[0] >= 52 % 5:
                    pos_inventory = (pos_inventory[0], 3, 52 // 5 - 4)
                else:
                    pos_inventory = (pos_inventory[0], 4, 52 // 5 - 4)
        temp = time.time()
    display.display_fight(enemy1.get_background(), enemy1.get_image(), enemy1.get_size(), enemy1.get_hp(),
                          enemy1.get_name(), player.get_stats(), pos_inventory, change, text='hey')
    pygame.display.flip()


def game_play(pressed):
    global menu, temp, x, y, map_game, x_map_game, y_map_game, frame
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 1, time.time() + 0.2
        return
    x, y = player.player_move(pressed, x, y, map_game, Width, Length)
    map_game, x_map_game, y_map_game = update_map_game(x_map_game, y_map_game, x, y, Map, map_game)
    display.display(map_game)


def game_menu(pressed):
    global menu, temp
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 0, time.time() + 0.2


def update_map_game(x_map, y_map, x_player, y_player, map_full, map_game_update):
    while (x_player + 32) // 64 < x_map:
        del map_game_update[-1]
        temp2 = []
        if x_map - 9 >= 0:
            for y_case in range(y_map - 8, y_map + 14):
                if 0 <= y_case < Width:
                    temp2.append(map_full[x_map - 9][y_case])
                else:
                    temp2.append(None)
        else:
            for i in range(22):
                temp2.append(None)
        map_game_update.insert(0, temp2[:])
        x_map -= 1

    while (x_player + 32) // 64 > x_map:
        del map_game_update[0]
        temp2 = []
        if x_map + 9 < Length:
            for y_case in range(y_map - 8, y_map + 14):
                if 0 <= y_case < Width:
                    temp2.append(map_full[x_map + 9][y_case])
                else:
                    temp2.append(None)
        else:
            for i in range(22):
                temp2.append(None)
        map_game_update.append(temp2[:])
        x_map += 1

    while (y_player + 32) // 64 < y_map:
        for col in map_game_update:
            del col[-1]
        if y_map - 9 >= 0:
            for x_case in range(x_map - 8, x_map + 9):
                if 0 <= x_case < Length:
                    case = map_full[x_case][y_map - 9]
                else:
                    case = None
                map_game_update[x_case - x_map + 8].insert(0, case)
        else:
            for i in range(17):
                map_game_update[i].insert(0, None)
        y_map -= 1

    while (y_player + 32) // 64 > y_map:
        for col in map_game_update:
            del col[0]
        if y_map + 14 < Width:
            for x_case in range(x_map - 8, x_map + 9):
                if 0 <= x_case < Length:
                    case = map_full[x_case][y_map + 14]
                else:
                    case = None
                map_game_update[x_case - x_map + 8].append(case)
        else:
            for i in range(17):
                map_game_update[i].append(None)
        y_map += 1

    return map_game_update, x_map, y_map
