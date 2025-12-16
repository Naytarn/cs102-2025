"""visualizes game with pygame!"""

# pylint: disable=line-too-long
# pylint: disable=E1101


import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    """very scary class"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.life.rows * cell_size
        self.width = self.life.cols * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        window = self.screen

        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                if cell == 1:
                    cell_color = "lavender"
                else:
                    cell_color = "grey"

                cell_shape = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(window, cell_color, cell_shape)

    def set_cell_state(self, click_pos: tuple) -> None:
        """changes cell state on click"""
        click_y, click_x = click_pos
        cell_chosen_x = click_x // self.cell_size
        cell_chosen_y = click_y // self.cell_size

        self.life.curr_generation[cell_chosen_x][cell_chosen_y] = (
            1 - self.life.curr_generation[cell_chosen_x][cell_chosen_y]
        )

    def run(self) -> None:
        """Запустить игру"""
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.life.curr_generation = self.life.create_grid(True)

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                elif event.type == MOUSEBUTTONDOWN:
                    if paused and event.button == 1:
                        self.set_cell_state(event.pos)
            self.draw_lines()
            self.draw_grid()
            if not paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


# run game
life_game = GameOfLife((48, 64))
gui = GUI(life_game)
gui.run()
