import Game
import pygame

running = True#ezneidn
pressed = {}
Game.Afficher()
while running:
    Game.Keyboard_pressed(pressed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False
            quit()
        elif event.type == pygame.KEYDOWN:
            pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
