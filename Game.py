from Variable import *
import time
 
x, y, menu, escape = 48 * 64, 30 * 64, 0, time.time()


def save():
    pass


def Game_play(Pressed):
    global menu, escape, x, y
    if Pressed.get(pygame.K_ESCAPE) and time.time() > escape:
        menu, escape = 1, time.time() + 0.2
        return
    x, y = player.Player_move(Pressed, x, y, Map, Width, Length)
    display.display()


def Game_menu(Pressed):
    global menu, escape
    if Pressed.get(pygame.K_ESCAPE) and time.time() > escape:
        menu, escape = 0, time.time() + 0.2
