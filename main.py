import Game
import pygame
onclick, running, pressed, pos = False, True, {}, [0, 0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if Game.menu == 1 or Game.menu == 2 or Game.menu == 4:
                running = False
                continue
        elif event.type == pygame.KEYDOWN:
            pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            onclick = True
            pos = pygame.mouse.get_pos()
        else:
            onclick = False
    if Game.menu == 0:
        if onclick:
            if Game.button_menu.button_clicked(pos[0], pos[1]):
                Game.menu = 1
            elif Game.button_shop.button_clicked(pos[0], pos[1]):
                pass
        else:
            Game.game_play(pressed)
    elif Game.menu == 1:
        Game.display.display_game()
        pygame.display.flip()
        Game.menu = 2
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
                Game.menu = 4
        else:
            Game.game_menu(pressed)
    elif Game.menu == 4:
        if Game.fight_mode == 0 and onclick:
            if Game.button_attack.button_clicked(pos[0], pos[1]):
                Game.fight_mode = 1
            elif Game.button_magic.button_clicked(pos[0], pos[1]):
                Game.fight_mode = 2
            elif Game.button_inventory.button_clicked(pos[0], pos[1]):
                Game.fight_mode = 3
            elif Game.button_leave.button_clicked(pos[0], pos[1]):
                Game.fight_mode = 4
        Game.game_fight()
Game.save()
quit()
