import Game
import pygame

pygame.init()


class Button:
    def __init__(self, color_button, color_text, position_button, text=None, position_text=None, size_police=0,
                 image=None):
        self.image = image
        self.color_button = color_button
        self.color_text = color_text
        self.position_button = position_button
        self.text = text
        self.position_text = position_text
        self.arial = pygame.font.SysFont("arial", size_police)

    def display_button(self, position_x=None, position_y=None, position_text=None):
        if position_x is None:
            position_x, position_y, position_text = self.position_button[0], self.position_button[1], self.position_text
        if self.image is not None:
            Game.Screen.blit(self.image, (position_x, position_y))
        else:
            pygame.draw.rect(Game.Screen, self.color_button,
                             [position_x, position_y, self.position_button[2], self.position_button[3]])
        if self.text is not None:
            Game.Screen.blit(self.arial.render(self.text, False, self.color_text), position_text)

    def button_clicked(self, x, y, position_x=None, position_y=None):
        if position_x is None:
            position_x, position_y = self.position_button[0], self.position_button[1]
        if position_x + self.position_button[2] >= x >= position_x and \
                position_y + self.position_button[3] >= y >= position_y:
            return True
        return False
