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
fight_mode = -1
enemy_ = Enemy(enemy[0])
change = True
debut_combat = True
texts = ''
pos_inventory = (0, 0, 0)
use_obj = False
prog = 1
x_y_generation = (x % 64, y % 64)
area = _[5]
map_ = []
nb_case = 0
end_ = True


def init_fight(index):
    global enemy_, texts, prog, enemy
    player.init()
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
        temp, texts, map_game
    if debut_combat:
        init_fight(chose_enemy())
        debut_combat = False
    while not time.time() > frame + 1 / 90:
        pass
    frame = time.time()
    if fight_mode == 3 and time.time() > temp + 1 / 7:
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
    if fight_mode == -1:
        display.display(map_, enemy_.get_background())
        case_ = random.randint(0, 17 * 22 - 1)
        while map_[(case_ // 22) % 17][case_ % 22] is None:
            if map_ == [[None] * 22] * 17:
                fight_mode = 0
                time.sleep(0.5)
                Screen.blit(enemy_.get_background(), (0, 0))
                pygame.display.flip()
                time.sleep(1)
                Screen.blit(enemy_.get_image(), enemy_.get_size())
                Screen.blit(display.arial.render(enemy_.get_name()[0], False, display.colors[enemy_.get_name()[1]]),
                            (65, 357))
                Screen.blit(display.arial.render("{}/{}".format(enemy_.get_hp()[0], enemy_.get_hp()[1]), False,
                                                 (255, 255, 255)), (215, 357))
                pygame.display.flip()
                time.sleep(0.5)
                button_attack.display_button()
                pygame.display.flip()
                time.sleep(0.5)
                button_magic.display_button()
                pygame.display.flip()
                time.sleep(0.5)
                button_inventory.display_button()
                pygame.display.flip()
                time.sleep(0.5)
                button_leave.display_button()
                pygame.display.flip()
                time.sleep(0.5)
                Screen.blit(display.arial.render(
                    "{} : {}/{}  {} : {}/{}".format(Texts.hp, player.get_stats()[0], player.get_stats()[1], Texts.mp,
                                                    player.get_stats()[2], player.get_stats()[3]), False,
                    (255, 255, 255)), (430, 357))
                pygame.display.flip()
                time.sleep(0.5)
                Screen.blit(display.arial.render("{}   {}".format(Texts.attack_stat, Texts.defense_stat), False,
                                                 (255, 255, 255)), (530, 420))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render("Base", False, (255, 255, 255)), (430, 460))
                Screen.blit(
                    display.arial.render(str(player.get_stats()[4] + player.get_equipment()[0].get_stat()[0]), False,
                                         (255, 255, 255)),
                    (585 - len(str(player.get_stats()[4] + player.get_equipment()[0].get_stat()[0])) * 8, 460))
                Screen.blit(
                    display.arial.render(str(player.get_stats()[5] + player.get_equipment()[1].get_stat()[0]), False,
                                         (255, 255, 255)),
                    (665 - len(str(player.get_stats()[5] + player.get_equipment()[1].get_stat()[0])) * 8, 460))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.plain, False, (68, 255, 0)), (430, 500))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[1]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[6]) + '+') * 8, 500))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[1]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[6]) + '+') * 8, 500))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.desert, False, (249, 210, 39)), (430, 530))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[2]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[2]) + '+') * 8, 530))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[2]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[2]) + '+') * 8, 530))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.snow, False, (152, 249, 219)), (430, 560))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[3]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[1]) + '+') * 8, 560))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[3]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[1]) + '+') * 8, 560))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.forest, False, (11, 109, 13)), (430, 590))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[4]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[3]) + '+') * 8, 590))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[4]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[3]) + '+') * 8, 590))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.mountain, False, (123, 95, 62)), (430, 620))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[5]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[5]) + '+') * 8, 620))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[5]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[5]) + '+') * 8, 620))
                pygame.display.flip()
                time.sleep(0.2)
                Screen.blit(display.arial.render(Texts.volcano, False, (163, 41, 18)), (430, 650))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[0].get_stat()[6]), False, (255, 255, 255)),
                    (585 - len(str(player.get_equipment()[0].get_stat()[4]) + '+') * 8, 650))
                Screen.blit(
                    display.arial.render('+' + str(player.get_equipment()[1].get_stat()[6]), False, (255, 255, 255)),
                    (665 - len(str(player.get_equipment()[1].get_stat()[4]) + '+') * 8, 650))
                pygame.display.flip()
                time.sleep(0.5)
                break
            case_ += 1
        map_[(case_ // 22) % 17][case_ % 22] = None

    else:
        display.display_fight(enemy_.get_background(), enemy_.get_image(), enemy_.get_size(), enemy_.get_hp(),
                              enemy_.get_name(), player.get_stats(), pos_inventory)
    pygame.display.flip()


def game_play(pressed):
    global menu, temp, x, y, map_game, x_map_game, y_map_game, frame, x_y_generation, area, nb_case, debut_combat, \
        fight_mode, map_
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
        if random.random() != nb_case * (2 + player.level / 100) / 5000:  # <=
            menu = 4
            nb_case = 0
            debut_combat = True
            fight_mode = -1
            map_ = []
            for i in map_game:
                temp2 = []
                for j in i:
                    temp2.append(j)
                map_.append(temp2)


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


def add_text(text, c=True, add=False):
    global texts, change, prog
    texts = texts.split('|')
    texts.append(text)
    change = c
    texts = '|'.join(texts)
    if add:
        prog += 1
    if texts[0] == '|':
        texts = texts[1:]


def remove_text(n=1):
    global texts, change
    for i in range(n):
        texts = texts.split('|')
        del texts[-1]
        texts = '|'.join(texts)


def attack_player(n, use=True):
    global prog, texts, fight_mode
    i = 6
    if enemy_.get_name()[1] == Texts.plain:
        i = 1
    elif enemy_.get_name()[1] == Texts.desert:
        i = 2
    elif enemy_.get_name()[1] == Texts.snow:
        i = 3
    elif enemy_.get_name()[1] == Texts.forest:
        i = 4
    elif enemy_.get_name()[1] == Texts.mountain:
        i = 5

    if random.random() < player.get_crit()[0] and use:
        crit = player.get_crit()[1]
        add_text("Coup critique !!!", True, True)
    else:
        crit = 1
    damage = 0
    if n == 1:
        damage = 7 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                             player.get_equipment()[0].get_stat()[i]) / enemy_.get_defense()
    elif n == 2:
        damage = 2 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                             player.get_equipment()[0].get_stat()[i]) / enemy_.get_defense()
    elif n == 3:
        damage = 10 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                              player.get_equipment()[0].get_stat()[i]) / enemy_.get_defense()
    elif n == 4:
        damage = 7 * crit * ((player.get_stats()[4] + player.get_equipment()[0].get_stat()[0]) / 2 +
                             player.get_equipment()[0].get_stat()[i] * 5) / enemy_.get_defense()
    if use:
        remove_text(2)
        fight_mode = 0
        if n == 1:
            enemy_.change_hp(-int(damage))
            add_text(
                "Vous frappez {} de votre épée et lui infligez {} dégats.".format(enemy_.get_name()[0], int(damage)),
                True, True)
        elif n == 2:
            player.change_att_2(int(damage))
            add_text("Vous avez blessé {}. Il saigne.".format(enemy_.get_name()[0]), True, True)
        elif n == 3:
            enemy_.change_hp(-int(damage))
            player.change_hp(-int(0.3 * damage / crit))
            add_text("Vous chargez {} et lui infligez {} dégats.".format(enemy_.get_name()[0], int(damage)), True, True)
            add_text(
                "Vous avez également été blessé par le choc. Vous subissez {} dégats.".format(int(0.3 * damage / crit)),
                True, True)
        elif n == 4:
            enemy_.change_hp(-int(damage))
            add_text("Vous mobilisez votre attaque spéciale pour infliger {} dégats à {}.".format(int(damage),
                                                                                                  enemy_.get_name()[0]),
                     True, True)
    else:
        return int(damage)


def magic_player(n, use=True):
    global end_, texts, fight_mode
    if use:
        remove_text()
        fight_mode = 0
    if n == 1:
        player.change_hp(0.2 * player.get_stats()[1], use)
        heal = player.change_hp(0.2 * player.get_stats()[1], False)
        if use:
            if player.get_stats()[2] < 10:
                end_ = False
                add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' + "Sélectionnez un autre sort ou une autre action.")
                fight_mode = 2
            elif player.get_stats()[0] == player.get_stats()[1]:
                end_ = False
                add_text("Vous avez déjà tous vos PV." + ' ' + "Sélectionnez un autre sort ou une autre action.")
            else:
                remove_text()
                player.change_mp(-10)
                player.change_hp(0.2 * player.get_stats()[1])
                if player.get_stats()[0] == player.get_stats()[1]:
                    add_text("PV entièrement régénérés.", True, True)
                else:
                    add_text("{} PV régénérés.".format(heal), True, True)

        else:
            return heal
    elif n == 2:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' + "Sélectionnez un autre sort ou une autre action.")
            fight_mode = 2
        else:
            player.change_mp(-10)
            player.change_protect(1.5)
    elif n == 3:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' + "Sélectionnez un autre sort ou une autre action.")
            fight_mode = 2
        else:
            player.change_boost_def(0, 0.15)
            add_text('Votre défense de base est désormais multipliée par {}.'.format(player.get_boost_stats()[1][0]),
                     True,
                     True)
            if player.get_boost_stats()[1][0] == 1.3:
                add_text('Votre défense de base est boostée à son maximum. (×1.3)', True, True)
    elif n == 4:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' + "Sélectionnez un autre sort ou une autre action.")
            fight_mode = 2
        else:
            player.change_boost_att(0, 0.15)
            add_text('Votre attaque de base est désormais multipliée par {}.'.format(player.get_boost_stats()[0][0]),
                     True,
                     True)
            if player.get_boost_stats()[0][0] == 1.3:
                add_text('Votre attaque de base est boostée à son maximum. (×1.3)', True, True)


def end_turn():
    global end_, prog
    if not end_:
        return None
    if player.att_2:
        damage = 0
        for i in range(len(player.att_2)):
            damage += player.att_2[i][0]
        enemy_.change_hp(-int(damage))
        add_text("L'ennemi souffre. Il subit {} dégats.".format(damage), True, True)
    n = player.turn_att_2()
    if n == 0:
        add_text("l'ennemi ne souffre plus.", True, True)
    elif n == 1:
        add_text("L'ennemi souffre de moins en moins.", True, True)
    player.change_protect()
    add_text(Texts.select_action)


def use_object(i, use=True):
    global fight_mode
    if use:
        fight_mode = 0
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
        return player.change_mp(10, use)
    elif i == 6:
        return player.change_mp(20, use)
    elif i == 7:
        return player.change_mp(50, use)
    elif i == 8:
        return player.change_mp(100, use)
    elif i == 9:
        return player.change_mp(player.mp_max, use)
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
