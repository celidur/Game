import time
import pygame


class Display:
    def __init__(self, size_window, Game):
        self.Game = Game
        self.list_ = []
        self.object = []
        self.size_window = size_window
        self.arial = pygame.font.Font("game/font/FRAMDCN.TTF", 20)
        self.dialogue = pygame.font.Font("game/font/rpg_.FON", 16)
        self.colors = {
            self.Game.Texts.plain: (68, 255, 0),
            self.Game.Texts.desert: (249, 210, 39),
            self.Game.Texts.snow: (152, 249, 219),
            self.Game.Texts.forest: (11, 109, 13),
            self.Game.Texts.mountain: (123, 95, 62),
            self.Game.Texts.volcano: (163, 41, 18)}

    def display_chunks(self, fight=False):
        i = (self.Game.x + 512) // 1024
        j = (self.Game.y + 512) // 1024
        image = []
        """if fight:
            image.append(
                (self.Game.game_chunk[0], (0 - self.Game.x + 512 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j)))
            image.append(
                (self.Game.game_chunk[1], (0 - self.Game.x + 512 + 1024 * i, 0 - self.Game.y + 320 + 1024 * j - 1024)))
            image.append(
                (self.Game.game_chunk[2], (0 - self.Game.x + 512 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j)))
            image.append((self.Game.game_chunk[3],
                          (0 - self.Game.x + 512 + 1024 * i - 1024, 0 - self.Game.y + 320 + 1024 * j - 1024)))
            return 0"""

        image.append((self.Game.map_chunk[i - 1][j - 1],
                          (0 - self.Game.x + 480 + 1024 * i - 1024, 0 - self.Game.y + 352 + 1024 * j - 1024)))
        image.append((self.Game.map_chunk[i][j - 1],
                          (0 - self.Game.x + 480 + 1024 * i, 0 - self.Game.y + 352 + 1024 * j - 1024)))
        image.append((self.Game.map_chunk[(i + 1) % len(self.Game.map_chunk)][j - 1],
                          (0 - self.Game.x + 480 + 1024 * i + 1024, 0 - self.Game.y + 352 + 1024 * j - 1024)))
        image.append((self.Game.map_chunk[i - 1][j],
                          (0 - self.Game.x + 480 + 1024 * i - 1024, 0 - self.Game.y + 352 + 1024 * j)))
        image.append((self.Game.map_chunk[i][j],
                          (0 - self.Game.x + 480 + 1024 * i, 0 - self.Game.y + 352 + 1024 * j)))
        image.append((self.Game.map_chunk[(i + 1) % len(self.Game.map_chunk)][j],
                          (0 - self.Game.x + 480 + 1024 * i + 1024, 0 - self.Game.y + 352 + 1024 * j)))
        return image

    def display_game(self):
        pygame.draw.rect(self.Game.Screen, (55, 25, 5), [0, 0, 1080, 768])
        placed = False
        self.object = self.display_chunks()
        for i in self.Game.entities:
            if (i[1] == self.Game.y and i[0] >= self.Game.x or i[1] > self.Game.y) and not placed:
                self.object.append((self.Game.player.image, (480, 352)))
                placed = True
            self.object.append((i[2].image, (i[2].x - self.Game.x + 480, i[2].y - self.Game.y + 352)))
        if not placed:
            self.object.append((self.Game.player.image, (480, 352)))
        self.Game.Screen.blits(self.object)
        """self.Game.player.all_projectiles.draw(self.Game.Screen)"""
        for i in self.Game.entities:
            for j in range(len(i[2].rects)):
                s = pygame.Surface((i[2].rects[j].w, i[2].rects[j].h), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                self.Game.Screen.blit(s, (i[2].rects[j].x - self.Game.x + 480, i[2].rects[j].y -
                                                               self.Game.y + 352))
        s = pygame.Surface((self.Game.player.rects[0].w, self.Game.player.rects[0].h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.Game.Screen.blit(s, (self.Game.player.rects[0].x - self.Game.x + 480, self.Game.player.rects[0].y -
                                  self.Game.y + 352))
        if self.Game.display_inventory:
            self.Game.Screen.blit(pygame.image.load('game/assets/inventory/inventory_menu.png'), (704, 0))
        if self.Game.menu == 0:
            if self.Game.area == 'village':
                self.Game.Screen = self.Game.button_shop.display_button(self.Game.Screen)
            self.Game.Screen = self.Game.button_menu.display_button(self.Game.Screen)

    def display_pause(self):
        s = pygame.Surface((self.size_window[0], self.size_window[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.Game.Screen.blit(s, (0, 0))
        self.Game.Screen = self.Game.button_pause.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_setting.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_save.display_button(self.Game.Screen)
        self.Game.Screen = self.Game.button_exit.display_button(self.Game.Screen)

    def display_chest(self):
        self.Game.Screen.blit(pygame.image.load('game/assets/inventory/chest_menu.png'), (144, 240))

    def display(self):  # #
        self.display_game()
        if self.Game.menu == 2:
            self.display_pause()
        elif self.Game.menu == 1:
            self.display_chest()
        pygame.display.flip()

    def display_text(self, texts, x_pos, y_pos, font, size, prog, color, length, change_old, point=False):
        font_ = pygame.font.Font("game/font/" + font, size)
        x, y = 0, 0
        texts = texts.split('|')
        for i in range(len(texts)):
            if point:
                font_2 = pygame.font.Font("game/font/FRAMDCN.TTF", 32)
                if prog == 0:
                    if change_old and i < len(texts) - 1:
                        self.Game.Screen.blit(
                            font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                            (x_pos - 10, y_pos + y - 16))
                    else:
                        self.Game.Screen.blit(font_2.render('·', False, color),
                                              (x_pos - 10, y_pos + y - 16))
                else:
                    if i < len(texts) - prog:
                        self.Game.Screen.blit(
                            font_2.render('·', False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                            (x_pos - 10, y_pos + y - 16))
                    else:
                        self.Game.Screen.blit(font_2.render('·', False, color),
                                              (x_pos - 10, y_pos + y - 16))
            texts[i] = texts[i].split(' ')
            line = ''
            for word in texts[i]:
                if prog == 0:
                    if font_.size(line + word)[0] < length or line == '':
                        line += word + ' '
                    elif font_.size(line + word)[0] >= length or word == texts[i][-1]:
                        if change_old and i < len(texts) - 1:
                            self.Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7,
                                                                             color[2] // 1.7)),
                                                  (x_pos, y_pos + y))
                        else:
                            self.Game.Screen.blit(font_.render(line, False, color), (x_pos, y_pos + y))
                        line, y = word + ' ', y + size
                else:
                    if x + font_.size(word)[0] >= length:
                        x = 0
                        y += size
                    for char in word:
                        if i >= len(texts) - prog:
                            self.Game.Screen.blit(self.dialogue.render(char, False, color), (x_pos + x, y_pos + y))
                            pygame.display.flip()
                            time.sleep(0.05)
                            if char == '.':
                                time.sleep(0.5)
                        elif change_old:
                            self.Game.Screen.blit(
                                self.dialogue.render(char, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                (x_pos + x, y_pos + y))
                        x += font_.size(char)[0]
                    x += font_.size(' ')[0]
                    pass
            if change_old and i < len(texts) - 1:
                self.Game.Screen.blit(font_.render(line, False, (color[0] // 1.7, color[1] // 1.7, color[2] // 1.7)),
                                      (x_pos + x, y_pos + y))

            else:
                self.Game.Screen.blit(font_.render(line, False, color), (x_pos + x, y_pos + y))
            x = 0
            y += size
