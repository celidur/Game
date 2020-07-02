import Game


class Display:
    def __init__(self, block, block2, fond, Width, Length, x, y):
        self.Width, self.Length, self.x, self.y = Width, Length, x, y
        self.block = block
        self.block2 = block2
        self.fond = fond

    def Afficher_case(self, block, x_case, y_case, move_x=0, move_y=0):
        Game.Screen.blit(block, (int((x_case + 5) * 64 - (self.x % 64)) + move_x, int((y_case + 5) * 64 - (self.y % 64) + move_y)))

    def management_Screen(self, X1, X2, Y1, Y2, n, Block):
        for X_case in range(X1, (11 + 1) // 2 + X2):
            for Y_case in range(Y1, Y2):
                if 0 <= X_case + self.x // 64 < self.Length and self.y // 64 + Y_case >= 0 and Y_case + self.y // 64 < self.Width:
                    if Game.Map[self.x // 64 + X_case][self.y // 64 + Y_case][n] in Block:
                        if n == 4:
                            block_2 = Block[Game.Map[self.x // 64 + X_case][self.y // 64 + Y_case][n]]
                            self.Afficher_case(block_2[0], X_case, Y_case, block_2[1], block_2[2])
                        else:
                            self.Afficher_case(Block[Game.Map[self.x // 64 + X_case][self.y // 64 + Y_case][n]], X_case, Y_case)

    def house(self, c):
        if Game.Map[((self.x + 32) // 64)][((self.y + 32) // 64)][4] != c and Game.Map[((self.x + 32) // 64)][((self.y + 32) // 64) - 1][4] != c:
            return True
        return False

    def display_game(self, Width, Length, x, y, menu, button_shop, button_menu, player):
        self.Width, self.Length, self.x, self.y = Width, Length, x, y
        Game.Screen.blit(self.fond, (0, 0))
        self.management_Screen(-5, 3, -6, 8, 0, self.block)
        self.management_Screen(-5, 3, -6, 8, 1, self.block)
        self.management_Screen(-5, 3, -6, 8, 2, self.block)
        if menu == 0:
            button_shop.display_button()
            button_menu.display_button()
        if self.house('h1') and self.house('h2') and self.house('h3'):
            Game.Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
            self.management_Screen(-9, 8, -8, 13, 4, self.block2)
        else:
            self.management_Screen(-9, 8, -8, 13, 4, self.block2)
            Game.Screen.blit(player.image, (11 // 2 * 64, 5 * 64))
