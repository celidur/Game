import pygame


size_window = [704, 736]
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((size_window[0], size_window[1]))
menu = 1
running = True
while running:
    if menu == 0:
        pass
    elif menu == 1:
        from game import main
        menu = 2
    elif menu == 2:
        running = main.runnig_game()

main.Game.save()
quit()
