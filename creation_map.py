import Variable
import pygame
running = True
pressed = {}
Variable.Afficher()
while running:
    Variable.Keyboard_pressed(pressed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 55 >= pos[0] >= 30 and 725 >= pos[1] >= 710:
                Variable.x_input = True
                Variable.x = (Variable.input_game(Variable.Length))*64
                Variable.x_input = False
                Variable.Afficher()
            elif 105 >= pos[0] >= 80 and 725 >= pos[1] >= 710:
                Variable.y_input = True
                Variable.y = (Variable.input_game(Variable.Width))*64
                Variable.y_input = False
                Variable.Afficher()
            elif 195 >= pos[0] >= 170 and 725 >= pos[1] >= 710:
                Variable.velocity_input = True
                Variable.velocity = Variable.input_game(100)
                if Variable.velocity <= 0:
                    Variable.velocity = 1
                Variable.velocity_input = False
                Variable.Afficher()
            elif 601 >= pos[0] >= 580 and 725 >= pos[1] >= 710:
                Variable.layer_input = True
                Variable.layer = Variable.input_game(3)
                if Variable.layer <= 0:
                    Variable.layer = 0
                Variable.layer_input = False
                Variable.Afficher()
            elif 530 >= pos[0] >= 480 and 725 >= pos[1] >= 710:
                Variable.b_input = True
                Variable.b = Variable.input_game("", 1)
                Variable.b_input = False
                Variable.Afficher()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Variable.x2, Variable.y2, Variable.x1, Variable.y1 = -1, -1, -1, -1
            elif event.key == pygame.K_RETURN:
                if Variable.x1 == -1 and Variable.y1 == -1:
                    Variable.x1, Variable.y1 = (Variable.x+32)//64, (Variable.y+32)//64
                elif Variable.x2 == -1 and Variable.y2 == -1:
                    if (Variable.x+32)//64 != Variable.x1 or (Variable.y+32)//64 != Variable.y1:
                        Variable.x2, Variable.y2 = Variable.x//64, Variable.y//64
                else:
                    if Variable.x1 > Variable.x2:
                        Variable.x1, Variable.x2 = Variable.x2, Variable.x1
                    if Variable.y1 > Variable.y2:
                        Variable.y1, Variable.y2 = Variable.y2, Variable.y1
                    for i in range(Variable.x1, Variable.x2+1):
                        for j in range(Variable.y1, Variable.y2 + 1):
                            Variable.Map[i][j][Variable.layer] = Variable.b
                    Variable.x2, Variable.y2, Variable.x1, Variable.y1 = -1, -1, -1, -1

            pressed[event.key] = True
            Variable.Save()
        elif event.type == pygame.KEYUP:
            pressed[event.key] = False
