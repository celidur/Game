import pygame
from game import Game


size_window = [704, 736]
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((size_window[0], size_window[1]))
menu = 1
running = True
save = 1
Game_ = None
while running:
    if menu == 0:
        pass
    elif menu == 1:
        Game_ = Game.Game(save, Screen, size_window)
        if Game_.check_save():
            menu = 2
        else:
            menu = 0
    elif menu == 2:
        running = Game_.running_game()

Game_.save()
quit()
