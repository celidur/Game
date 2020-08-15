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
map_collision = []
map_object = []
for i in Map:
    temp = []
    temp_2 = []
    for j in i:
        temp.append(j[3])
        temp_2.append(j[4])
    map_collision.append(temp)
    map_object.append(temp_2)
x, y, menu, temp = _[3], _[4], 0, time.time()
Settings = _[2]
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
nb_case = 0
end_ = True
map_chunk = []
volume = 0.5
pygame.mixer_music.load(music[area])
pygame.mixer_music.set_volume(volume)
fade = [False, volume, 0, 0]  # fade, volume, début, durée


def init_fight(index):
    global enemy_, texts, prog, enemy, fade, volume
    player.init()
    enemy_ = Enemy(enemy[index])
    texts = '{} sauvage apparaît.|{}'.format(enemy_.get_name()[0], Texts.select_action)
    prog = 2
    fade = [True, volume, time.time(), 1]


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
    global menu, frame, player, enemy_, fight_mode, debut_combat, pos_inventory, \
        temp, texts, fade
    if debut_combat:
        init_fight(chose_enemy())
        debut_combat = False
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if fight_mode == 3 and time.time() > temp + 1 / 7:
        if pressed.get(Settings[0]) or pressed.get(Settings[4]):
            pos_inventory = (
                ((pos_inventory[0] + 1) % 5),
                (pos_inventory[1] * 5 + pos_inventory[0] + 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                pos_inventory = (0, 0, 0)
        elif pressed.get(Settings[1]) or pressed.get(Settings[5]):
            pos_inventory = (
                (pos_inventory[1] * 5 + pos_inventory[0] - 1) % 5, (pos_inventory[1] * 5 + pos_inventory[0] - 1) // 5,
                pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                pos_inventory = (36 % 5 - 1, 4, 36 // 5 - 4)
        elif pressed.get(Settings[2]) or pressed.get(Settings[6]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] + 1, pos_inventory[2])
            if pos_inventory[1] >= 5:
                pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
            if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                pos_inventory = (pos_inventory[0], 0, 0)
        elif pressed.get(Settings[3]) or pressed.get(Settings[7]):
            pos_inventory = (pos_inventory[0], pos_inventory[1] - 1, pos_inventory[2])
            if pos_inventory[1] < 0:
                pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
            if pos_inventory[2] < 0:
                if pos_inventory[0] >= 36 % 5:
                    pos_inventory = (pos_inventory[0], 3, 36 // 5 - 4)
                else:
                    pos_inventory = (pos_inventory[0], 4, 36 // 5 - 4)
        temp = time.time()
    if fight_mode == -1 and not fade[0]:
        pygame.mixer_music.load(music['combat'])
        pygame.mixer_music.play(loops=-1)
        fight_mode = 0
        pygame.time.delay(500)
        Screen.blit(enemy_.get_background(), (0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)
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
    elif fight_mode == -1:
        # transition
        pass
    else:
        display.display_fight(enemy_.get_background(), enemy_.get_image(), enemy_.get_size(), enemy_.get_hp(),
                              enemy_.get_name(), player.get_stats(), pos_inventory)
    pygame.display.flip()


def game_play(pressed):
    global menu, temp, x, y, map_chunk, frame, x_y_generation, area, nb_case, debut_combat, \
        fight_mode, map_collision, fade
    while not time.time() > frame + 1 / 61:
        pass
    frame = time.time()
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 2, time.time() + 0.2
        return
    x, y = player.player_move(pressed, x, y, map_collision, Width, Length, Settings)
    display.display(map_chunk)
    if y // 64 == 31 and 45 <= x // 64 <= 50:
        if area != 'plain':
            if not fade[0]:
                fade = [True, volume, time.time(), 1]
            area = 'plain'
    elif y // 64 == 30 and 45 <= x // 64 <= 50:
        if area != 'village':
            if not fade[0]:
                fade = [True, volume, time.time(), 1]
            area = 'village'
    if (x // 64 != x_y_generation[0] or y // 64 != x_y_generation[1]) and area == 'plain':
        nb_case += 1
        x_y_generation = (x // 64, y // 64)
        if random.random() == nb_case * (2 + player.level / 100) / 5000:  # <=
            menu = 4
            nb_case = 0
            debut_combat = True
            fight_mode = -1


def game_menu(pressed):
    global menu, temp, map_chunk
    if pressed.get(pygame.K_ESCAPE) and time.time() > temp:
        menu, temp = 0, time.time() + 0.2
    display.display(map_chunk)


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
    for e in range(n):
        texts = texts.split('|')
        del texts[-1]
        texts = '|'.join(texts)


def attack_player(n, use=True):
    global prog, texts, fight_mode, end_
    env = 6
    if enemy_.get_name()[1] == Texts.plain:
        env = 1
    elif enemy_.get_name()[1] == Texts.desert:
        env = 2
    elif enemy_.get_name()[1] == Texts.snow:
        env = 3
    elif enemy_.get_name()[1] == Texts.forest:
        env = 4
    elif enemy_.get_name()[1] == Texts.mountain:
        env = 5

    if random.random() < player.get_crit()[0] and use:
        crit = player.get_crit()[1]
        add_text("Coup critique !!!", True, True)
    else:
        crit = 1
    damage = 0
    if n == 1:
        damage = 7 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                             player.get_equipment()[0].get_stat()[env]) / enemy_.get_defense()
    elif n == 2:
        damage = 2 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                             player.get_equipment()[0].get_stat()[env]) / enemy_.get_defense()
    elif n == 3:
        damage = 12 * crit * (player.get_stats()[4] + player.get_equipment()[0].get_stat()[0] +
                              player.get_equipment()[0].get_stat()[env]) / enemy_.get_defense()
    elif n == 4:
        damage = 7 * crit * ((player.get_stats()[4] + player.get_equipment()[0].get_stat()[0]) / 2 +
                             player.get_equipment()[0].get_stat()[env] * 5) / enemy_.get_defense()
    if use:
        remove_text()
        fight_mode = 0
        if n == 1:
            remove_text()
            enemy_.change_hp(-int(damage))
            add_text(
                "Vous frappez {} de votre épée et lui infligez {} dégats.".format(enemy_.get_name()[0], int(damage)),
                True, True)
        elif n == 2:
            remove_text()
            player.change_att_2(int(damage))
            add_text("Vous avez blessé {}. Il saigne.".format(enemy_.get_name()[0]), True, True)
        elif n == 3:
            remove_text()
            enemy_.change_hp(-int(damage))
            player.change_hp(-int(0.25 * damage / crit))
            add_text("Vous chargez {} et lui infligez {} dégats.".format(enemy_.get_name()[0], int(damage)), True, True)
            add_text(
                "Vous avez également été blessé par le choc. Vous subissez {} dégats.".format(
                    int(0.25 * damage / crit)), True, True)
        elif n == 4:
            if player.get_stats()[2] < 10:
                end_ = False
                add_text("Mana insuffisant." + ' ' +
                         "Sélectionnez un autre sort ou une autre action.")
                fight_mode = 1
            else:
                remove_text()
                enemy_.change_hp(-int(damage))
                add_text("Vous mobilisez votre attaque spéciale pour infliger {} dégats à {}.".format(int(damage),
                                                                                                      enemy_.get_name()[
                                                                                                          0]),
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
                add_text("Mana insuffisant." + ' ' +
                         "Sélectionnez un autre sort ou une autre action.")
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
            add_text("Mana insuffisant." + ' ' +
                     "Sélectionnez un autre sort ou une autre action.")
            fight_mode = 2
        else:
            player.change_mp(-10)
            player.change_protect(1.5)
    elif n == 3:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Mana insuffisant." + ' ' +
                     "Sélectionnez un autre sort ou une autre action.")
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
            add_text("Vous n'avez pas assez de Mana pour utiliser ce sort." + ' ' +
                     "Sélectionnez un autre sort ou une autre action.")
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
        for __ in range(len(player.att_2)):
            damage += player.att_2[__][0]
        enemy_.change_hp(-int(damage))
        add_text("L'ennemi souffre. Il subit {} dégats.".format(damage), True, True)
    n = player.turn_att_2()
    if n == 0:
        add_text("l'ennemi ne souffre plus.", True, True)
    elif n == 1:
        add_text("L'ennemi souffre de moins en moins.", True, True)
    player.change_protect()
    add_text(Texts.select_action)


def use_object(index_object, use=True):
    global fight_mode
    if use:
        fight_mode = 0
        player.inventory[1][index_object] -= 1
    if index_object == 0:
        return Texts.description_object[index_object][1].format(player.change_hp(10, use))
    elif index_object == 1:
        return Texts.description_object[index_object][1].format(player.change_hp(20, use))
    elif index_object == 2:
        return Texts.description_object[index_object][1].format(player.change_hp(50, use))
    elif index_object == 3:
        return Texts.description_object[index_object][1].format(player.change_hp(100, use))
    elif index_object == 4:
        return Texts.description_object[index_object][1].format(player.change_hp(player.hp_max, use))
    elif index_object == 5:
        return Texts.description_object[index_object][1].format(player.change_mp(10, use))
    elif index_object == 6:
        return Texts.description_object[index_object][1].format(player.change_mp(20, use))
    elif index_object == 7:
        return Texts.description_object[index_object][1].format(player.change_mp(50, use))
    elif index_object == 8:
        return Texts.description_object[index_object][1].format(player.change_mp(100, use))
    elif index_object == 9:
        return Texts.description_object[index_object][1].format(player.change_mp(player.mp_max, use))
    elif index_object == 10:  #
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 11:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 12:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 13:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 14:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 15:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 16:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 17:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 18:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 19:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 20:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 21:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 22:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 23:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 24:
        return Texts.description_object[index_object][1].format(0, 0)
    elif index_object == 25:
        return Texts.description_object[index_object][1]
    elif index_object == 26:
        return Texts.description_object[index_object][1]
    elif index_object == 27:
        return Texts.description_object[index_object][1]
    elif index_object == 28:
        return Texts.description_object[index_object][1]
    elif index_object == 29:
        return Texts.description_object[index_object][1]
    elif index_object == 30:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 31:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 32:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 33:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 34:
        return Texts.description_object[index_object][1].format(0)
    elif index_object == 35:
        return Texts.description_object[index_object][1].format(0)


def fadeout():
    global fade, volume
    if fade[0]:
        vol = fade[1] - ((time.time() - fade[2]) / fade[3]) * fade[1]
        if vol <= 0:
            fade = [False, volume, 0, 0]
            pygame.mixer_music.stop()
            pygame.mixer_music.set_volume(volume)
        else:
            pygame.mixer_music.set_volume(vol)
