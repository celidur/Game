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
Screen = pygame.display.set_mode((704, 704))
x, y, velocity, pressed = 48 * 64, 30 * 64, 10, {}
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


def Afficher():
    global Width, Length, x, y
    Screen.blit(fond, (0, 0))
    management_Screen(-5, 3, -6, 7, 0, block)
    management_Screen(-5, 3, -6, 7, 1, block)
    management_Screen(-5, 3, -6, 7, 2, block)
    if Map[((x + 32) // 64)][((y + 32) // 64)][4] != "h1" and Map[((x + 32) // 64)][((y + 32) // 64) - 1][4] != "h1":
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
        management_Screen(-9, 8, -8, 12, 4, block2)
    else:
        management_Screen(-9, 8, -8, 12, 4, block2)
        Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
    pygame.display.flip()


def Keyboard_pressed(Pressed):
    global x, y, velocity
    move = False
    if Pressed.get(pygame.K_DOWN) and y // 64 < Width - 1:
        if not Map[((x + 32) // 64)][(y // 64) + 1][3]:
            y += velocity
            player.Move("down")
            move = True
    elif Pressed.get(pygame.K_UP) and (y + 63) // 64 > 0:
        if not Map[((x + 32) // 64)][(y // 64)][3]:
            y -= velocity
            player.Move("up")
            move = True
    if Pressed.get(pygame.K_RIGHT) and x // 64 < Length - 1:
        if not Map[(x // 64) + 1][(y + 32) // 64][3]:
            x += velocity
            if not move:
                player.Move("right")
    elif Pressed.get(pygame.K_LEFT) and (x + 63) // 64 > 0:
        if not Map[(x // 64)][(y + 32) // 64][3]:
            x -= velocity
            if not move:
                player.Move("left")
    elif not move:
        player.Move("same")
    Afficher()
