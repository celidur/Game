from game import Game
import pygame

pygame.init()


class Button:
    def __init__(self, color_button, color_text, position_button, text=None, ID=None, size_police=0,
                 image=None, police=None):
        self.image = image
        self.color_button = color_button
        self.position_button = position_button
        self.text = text
        if text is not None:
            self.police = pygame.font.Font("game/font/{}".format(police), size_police)
            self.color_text = color_text
            self.ID = ID
            self.position_text = self.pos_text()

    def display_button(self, Screen, position_x=None, position_y=None, ID=None, position_text=None):
        if position_x is None:
            position_x, position_y = self.position_button[0], self.position_button[1]
        if self.text is not None and ID is not None:
            self.ID = ID
            position_text = self.pos_text(position_x, position_y)
        elif self.text is not None:
            position_text = self.position_text
        if self.image is not None:
            Screen.blit(self.image, (position_x, position_y))
        else:
            pygame.draw.rect(Screen, self.color_button,
                             [position_x, position_y, self.position_button[2], self.position_button[3]])
        if self.text is not None:
            Screen.blit(self.police.render(self.text, False, self.color_text), position_text)
        return Screen

    def button_clicked(self, x, y, position_x=None, position_y=None):
        if position_x is None:
            position_x, position_y = self.position_button[0], self.position_button[1]
        if position_x + self.position_button[2] >= x >= position_x and \
                position_y + self.position_button[3] >= y >= position_y:
            return True
        return False

    def pos_text(self, position_x=None, position_y=None):
        if position_x is None:
            position_x = self.position_button[0]
            position_y = self.position_button[1]
        if self.ID == 'center_up':
            return position_x + (self.position_button[2] - self.police.size(self.text)[0]) // 2, \
                   position_y
        elif self.ID == 'right_up':
            return position_x + self.position_button[2] - self.police.size(self.text)[0], \
                   position_y
        elif self.ID == 'left_middle':
            return position_x, position_y + (
                    self.position_button[3] - self.police.size(self.text)[1]) // 2
        elif self.ID == 'center':
            return position_x + (self.position_button[2] - self.police.size(self.text)[0]) // 2, \
                   position_y + (self.position_button[3] - self.police.size(self.text)[1]) // 2
        elif self.ID == 'right_middle':
            return position_x + self.position_button[2] - self.police.size(self.text)[0], \
                   position_y + (self.position_button[3] - self.police.size(self.text)[1]) // 2
        elif self.ID == 'left_down':
            return position_x, position_y + self.position_button[3] - \
                   self.police.size(self.text)[1]
        elif self.ID == 'center_down':
            return position_x + (self.position_button[2] - self.police.size(self.text)[0]) // 2, \
                   position_y + self.position_button[3] - self.police.size(self.text)[1]
        elif self.ID == 'right_down':
            return position_x + self.position_button[2] - self.police.size(self.text)[0], \
                   position_y + self.position_button[3] - self.police.size(self.text)[1]
        else:  # left_up or errors
            return position_x, position_y
