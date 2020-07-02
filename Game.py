import pickle
import time
from Display import Display
from Player import Player
from Variable import *


def import_map():
    with open('file/map.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        map1 = file.load()
    with open('file/size.txt', 'rb') as file:
        file = pickle.Unpickler(file)
        size = file.load()
    length, width = size[0], size[1]
    return map1, length, width


Map, Length, Width = import_map()
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((704, 736))
x, y, velocity, pressed, menu, escape = 48 * 64, 30 * 64, 8, {}, 0, time.time()
player = Player()
display = Display(block, block2, fond, Width, Length, x, y)


def save():
    pass


def Collision(a, b, c, d, e, f, g, h, i, j, k):
    if (a // 32) % 2 == 0:
        b, c, d, e = b // 64, c // 64, d // 64, e // 64
        if (not Map[b][d][3][f]) and (not Map[c][e][3][g]):
            return True
    else:
        b, c, d, e = (b + j) // 64, (c + j) // 64, (d + k) // 64, (e + k) // 64
        if (not Map[b][d][3][h]) and (not Map[c][e][3][i]):
            return True
    return False


def Game_play(Pressed):
    global x, y, velocity, menu, escape
    move = False
    if Pressed.get(pygame.K_ESCAPE):
        if time.time() > escape:
            menu = 1
            escape = time.time() + 0.2
            return
    if Pressed.get(pygame.K_DOWN) and y // 64 < Width - 1:
        d = Collision(y + 14, x + 17, x + 50, y + 50, y + 50, 1, 0, 3, 2, 0, -32)
        if d:
            y += velocity
            player.Move("down")
            move = True
    elif Pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
        d = Collision(y + 16, x + 17, x + 50, y + 4, y + 4, 3, 2, 1, 0, 0, +32)
        if d:
            y -= velocity
            player.Move("up")
            move = True
    if Pressed.get(pygame.K_RIGHT) and x // 64 < Length - 1:
        d = Collision(x + 14, x + 56, x + 56, y + 42, y + 10, 0, 2, 1, 3, -32, 0)
        if d:
            x += velocity
            if not move:
                player.Move("right")
    elif Pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
        d = Collision(x + 16, x + 10, x + 10, y + 42, y + 10, 1, 3, 0, 2, +32, 0)
        if d:
            x -= velocity
            if not move:
                player.Move("left")
    elif not move:
        player.Move("same")
    display.display_game(Width, Length, x, y, menu, button_shop, button_menu, player)
    pygame.display.flip()


def Game_menu(Pressed):
    global menu, escape
    if Pressed.get(pygame.K_ESCAPE) and time.time() > escape:
        menu = 0
        escape = time.time() + 0.2
