import curses
import time
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        height, width = screen.getmaxyx()
        for x in range(1, width - 1):
            screen.addch(0, x, '_')
            screen.addch(height - 1, x, '_')
        for y in range(1, height - 1):
            screen.addch(y, 0, '|')
            screen.addch(y, width - 1, '|')


    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        pass

    def run(self) -> None:
        screen = curses.initscr()
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.curs_set(0)
        screen.nodelay(True)  # Неблокирующий ввод

        # Основной цикл
        while (
                self.life.is_changing
                and not self.life.is_max_generations_exceeded
        ):
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.1)
            self.life.step()
        curses.endwin()


life = GameOfLife((24, 80), max_generations=50)
ui = Console(life)
ui.run()