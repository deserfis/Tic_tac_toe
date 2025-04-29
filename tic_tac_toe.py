import pygame
from pygame.locals import *
from database import criar_tabela, adicionar_ponto, buscar_pontos, resetar_pontos

pygame.init()
pygame.font.init()

# Configurações iniciais
pygame_icon = pygame.image.load("images/icon.png")
pygame_icon = pygame.transform.scale(pygame_icon, (20, 20))
pygame.display.set_icon(pygame_icon)

WIN_SIZE = (450, 600)  # espaço extra para placar e botão
CELL_SIZE = 150

screen = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Tic-Tac-Toe")

class TicTacToe():
    def __init__(self, table_size):
        criar_tabela()  # Garante que a tabela no banco de dados seja criada
        self.score_x, self.score_o = self.load_scores()  # Carrega os pontos dos jogadores

        self.lixeira_button = pygame.Rect(10, 540, 50, 45)
        self.lixeira_icon = pygame.image.load("images/lixeira.png")
        self.lixeira_icon = pygame.transform.scale(self.lixeira_icon, (30, 30))

        self.table_size = table_size
        self.cell_size = table_size // 3
        self.table_space = 20
        self.table = [["-" for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.winner = None
        self.taking_move = True
        self.running = True

        self.background_color = (180, 179, 181)
        self.table_color = (50, 50, 50)
        self.line_color = (38, 255, 0)
        self.instructions_color = (223, 28, 64)
        self.game_over_bg_color = (255, 255, 255)
        self.game_over_color = (223, 28, 64)
        self.font = pygame.font.SysFont("Courier New", 35)
        self.FPS = pygame.time.Clock()

        self.restart_button = pygame.Rect(150, 540, 150, 45)

    def _draw_restart_button(self):
        pygame.draw.rect(screen, (80, 80, 80), self.restart_button, border_radius=8)
        text = self.font.render("Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.restart_button.center)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (200, 0, 0), self.lixeira_button, border_radius=8)
        lixeira_rect = self.lixeira_icon.get_rect(center=self.lixeira_button.center)
        screen.blit(self.lixeira_icon, lixeira_rect)


    def _draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[0]], [tb_space_point[1], cell_space_point[0]], 8)
        pygame.draw.line(screen, self.table_color, [cell_space_point[0], tb_space_point[0]], [cell_space_point[0], tb_space_point[1]], 8)
        pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[1]], [tb_space_point[1], cell_space_point[1]], 8)
        pygame.draw.line(screen, self.table_color, [cell_space_point[1], tb_space_point[0]], [cell_space_point[1], tb_space_point[1]], 8)

    def _change_player(self):
        self.player = "O" if self.player == "X" else "X"

    def _move(self, pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if self.table[x][y] == "-" and self.taking_move:
                self.table[x][y] = self.player
                self._draw_char(x, y, self.player)
                self._game_check()
                if self.taking_move:
                    self._change_player()
        except:
            print("Click dentro do tabuleiro, por favor!")

    def _draw_char(self, x, y, player):
        if player == "O":
            img = pygame.image.load("images/Tc-o.png")
        else:
            img = pygame.image.load("images/Tc-x.png")
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        screen.blit(img, (x * self.cell_size, y * self.cell_size))

    def _reset_game(self):
        self.table = [["-" for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.winner = None
        self.taking_move = True
        screen.fill(self.background_color)
        self._draw_table()

    def _message(self):
        screen.fill(self.background_color, (0, 450, WIN_SIZE[0], 150))

        if self.winner:
            msg = self.font.render(f'{self.winner} WINS!!', True, self.game_over_color)
            screen.blit(msg, (140, 460))
        elif not self.taking_move:
            draw_msg = self.font.render("DRAW!!", True, self.game_over_color)
            screen.blit(draw_msg, (170, 460))
        else:
            instructions = self.font.render(f'{self.player} to move', True, self.instructions_color)
            screen.blit(instructions, (135, 460))

        score_font = pygame.font.SysFont("Courier New", 30)
        score_text = score_font.render(f"Score  X: {self.score_x}  O: {self.score_o}", True, (0, 0, 0))
        screen.blit(score_text, (125, 500))

        self._draw_restart_button()

    def _game_check(self):
        for i in range(3):
            if all(self.table[i][j] == self.player for j in range(3)):
                self._pattern_strike((i, 0), (i, 2), "ver")
                self._win()
                return
            if all(self.table[j][i] == self.player for j in range(3)):
                self._pattern_strike((0, i), (2, i), "hor")
                self._win()
                return

        if all(self.table[i][i] == self.player for i in range(3)):
            self._pattern_strike((0, 0), (2, 2), "left-diag")
            self._win()
            return

        if all(self.table[i][2 - i] == self.player for i in range(3)):
            self._pattern_strike((0, 2), (2, 0), "right-diag")
            self._win()
            return

        if not any("-" in row for row in self.table):
            self.taking_move = False
            self._message()

    def _win(self):
        self.winner = self.player
        self.taking_move = False
        if self.player == "X":
            self.score_x += 1
            adicionar_ponto("X")  # Adiciona ponto ao jogador X no banco de dados
        else:
            self.score_o += 1
            adicionar_ponto("O")  # Adiciona ponto ao jogador O no banco de dados
        self._message()

    def _pattern_strike(self, start_point, end_point, line_type):
        mid_val = self.cell_size // 2

        if line_type == "ver":
            start_x, start_y = start_point[0] * self.cell_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cell_size + mid_val, self.table_size - self.table_space
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[1] * self.cell_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[1] * self.cell_size + mid_val
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        pygame.draw.line(screen, self.line_color, (start_x, start_y), (end_x, end_y), 10)

    def load_scores(self):
        scores = buscar_pontos()  # Busca os pontos no banco de dados
        score_x = next((score[1] for score in scores if score[0] == "X"), 0)
        score_o = next((score[1] for score in scores if score[0] == "O"), 0)
        return score_x, score_o

def main():
    game = TicTacToe(450)
    screen.fill(game.background_color)
    game._draw_table()

    while game.running:
        screen.fill(game.background_color)
        game._draw_table()

        # Desenha as jogadas anteriores
        for x in range(3):
            for y in range(3):
                if game.table[x][y] != "-":
                    game._draw_char(x, y, game.table[x][y])

        game._message()

        for event in pygame.event.get():
            if event.type == QUIT:
                game.running = False

            if event.type == MOUSEBUTTONDOWN:
                if game.restart_button.collidepoint(event.pos):
                    game._reset_game()
                elif game.lixeira_button.collidepoint(event.pos):
                    resetar_pontos()
                    game.score_x = 0
                    game.score_o = 0
                    game._reset_game()
                else:
                    game._move(event.pos)


        pygame.display.update()
        game.FPS.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
