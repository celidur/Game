import asyncio
import time

import pygame
from game import Game

nb_frame_game = 0
nb_frame_display = 0
time_start_sec = time.time()
fps_game = 60
fps_display = -1


async def game():
    global time_start_sec, nb_frame_game, fps_game
    while time.time() < time_start_sec + 1 and Game_.running:
        nb_frame_game += 1
        while time.time() < time_start_sec + nb_frame_game / fps_game:
            await asyncio.sleep(0)
        Game_.running_game()


async def display():
    global time_start_sec, nb_frame_display, fps_display
    while time.time() < time_start_sec + 1 and Game_.running:
        nb_frame_display += 1
        while time.time() < time_start_sec + nb_frame_display / fps_display:
            await asyncio.sleep(0)
        Game_.refresh_screen()
        await asyncio.sleep(0)


async def pressed():
    global time_start_sec
    while time.time() < time_start_sec + 1 and Game_.running:
        Game_.get_pressed()
        await asyncio.sleep(0)


async def main_sec():
    global time_start_sec, nb_frame_game, nb_frame_display
    t1 = asyncio.create_task(game())
    t2 = asyncio.create_task(display())
    t3 = asyncio.create_task(pressed())
    await asyncio.gather(t1, t2, t3)
    print(nb_frame_display)
    time_start_sec, nb_frame_game, nb_frame_display = time.time(), 0, 0


size_window = [1024, 768]
pygame.init()
pygame.display.set_caption("Game")
Screen = pygame.display.set_mode((size_window[0], size_window[1]), pygame.FULLSCREEN | pygame.HWSURFACE)
menu = 2
save = 1
Game_ = Game.Game(save, Screen, size_window)
if Game_.check:
    pass

while Game_.running:
    if menu == 1:
        asyncio.run(main_sec())
    elif menu == 2:
        if Game_.ready:
            menu = 1
            Game_.running_game()
            pygame.display.get_surface()
        else:
            Game_.loading()
Game_.save()
quit()
