import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.life.rows * cell_size
        self.width = self.life.cols * cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
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
                    cell_color = 'lavender'
                else:
                    cell_color = 'grey'

                cell_shape = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(window, cell_color, cell_shape)

    def run(self) -> None:
        """ Запустить игру """
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.life.curr_generation = self.life.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


# run game
life = GameOfLife((48, 64))
gui = GUI(life)
gui.run()
