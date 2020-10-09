import pygame
import os
import pickle


def save(a):
    try:
        os.remove("game/file/save")
    except FileNotFoundError:
        pass
    with open("game/file/save", 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(a)

size_window = [704, 736]
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((size_window[0], size_window[1]))
menu = 1
running = True
save_ = 1
save(save_)
while running:
    if menu == 0:
        pass
    elif menu == 1:
        from game import Game
        menu = 2
    elif menu == 2:
        running = Game.running_game()

Game.save()
quit()
