import pygame


a = 1
if a == 1:
    from game import main
    while main.running:
        main.runnig_game()


main.Game.save()
quit()
