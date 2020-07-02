import Game
import pygame
onclick = False
running = True
pressed = {}
pos = [0, 0]
while running:
    if Game.menu == 0:
        if onclick:
            if Game.button_menu.button_clicked(pos[0], pos[1]):
                Game.menu = 1
            elif Game.button_shop.button_clicked(pos[0], pos[1]):
                pass
        else:
            Game.Game_play(pressed)
    elif Game.menu == 1:
        Game.display.display_game(Game.Width, Game.Length, Game.x, Game.y, Game.menu, Game.button_shop, Game.button_menu, Game.player)
        s = pygame.Surface((704, 736), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        Game.Screen.blit(s, (0, 0))
        Game.button_pause.display_button()
        Game.button_setting.display_button()
        Game.button_save.display_button()
        Game.button_exit.display_button()
        pygame.display.flip()
        Game.menu = 2
    elif Game.menu == 2:
        if onclick:
            if Game.button_pause.button_clicked(pos[0], pos[1]):
                Game.menu = 0
            elif Game.button_exit.button_clicked(pos[0], pos[1]):
                running = False
                Game.save()
                continue
            elif Game.button_save.button_clicked(pos[0], pos[1]):
                Game.save()
        else:
            Game.Game_menu(pressed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
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
quit()
