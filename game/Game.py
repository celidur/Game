from game.Variable import *
import time
import asyncio
import pygame
from game.Display import Display
from game.Player import Player
import random
from game.Enemy import Enemy
from game.Ennemy2 import Ennemy2
Texts, button_exit, button_menu, button_magic, button_leave, button_inventory, button_attack, \
       button_save, button_pause, button_setting, button_attack1, button_attack2, button_attack4, button_attack3, \
       button_back, button_magic1, button_magic2, button_magic3, button_magic4, button_confirm, \
       button_use, enemy = import_language()
_ = import_save()
nb_map = 0
if _:
    player = Player(_[0], _[1])
    x_t, y_t, menu, temp = _[3], _[4], 0, time.time()
    Settings = _[2]
    area = _[5]
    while len(x_t) < len(Map_t):
        x_t.append(0)
    while len(y_t) < len(Map_t):
        y_t.append(0)
    x_t[1]=47*64
    y_t[1]=47*64
    x, y = x_t[nb_map], y_t[nb_map]
    x_y_generation = (x_t[nb_map] % 64, y_t[nb_map] % 64)
Map, map_object, map_collision, Length, Width = [], [], [], 0, 0
display = Display(block, block2, size_window, background)
frame = 0
fight_mode = 0
enemy_ = Enemy(enemy[0])
change = True
debut_combat = True
texts = ''
pos_inventory = (0, 0, 0)
use_obj = False
prog = 1
nb_case = 0
end_ = True
volume = 0.5
fade = [False, volume, 0, 0]  # fade, volume, début, durée
game_chunk = []
list_coord = []
Map_chunk = []
pressed2 = {}
time_temp = time.time()
onclick, running, pressed, pos = False, True, {}, [0, 0]
ready = False
loading_text = "Creating a flat Earth"
loading_pos = [(0, -40), (-20, -35), (-35, -20), (-40, 0), (-35, 20), (-20, 35), (0, 40), (20, 35), (35, 20), (40, 0),
               (35, -20), (20, -35)]
font_ = pygame.font.Font("game/font/FRAMDCN.TTF", 16)
progress = 0
enemy_map = []
#for i in range(1000):
#    enemy_map.append(Ennemy2(3060, 2236))


def init_fight():
    global enemy_, texts, prog, enemy, fade, volume
    player.init()
    if area == 'plain':
        index = 0
    else:
        index = 0
    enemy_ = Enemy(enemy[index])
    texts = '{} sauvage apparaît.|{}'.format(enemy_.get_name()[0], Texts.select_action)
    prog = 2
    fade = [True, volume, time.time(), 3]


def save():
    save_game = [player.get_stats(), player.get_inventory(), Settings, x_t, y_t, area]
    try:
        with open('game/file/save', 'rb') as file:
            file = pickle.Unpickler(file)
            nb = file.load()
    except pickle.UnpicklingError:
        return False
    if not os.path.exists('game/save/{}'.format(nb)):
        os.makedirs('game/save/{}'.format(nb))
    with open('game/save/{}/save_game_'.format(nb), 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(save_game)
    try:
        os.remove('game/save/{}/save_game'.format(nb))
    except FileNotFoundError:
        pass
    os.rename('game/save/{}/save_game_'.format(nb), 'game/save/{}/save_game'.format(nb))


async def loading_animation(x_, y_):
    global ready, loading_pos, loading_text, font_, progress
    n = 0
    while not ready:
        Screen.blit(pygame.image.load("game/assets/temp/loading_background.png"), (0, 0))
        pygame.draw.rect(Screen, (0, 255, 0), [252, 650, int(progress * 200), 16])
        Screen.blit(font_.render('{} %'.format(int(progress * 100)), False, (255, 255, 255)),
                    (262 + int(progress * 200), 650))
        Screen.blit(font_.render(loading_text, False, (255, 255, 255)),
                    (352 - font_.size(loading_text)[0] // 2, 670))
        Screen.blit(font_.render('.' * (n // 3), False, (255, 255, 255)),
                    (352 + font_.size(loading_text)[0] // 2, 670))
        for z in range(12):
            Screen.blit(pygame.image.load("game/assets/icons/loading/{}.png".format((z + n) % 12)),
                        (loading_pos[z][0] + x_ - 9, loading_pos[z][1] + y_ - 9))
        pygame.display.flip()
        n += 1
        n %= 12
        await asyncio.sleep(1 / 12)


async def loading_map(a):
    global ready, loading_text, progress, Map_chunk
    for i in Map_t:
        map_split = []
        temp_ = []
        for lines in range((len(i) + 15) // 16):
            strip = []
            for columns in range((len(i[0]) + 15) // 16):
                mini_map = []
                for line in range(16):
                    mini_lines = []
                    for column in range(16):
                        if lines * 16 + line > len(i) - 1 or columns * 16 + column > len(i[0]) - 1:
                            mini_lines.append([None, None, None])
                        else:
                            mini_lines.append(i[lines * 16 + line][columns * 16 + column][:3])
                        await asyncio.sleep(0)
                    mini_map.append(mini_lines)
                strip.append(mini_map)
            map_split.append(strip)
        for x_chunk in range(len(map_split)):
            strip = []
            for y_chunk in range(len(map_split[0])):
                chunk = pygame.Surface((16 * 64, 16 * 64), pygame.SRCALPHA, 32)
                for x_temp in range(16):
                    progress = (((y_chunk + (x_temp / 16)) / len(map_split[0])) + x_chunk) / len(map_split)
                    for y_temp in range(16):
                        for layer in range(3):
                            try:
                                chunk.blit(block[map_split[x_chunk][y_chunk][x_temp][y_temp][layer]],
                                           (x_temp * 64, y_temp * 64))
                            except KeyError:
                                continue
                        await asyncio.sleep(0)
                strip.append(chunk)
            temp_.append(strip)
        Map_chunk.append(temp_)
    if a:
        loading_text = "Shuffling random numbers"
        progress = 0
        for i_1 in range(4 * 1024):
            for j2 in range(1024):
                list_coord.append((i_1 // 1024, i_1 % 1024, j2))
            await asyncio.sleep(0)
        for i_1 in reversed(range(1, len(list_coord))):
            j2 = int(random.random() * (i_1 + 1))
            list_coord[i_1], list_coord[j2] = list_coord[j2], list_coord[i_1]
            if i_1 % 1024 == 0:
                progress = 1 - i_1 / (4 * 1024 * 1024)
                await asyncio.sleep(0)
        progress = 1
        try:
            os.remove("game/file/temp")
        except FileNotFoundError:
            pass
        await asyncio.sleep(0)
        with open("game/file/temp", 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(list_coord)
    await asyncio.sleep(0.5)
    ready = True
    pygame.mixer_music.load(music[area])
    pygame.mixer_music.set_volume(volume)
    pygame.mixer_music.play(loops=-1)


async def prepare_map(a=True):
    t1 = asyncio.create_task(loading_animation(352, 580))
    t2 = asyncio.create_task(loading_map(a))
    await asyncio.gather(t1, t2)


def running_game():
    global running, onclick, pos, time_temp, menu, fight_mode, pos_inventory, prog, end_, pressed, fade, frame, \
        player, enemy_, debut_combat, temp, texts, area, x_y_generation, x, y, nb_case, map_chunk, pressed2, \
        list_coord, ready, x_t, y_t, Map, map_object, map_collision, Length, Width, nb_map
    if not _:
        return 1
    while not ready:
        v = import_temp()
        if v:
            list_coord = v
            asyncio.run(prepare_map(False))
        else:
            asyncio.run(prepare_map())
    fadeout()
    Map, map_object, map_collision, Length, Width = Map_t[nb_map], map_object_t[nb_map], map_collision_t[nb_map], \
                                                    Length_t[nb_map], Width_t[nb_map]
    x, y = x_t[nb_map], y_t[nb_map]
    map_chunk = Map_chunk[nb_map]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if menu != 5:
                running = False
                return False
        elif event.type == pygame.KEYDOWN:
            pressed[event.key] = True
            pressed2[event.key] = True
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            onclick = True
            pos = pygame.mouse.get_pos()
    if pressed2.get(pygame.K_KP_PLUS):
        nb_map = (nb_map+1) % len(Map_t)
        Map, map_object, map_collision, Length, Width = Map_t[nb_map], map_object_t[nb_map], map_collision_t[nb_map], \
                                                        Length_t[nb_map], Width_t[nb_map]
        x, y = x_t[nb_map], y_t[nb_map]
        map_chunk = Map_chunk[nb_map]
    if menu == 0:
        for enemy__ in enemy_map:
            enemy__.enemy_move(map_collision, Width, Length, x, y)
        for projectile in player.all_projectiles:
            projectile.mov()
        if onclick:
            if button_menu.button_clicked(pos[0], pos[1]):
                menu = 2
            elif button_shop.button_clicked(pos[0], pos[1]) and area == 'village':
                pass
            # ajouter test bouton iventaire
        else:
            while not time.time() > frame + 1 / 61:
                pass
            frame = time.time()
            if pressed2.get(pygame.K_ESCAPE):
                menu = 2
            elif pressed2.get(pygame.K_SPACE):
                player.launch_projectile()
            x, y = player.player_move(pressed, x, y, map_collision, Width, Length, Settings)
            x_t[nb_map], y_t[nb_map] = x, y
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
                    nb_case = 0
            if (x // 64 != x_y_generation[0] or y // 64 != x_y_generation[1]) and area == 'plain':
                nb_case += 1
                x_y_generation = (x // 64, y // 64)
                if random.random() == nb_case * (2 + player.level / 100) / 5000:  # <=
                    menu = 4
                    nb_case = 0
                    debut_combat = True
                    fight_mode = -2
    elif menu == 1:
        pass  # mode inventaire
    elif menu == 2:  # mode pause
        if onclick:
            if button_pause.button_clicked(pos[0], pos[1]):
                menu = 0
            elif button_exit.button_clicked(pos[0], pos[1]):
                running = False
                return False
            elif button_save.button_clicked(pos[0], pos[1]):
                save()
            elif button_setting.button_clicked(pos[0], pos[1]):
                pass
        else:
            if pressed2.get(pygame.K_ESCAPE):
                menu = 0
            display.display(map_chunk)
    elif menu == 3:  # menu shop
        pass
    elif menu == 4:
        end_ = True
        if onclick:
            if fight_mode == 0:
                if button_attack.button_clicked(pos[0], pos[1]):
                    fight_mode = 1
                    add_text(Texts.select_attack)
                    prog = 1
                elif button_magic.button_clicked(pos[0], pos[1]):
                    fight_mode = 2
                    add_text(Texts.select_spell)
                    prog = 1
                elif button_inventory.button_clicked(pos[0], pos[1]):
                    fight_mode = 3
                    add_text(Texts.select_object)
                    prog = 1
                    pos_inventory = (0, 0, 0)
                elif button_leave.button_clicked(pos[0], pos[1]):
                    fight_mode = 4
            elif fight_mode == 1 or fight_mode == 2:
                if button_back.button_clicked(pos[0], pos[1]):
                    fight_mode = 0
                    remove_text()
                elif fight_mode == 1:
                    if button_attack1.button_clicked(pos[0], pos[1]):
                        attack_player(1)
                        end_turn()
                    elif button_attack2.button_clicked(pos[0], pos[1]):
                        attack_player(2)
                        end_turn()
                    elif button_attack3.button_clicked(pos[0], pos[1]):
                        attack_player(3)
                        end_turn()
                    elif button_attack4.button_clicked(pos[0], pos[1]):
                        attack_player(4)
                        end_turn()
                else:
                    if button_magic1.button_clicked(pos[0], pos[1]):
                        magic_player(1)
                        end_turn()
                    elif button_magic2.button_clicked(pos[0], pos[1]):
                        magic_player(2)
                        end_turn()
                    elif button_magic3.button_clicked(pos[0], pos[1]):
                        magic_player(3)
                        end_turn()
                    elif button_magic4.button_clicked(pos[0], pos[1]):
                        magic_player(4)
                        end_turn()
            elif fight_mode == 3:
                if button_back.button_clicked(pos[0], pos[1], 280, 670):
                    fight_mode = 0
                    remove_text()
                elif button_use.button_clicked(pos[0], pos[1]) and use_obj:
                    remove_text(2)
                    add_text(
                        use_object((pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0]),
                        True, True)
                    end_turn()
            elif fight_mode == 4:
                if button_back.button_clicked(pos[0], pos[1], 433, 348):
                    fight_mode = 0
                elif button_confirm.button_clicked(pos[0], pos[1]):
                    fight_mode = 0
                    fade = [True, volume, time.time(), 1]
                    menu = 0
        elif pressed2.get(pygame.K_ESCAPE):
            if fight_mode != 0:
                if fight_mode != 4:
                    remove_text()
                fight_mode = 0
            else:
                fight_mode = 4
        elif pressed2.get(pygame.K_RETURN) and fight_mode == 4:
            fight_mode = 0
            fade = [True, volume, time.time(), 1]
            menu = 0
        if debut_combat:
            init_fight()
            debut_combat = False
        while not time.time() > frame + 1 / 61:
            pass
        frame = time.time()
        if fight_mode == 3:
            if ((pressed.get(Settings[0]) or pressed.get(Settings[4])) and time.time() > temp + 1 / 7) or \
                    pressed2.get(Settings[0]) or pressed2.get(Settings[4]):
                pos_inventory = (
                    ((pos_inventory[0] + 1) % 5),
                    (pos_inventory[1] * 5 + pos_inventory[0] + 1) // 5,
                    pos_inventory[2])
                if pos_inventory[1] >= 5:
                    pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
                if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                    pos_inventory = (0, 0, 0)
                temp = time.time()
            elif ((pressed.get(Settings[1]) or pressed.get(Settings[5])) and time.time() > temp + 1 / 7) or \
                    pressed2.get(Settings[0]) or pressed2.get(Settings[4]):
                pos_inventory = (
                    (pos_inventory[1] * 5 + pos_inventory[0] - 1) % 5,
                    (pos_inventory[1] * 5 + pos_inventory[0] - 1) // 5,
                    pos_inventory[2])
                if pos_inventory[1] < 0:
                    pos_inventory = (pos_inventory[0], 0, pos_inventory[2] - 1)
                if pos_inventory[2] < 0:
                    pos_inventory = (36 % 5 - 1, 4, 36 // 5 - 4)
                temp = time.time()
            elif ((pressed.get(Settings[2]) or pressed.get(Settings[6])) and time.time() > temp + 1 / 7) or \
                    pressed2.get(Settings[0]) or pressed2.get(Settings[4]):
                pos_inventory = (pos_inventory[0], pos_inventory[1] + 1, pos_inventory[2])
                if pos_inventory[1] >= 5:
                    pos_inventory = (pos_inventory[0], 4, pos_inventory[2] + 1)
                if (pos_inventory[1] + pos_inventory[2]) * 5 + pos_inventory[0] >= 36:
                    pos_inventory = (pos_inventory[0], 0, 0)
                temp = time.time()
            elif ((pressed.get(Settings[3]) or pressed.get(Settings[7])) and time.time() > temp + 1 / 7) or \
                    pressed2.get(Settings[0]) or pressed2.get(Settings[4]):
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
    onclick, pressed2 = False, {}
    if menu != 4:
        fight_mode = 0
    return True


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

    if random.random() != player.get_crit()[0] and use:  # <
        crit = player.get_crit()[1]
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
            if crit != 1:
                add_text("Coup critique !", True, True)
            enemy_.change_hp(-int(damage))
            add_text(
                "Vous frappez {} de votre épée et lui infligez {} dégats.".format(enemy_.get_name()[0], int(damage)),
                True, True)
        elif n == 2:
            remove_text()
            if crit != 1:
                add_text("Coup critique !", True, True)
            player.change_att_2(int(damage))
            add_text("Vous avez blessé {}. Il saigne.".format(enemy_.get_name()[0]), True, True)
        elif n == 3:
            remove_text()
            if crit != 1:
                add_text("Coup critique !", True, True)
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
                if crit != 1:
                    add_text("Coup critique !", True, True)
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
        heal = player.change_hp(0.2 * player.get_stats()[1], False)
        if use:
            if player.get_stats()[2] < 10:
                end_ = False
                add_text("Mana insuffisant." + ' ' +
                         "Sélectionnez autre action.")
                fight_mode = 2
            elif player.get_stats()[0] == player.get_stats()[1]:
                end_ = False
                add_text("Vous avez déjà tous vos PV." + ' ' + "Sélectionnez une autre action.")
            else:
                remove_text()
                player.change_mp(-10)
                player.change_hp(0.2 * player.get_stats()[1])
                if player.get_stats()[0] == player.get_stats()[1]:
                    add_text("PV entièrement régénérés.", True, True)
                else:
                    add_text("{} PV régénérés.".format(heal - player.get_stats()[0]), True, True)

        else:
            return heal
    elif n == 2:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Mana insuffisant." + ' ' +
                     "Sélectionnez une autre action.")
            fight_mode = 2
        else:
            player.change_mp(-10)
            player.change_protect(1.5)
            add_text("Vous formez un bouclier magique de force {} autour de vous pour vous protéger.".format(1.5),
                     True, True)
    elif n == 3:
        if player.get_stats()[2] < 10:
            end_ = False
            add_text("Mana insuffisant." + ' ' +
                     "Sélectionnez une autre action.")
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
                     "Sélectionnez une autre action.")
            fight_mode = 2
        else:
            player.change_boost_att(0, 0.15)
            add_text('Votre attaque de base est désormais multipliée par {}.'.format(player.get_boost_stats()[0][0]),
                     True,
                     True)
            if player.get_boost_stats()[0][0] == 1.3:
                add_text('Votre attaque de base est boostée à son maximum. (×1.3)', True, True)


def end_turn():
    global end_, prog, enemy_
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
    v = enemy_.chose_attack_enemy()
    if v == 0:
        hp = enemy_.get_hp()[0]
        enemy_.attack_enemy(v)
        add_text("L'ennemi se soigne et récupère {} PV.".format(enemy_.get_hp()[0] - hp), True, True)
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
            if fight_mode != 0:
                pygame.mixer_music.load(music['combat'])
                pygame.mixer_music.play(loops=-1)
            else:
                pygame.mixer_music.load(music[area])
                pygame.mixer_music.play(loops=-1)
        else:
            pygame.mixer_music.set_volume(vol)
