"""This is my torture. it definitely is"""

from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]


# pylint: disable=line-too-long
def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    """Creates grid!"""
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid: maze grid
    :param coord: coordinates where to remove wall
    :return: updated grid
    """
    wall_x, wall_y = coord
    direction_list = []
    if wall_x >= 1:
        direction_list.append("up")
    if wall_y < len(grid[0]) - 2:
        direction_list.append("right")
    if direction_list:
        direction = choice(direction_list)
        if direction == "right":
            grid[wall_x][wall_y + 1] = " "
        elif direction == "up":
            grid[wall_x - 1][wall_y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows: number of rows
    :param cols: number of columns
    :param random_exit: if True - random entrance/exit, else - fixed
    :return: generated maze
    """
    grid = create_grid(rows, cols)

    for i in range(rows):
        for j in range(cols):
            if i % 2 == 1 and j % 2 == 1:
                grid[i][j] = " "

    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        x, y = cell
        remove_wall(grid, (x, y))

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = [int(i) for i in input("Please enter the first door's coordinates:").split()]
        x_out, y_out = [int(i) for i in input("Please enter the second door's coordinates:").split()]

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid: maze grid
    :return: list of exit coordinates
    """
    entry_exit_coords = []
    for i, row in enumerate(grid):
        for j, elem in enumerate(row):
            if elem == "X":
                entry_exit_coords.append((i, j))
    return entry_exit_coords


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid: maze grid with numeric labels
    :param k: current wave number
    :return: updated grid
    """
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == k:
                for direction in DIRECTIONS:
                    cell_x = i + direction[0]
                    cell_y = j + direction[1]
                    if len(grid) > cell_x >= 0 and len(grid[0]) > cell_y >= 0 and grid[cell_x][cell_y] == 0:
                        grid[cell_x][cell_y] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid: maze grid with numeric labels
    :param exit_coord: exit coordinates
    :return: path coordinates from entrance to exit or None
    """
    current_x, current_y = exit_coord
    path = [exit_coord]
    current_k = int(grid[current_x][current_y])
    while current_k > 1:
        for direction in DIRECTIONS:
            cell_x = current_x + direction[0]
            cell_y = current_y + direction[1]
            if len(grid) > cell_x >= 0 and len(grid[0]) > cell_y >= 0:
                if grid[cell_x][cell_y] == current_k - 1:
                    path.append((cell_x, cell_y))
                    current_k -= 1
                    current_x, current_y = cell_x, cell_y
                    break
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid: maze grid
    :param coord: exit coordinates
    :return: True if exit is surrounded, False otherwise
    """
    deadend_count = 0
    exit_x, exit_y = coord
    if not (exit_x == 0 or exit_y == 0 or exit_x == len(grid) - 1 or exit_y == len(grid[0]) - 1):
        return False

    for direction in DIRECTIONS:
        x_check = exit_x + direction[0]
        y_check = exit_y + direction[1]
        if x_check < 0 or x_check >= len(grid) or y_check < 0 or y_check >= len(grid[0]):
            deadend_count += 1
        elif grid[x_check][y_check] == "■":
            deadend_count += 1

    return bool(deadend_count == 4)


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid: maze grid
    :return: tuple of (grid with numeric labels, path or None)
    """
    grid = deepcopy(grid)

    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits
    if len(exits) < 1:
        return grid, None

    for door in exits:
        if encircled_exit(grid, door):
            return grid, None

    for i, row in enumerate(grid):
        for j, elem in enumerate(row):
            if elem == " ":
                grid[i][j] = 0

    # pylint: disable=W0632
    entry, exit_door = exits

    grid[entry[0]][entry[1]] = 1
    grid[exit_door[0]][exit_door[1]] = 0
    k = 1

    while grid[exit_door[0]][exit_door[1]] == 0:
        grid = make_step(grid, k)
        k += 1

    path = shortest_path(grid, exit_door)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid: maze grid
    :param path: path coordinates
    :return: grid with path marked
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
