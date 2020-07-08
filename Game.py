from Variable import *
import time
 
x, y, menu, escape = 48 * 64, 30 * 64, 0, time.time()


def save():
    pass


def game_play(pressed):
    global menu, escape, x, y
    if pressed.get(pygame.K_ESCAPE) and time.time() > escape:
        menu, escape = 1, time.time() + 0.2
        return
    x, y = player.player_move(pressed, x, y, Map, Width, Length)
    display.display()


def game_menu(pressed):
    global menu, escape
    if pressed.get(pygame.K_ESCAPE) and time.time() > escape:
        menu, escape = 0, time.time() + 0.2
