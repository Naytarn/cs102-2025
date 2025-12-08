"""its my life and it's now or never i aint gonna live forever"""

# pylint: disable=line-too-long
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]


class GameOfLife:
    """game class"""

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        if randomize:
            return [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        neighbors = []
        for delta in NEIGHBORS:
            neighbor_x = cell[0] + delta[0]
            neighbor_y = cell[1] + delta[1]
            if not (neighbor_x >= self.rows or neighbor_y >= self.cols or neighbor_x < 0 or neighbor_y < 0):
                neighbors.append(self.curr_generation[neighbor_x][neighbor_y])

        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        return [
            [
                (
                    1
                    if str(sum(self.get_neighbours((i, j)))) in "23"
                    and self.curr_generation[i][j] == 1
                    or sum(self.get_neighbours((i, j))) == 3
                    and self.curr_generation[i][j] == 0
                    else 0
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.curr_generation = self.curr_generation, self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.readlines()
            for line in contents:
                grid.append([int(cell) for cell in line.split()])

        grid_size = (len(grid), len(grid[0]))
        game = GameOfLife(size=grid_size, randomize=False)
        game.curr_generation = grid
        game.prev_generation = [[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        game.generations = 1
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for row in range(self.rows):
                f.write(" ".join([str(cell) for cell in self.curr_generation[row]]) + "\n")
