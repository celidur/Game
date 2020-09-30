from game import creation_map
import pygame
running = True
pressed = {}
creation_map.Afficher()
while running:
    creation_map.Keyboard_pressed(pressed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 55 >= pos[0] >= 30 and 725 >= pos[1] >= 710:
                creation_map.x_input = True
                creation_map.x = (creation_map.input_game(creation_map.Length)) * 64
                creation_map.x_input = False
                creation_map.Afficher()
            elif 105 >= pos[0] >= 80 and 725 >= pos[1] >= 710:
                creation_map.y_input = True
                creation_map.y = (creation_map.input_game(creation_map.Width)) * 64
                creation_map.y_input = False
                creation_map.Afficher()
            elif 195 >= pos[0] >= 170 and 725 >= pos[1] >= 710:
                creation_map.velocity_input = True
                creation_map.velocity = creation_map.input_game(100)
                if creation_map.velocity <= 0:
                    creation_map.velocity = 1
                creation_map.velocity_input = False
                creation_map.Afficher()
            elif 601 >= pos[0] >= 580 and 725 >= pos[1] >= 710:
                creation_map.layer_input = True
                creation_map.layer = creation_map.input_game(3)
                if creation_map.layer <= 0:
                    creation_map.layer = 0
                creation_map.layer_input = False
                creation_map.Afficher()
            elif 530 >= pos[0] >= 480 and 725 >= pos[1] >= 710:
                creation_map.b_input = True
                creation_map.b = creation_map.input_game("", 1)
                creation_map.b_input = False
                creation_map.Afficher()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                creation_map.x2, creation_map.y2, creation_map.x1, creation_map.y1 = -1, -1, -1, -1
            elif event.key == pygame.K_RETURN:
                if creation_map.x1 == -1 and creation_map.y1 == -1:
                    creation_map.x1, creation_map.y1 = (creation_map.x + 32) // 64, (creation_map.y + 32) // 64
                elif creation_map.x2 == -1 and creation_map.y2 == -1:
                    if (creation_map.x + 32)//64 != creation_map.x1 or (creation_map.y + 32)//64 != creation_map.y1:
                        creation_map.x2, creation_map.y2 = creation_map.x // 64, creation_map.y // 64
                else:
                    if creation_map.x1 > creation_map.x2:
                        creation_map.x1, creation_map.x2 = creation_map.x2, creation_map.x1
                    if creation_map.y1 > creation_map.y2:
                        creation_map.y1, creation_map.y2 = creation_map.y2, creation_map.y1
                    for i in range(creation_map.x1, creation_map.x2 + 1):
                        for j in range(creation_map.y1, creation_map.y2 + 1):
                            creation_map.Map[i][j][creation_map.layer] = creation_map.b
                    creation_map.x2, creation_map.y2, creation_map.x1, creation_map.y1 = -1, -1, -1, -1

            pressed[event.key] = True
            creation_map.save()
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
