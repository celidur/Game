import time
import asyncio
import Game
import pygame

temp = time.time()
onclick, running, pressed, pos = False, True, {}, [0, 0]
ready = False
loading_pos = [(0, -40), (-20, -35), (-35, -20), (-40, 0), (-35, 20), (-20, 35), (0, 40), (20, 35), (35, 20), (40, 0),
               (35, -20), (20, -35)]


async def loading_animation(x, y):
    global ready, loading_pos
    n = 0
    while not ready:
        Game.Screen.blit(pygame.image.load("assets/temp/loading_background.png"), (0, 0))
        for i in range(12):
            Game.Screen.blit(pygame.image.load("assets/icons/loading/{}.png".format((i + n) % 12)),
                             (loading_pos[i][0] + x, loading_pos[i][1] + y))
        pygame.display.flip()
        n += 1
        n %= 12
        await asyncio.sleep(1 / 12)


async def loading_map():
    global ready
    map_split = []
    for lines in range((len(Game.Map) + 15) // 16):
        strip = []
        for columns in range((len(Game.Map[0]) + 15) // 16):
            mini_map = []
            for line in range(16):
                mini_lines = []
                for column in range(16):
                    if lines * 16 + line > len(Game.Map) - 1 or columns * 16 + column > len(Game.Map[0]) - 1:
                        mini_lines.append([None, None, None])
                    else:
                        mini_lines.append(Game.Map[lines * 16 + line][columns * 16 + column][:3])
                    await asyncio.sleep(0)
                mini_map.append(mini_lines)
            strip.append(mini_map)
        map_split.append(strip)
    for x_chunk in range(len(map_split)):
        strip = []
        for y_chunk in range(len(map_split[0])):
            chunk = pygame.Surface((16 * 64, 16 * 64))
            for x in range(16):
                for y in range(16):
                    for layer in range(3):
                        try:
                            chunk.blit(Game.block[map_split[x_chunk][y_chunk][x][y][layer]], (x * 64, y * 64))
                        except KeyError:
                            continue
                    await asyncio.sleep(0)
            strip.append(chunk)
        Game.map_chunk.append(strip)
    ready = True


async def prepare_map():
    t1 = asyncio.create_task(loading_animation(352, 600))
    t2 = asyncio.create_task(loading_map())
    await asyncio.gather(t1, t2)


while running:
    while not ready:
        asyncio.run(prepare_map())
    Game.fadeout()
    if not pygame.mixer_music.get_busy():
        pygame.mixer_music.load(Game.music[Game.area])
        pygame.mixer_music.play(loops=-1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if Game.menu != 5:
                running = False
                continue
        elif event.type == pygame.KEYDOWN:
            pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            onclick = True
            pos = pygame.mouse.get_pos()
    if Game.menu == 0:
        if onclick:
            if Game.button_menu.button_clicked(pos[0], pos[1]):
                Game.menu = 2
            elif Game.button_shop.button_clicked(pos[0], pos[1]):
                pass
        else:
            Game.game_play(pressed)
    elif Game.menu == 1:
        pass
    elif Game.menu == 2:
        if onclick:
            if Game.button_pause.button_clicked(pos[0], pos[1]):
                Game.menu = 0
            elif Game.button_exit.button_clicked(pos[0], pos[1]):
                running = False
                continue
            elif Game.button_save.button_clicked(pos[0], pos[1]):
                Game.save()
            elif Game.button_setting.button_clicked(pos[0], pos[1]):
                pass
        else:
            Game.game_menu(pressed)
    elif Game.menu == 4:
        Game.end_ = True
        if onclick:
            if Game.fight_mode == 0:
                if Game.button_attack.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 1
                    Game.add_text(Game.Texts.select_attack)
                    Game.prog = 1
                elif Game.button_magic.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 2
                    Game.add_text(Game.Texts.select_spell)
                    Game.prog = 1
                elif Game.button_inventory.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 3
                    Game.add_text(Game.Texts.select_object)
                    Game.prog = 1
                    Game.pos_inventory = (0, 0, 0)
                elif Game.button_leave.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 4
            elif Game.fight_mode == 1 or Game.fight_mode == 2:
                if Game.button_back.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 0
                    Game.remove_text()
                elif Game.fight_mode == 1:
                    if Game.button_attack1.button_clicked(pos[0], pos[1]):
                        Game.attack_player(1)
                        Game.end_turn()
                    elif Game.button_attack2.button_clicked(pos[0], pos[1]):
                        Game.attack_player(2)
                        Game.end_turn()
                    elif Game.button_attack3.button_clicked(pos[0], pos[1]):
                        Game.attack_player(3)
                        Game.end_turn()
                    elif Game.button_attack4.button_clicked(pos[0], pos[1]):
                        Game.attack_player(4)
                        Game.end_turn()
                else:
                    if Game.button_magic1.button_clicked(pos[0], pos[1]):
                        Game.magic_player(1)
                        Game.end_turn()
                    elif Game.button_magic2.button_clicked(pos[0], pos[1]):
                        Game.magic_player(2)
                        Game.end_turn()
                    elif Game.button_magic3.button_clicked(pos[0], pos[1]):
                        Game.magic_player(3)
                        Game.end_turn()
                    elif Game.button_magic4.button_clicked(pos[0], pos[1]):
                        Game.magic_player(4)
                        Game.end_turn()
            elif Game.fight_mode == 3:
                if Game.button_back.button_clicked(pos[0], pos[1], 280, 670):
                    Game.fight_mode = 0
                    Game.remove_text()
                elif Game.button_use.button_clicked(pos[0], pos[1]) and Game.use_obj:
                    Game.remove_text(2)
                    Game.add_text(
                        Game.use_object((Game.pos_inventory[1] + Game.pos_inventory[2]) * 5 + Game.pos_inventory[0]),
                        True, True)
                    Game.end_turn()
            elif Game.fight_mode == 4:
                if Game.button_back.button_clicked(pos[0], pos[1], 433, 348):
                    Game.fight_mode = 0
                elif Game.button_confirm.button_clicked(pos[0], pos[1]):
                    Game.fight_mode = 0
                    Game.fade = [True, Game.volume, time.time(), 1]
                    Game.menu = 0
        elif pressed.get(pygame.K_ESCAPE) and temp + 1 / 5 < time.time():
            temp = time.time()
            if Game.fight_mode != 0:
                if Game.fight_mode != 4:
                    Game.remove_text()
                Game.fight_mode = 0
            else:
                Game.fight_mode = 4
        elif pressed.get(pygame.K_RETURN) and Game.fight_mode == 4:
            Game.fight_mode = 0
            Game.fade = [True, Game.volume, time.time(), 1]
            Game.menu = 0
        Game.game_fight(pressed)
    onclick = False
Game.save()
quit()
