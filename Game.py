from Variable import *
import time
from Display import Display
from Player import Player
import random
from Enemy import Enemy
_, Texts, button_exit, button_menu, button_magic, button_leave, button_inventory, button_attack, \
          button_save, button_pause, button_setting, button_attack1, button_attack2, button_attack4, button_attack3, \
          button_back, button_magic1, button_magic2, button_magic3, button_magic4, button_confirm, \
          button_use, enemy = import_language()
player = Player(_[0], _[1])
x, y, menu, temp = _[3], _[4], 0, time.time()
map_game = []
Settings = _[2]
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
enemy_ = Enemy(enemy[0])
change = True
debut_combat = True
texts = ''
pos_inventory = (0, 0, 0)
use_obj = False
prog = 1
x_y_generation = (x % 64, y % 64)
area = _[5]
nb_case = 0


def init_fight(index):
    global enemy_, texts, prog, enemy
    player.change_boost_att(False)
    player.change_boost_def(False)
    enemy_ = Enemy(enemy[index])
    texts = '{} sauvage apparaît.|{}'.format(enemy_.get_name()[0], Texts.select_action)
    prog = 2


def save():
    save_game = [player.get_stats(), player.get_inventory(), Settings, x, y, area]
    try:
        os.remove("save/save_game.txt")
    except FileNotFoundError:
        pass
    with open("save/save_game.txt", 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(save_game)


def game_fight(pressed):  # menu=4
    global menu, frame, player, enemy_, map_game, x_map_game, y_map_game, fight_mode, debut_combat, pos_inventory, \
        temp, texts
    if debut_combat:
        init_fight(chose_enemy())
        debut_combat = False
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if fight_mode == 3 and time.time() > temp + 1 / 5:
        if pressed.get(Settings[0]):
            pos_inventory = (
                ((pos_inventory[0] + 1) % 5),
                (pos_inventory[1] * 5 + pos_inventory[0] + 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                pos_inventory = (0, 0, 0)
        elif pressed.get(Settings[1]):
            pos_inventory = (
                (pos_inventory[1] * 5 + pos_inventory[0] - 1) % 5, (pos_inventory[1] * 5 + pos_inventory[0] - 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                pos_inventory = (36 % 5 - 1, 4, 36 // 5 - 4)
        elif pressed.get(Settings[2]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] + 1, pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                pos_inventory = (pos_inventory[0], 0, 0)
        elif pressed.get(Settings[3]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] - 1, pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                if pos_inventory[0] >= 36 % 5:
                    pos_inventory = (pos_inventory[0], 3, 36 // 5 - 4)
                else:
                    pos_inventory = (pos_inventory[0], 4, 36 // 5 - 4)
        temp = time.time()
    display.display_fight(enemy_.get_background(), enemy_.get_image(), enemy_.get_size(), enemy_.get_hp(),
                          enemy_.get_name(), player.get_stats(), pos_inventory)
    pygame.display.flip()


def game_play(pressed):
    global menu, temp, x, y, map_game, x_map_game, y_map_game, frame, x_y_generation, area, nb_case
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 2, time.time() + 0.2
        return
    x, y = player.player_move(pressed, x, y, map_game, Width, Length, Settings)
    map_game, x_map_game, y_map_game = update_map_game(x_map_game, y_map_game, x, y, Map, map_game)
    display.display(map_game)
    if y // 64 == 31 and 45 <= x // 64 <= 50:
        area = 'plain'
    elif y // 64 == 30 and 45 <= x // 64 <= 50:
        area = 'village'
    if (x // 64 != x_y_generation[0] or y // 64 != x_y_generation[1]) and area == 'plain':
        nb_case += 1
        x_y_generation = (x // 64, y // 64)
        if random.random() <= nb_case * (1 + player.level / 100) / 5000:
            menu = 4
            nb_case = 0


def game_menu(pressed):
    global menu, temp
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 0, time.time() + 0.2
    display.display(map_game)


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


def chose_enemy():
    global area
    if area == 'plain':
        return 0


def add_text(text, c=True):
    global texts, change
    texts = texts.split('|')
    texts.append(text)
    change = c
    texts = '|'.join(texts)
    if texts[0] == '|':
        texts = texts[1:]


def remove_text(n=1):
    global texts, change
    for i in range(n):
        texts = texts.split('|')
        del texts[-1]
        texts = '|'.join(texts)


def use_object(i, use=True):
    if use:
        player.inventory[1][i] -= 1
    if i == 0:
        return player.change_hp(10, use)
    elif i == 1:
        return player.change_hp(20, use)
    elif i == 2:
        return player.change_hp(50, use)
    elif i == 3:
        return player.change_hp(100, use)
    elif i == 4:
        return player.change_hp(player.hp_max, use)
    elif i == 5:
        return player.change_hm(10, use)
    elif i == 6:
        return player.change_hm(20, use)
    elif i == 7:
        return player.change_hm(50, use)
    elif i == 8:
        return player.change_hm(100, use)
    elif i == 9:
        return player.change_hm(player.hm_max, use)
    elif i == 10:
        pass
    elif i == 11:
        pass
    elif i == 12:
        pass
    elif i == 13:
        pass
    elif i == 14:
        pass
    elif i == 15:
        pass
    elif i == 16:
        pass
    elif i == 17:
        pass
    elif i == 18:
        pass
    elif i == 19:
        pass
    elif i == 20:
        pass
    elif i == 21:
        pass
    elif i == 22:
        pass
    elif i == 23:
        pass
    elif i == 24:
        pass
    elif i == 25:
        pass
