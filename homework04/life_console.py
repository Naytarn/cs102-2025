"""visualizes game in terminal"""

# pylint: disable=E1101

import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    """another very scary class.."""

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        height, width = self.life.rows, self.life.cols
        for x in range(1, width + 1):
            screen.addch(0, x, "_")
            screen.addch(height, x, "_")
        for y in range(1, height + 1):
            screen.addch(y, 0, "|")
            screen.addch(y, width, "|")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    screen.addch(i + 1, j + 1, "■")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.curs_set(0)
        screen.nodelay(True)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            key = screen.getch()
            if key == ord("q"):
                break
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.1)
            self.life.step()
        curses.endwin()


if __name__ == "__main__":
    life_game = GameOfLife((24, 80), max_generations=50)
    ui = Console(life_game)
    ui.run()
