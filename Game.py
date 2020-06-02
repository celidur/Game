import pickle
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
x, y, velocity, pressed = 48 * 64, 30 * 64, 8, {}
player = Player()


def Afficher_case(Block, x_case, y_case, move_x=0, move_y=0):
    Screen.blit(Block, (int((x_case + 5) * 64 - (x % 64)) + move_x, int((y_case + 5) * 64 - (y % 64) + move_y)))


def management_Screen(X1, X2, Y1, Y2, n, Block):
    for X_case in range(X1, (11 + 1) // 2 + X2):
        for Y_case in range(Y1, Y2):
            if 0 <= X_case + x // 64 < Length and y // 64 + Y_case >= 0 and Y_case + y // 64 < Width:
                if Map[x // 64 + X_case][y // 64 + Y_case][n] in Block:
                    if n == 4:
                        block_2 = Block[Map[x // 64 + X_case][y // 64 + Y_case][n]]
                        Afficher_case(block_2[0], X_case, Y_case, block_2[1], block_2[2])
                    else:
                        Afficher_case(Block[Map[x // 64 + X_case][y // 64 + Y_case][n]], X_case, Y_case)

def house(c):
    if Map[((x + 32) // 64)][((y + 32) // 64)][4] != c and Map[((x + 32) // 64)][((y + 32) // 64) - 1][4] != c:
        return True
    return False

def Afficher():
    global Width, Length, x, y
    Screen.blit(fond, (0, 0))
    management_Screen(-5, 3, -6, 8, 0, block)
    management_Screen(-5, 3, -6, 8, 1, block)
    management_Screen(-5, 3, -6, 8, 2, block)
    if house('h1') and house('h2') and house('h3'):
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
        management_Screen(-9, 8, -8, 13, 4, block2)
    else:
        management_Screen(-9, 8, -8, 13, 4, block2)
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
    pygame.display.flip()


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


def Keyboard_pressed(Pressed):
    global x, y, velocity
    move = False
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
    Afficher()
