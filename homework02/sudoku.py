"""Sudoku solver, generator, checker etc."""

import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Превратить данные в таблицу"""
    digits = [c for c in puzzle if c in "123456789."]
    grid_from_list = group(digits, 9)
    return grid_from_list


def display(to_display: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        for col in range(9):
            print("".join(to_display[row][col].center(width) + ("|" if str(col) in "25" else "")))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid_get_row: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid_get_row[pos[0]]


def get_col(grid_get_col: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid_get_col[i][pos[1]] for i in range(len(grid_get_col))]
    # pylint: disable=line-too-long


def get_block(grid_get_block: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    block_row = (pos[0] // 3) * 3
    block_col = (pos[1] // 3) * 3

    return [grid_get_block[i][j] for i in range(block_row, block_row + 3) for j in range(block_col, block_col + 3)]


def find_empty_positions(grid_find_empty: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row, row_elements in enumerate(grid_find_empty):
        for col, cell in enumerate(row_elements):
            if cell == ".":
                return row, col
    return None


def find_possible_values(find_nums: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """

    used_digits = set(get_row(find_nums, pos)) | set(get_col(find_nums, pos)) | set(get_block(find_nums, pos))
    used_digits.discard(".")
    return set(str(i + 1) for i in range(len(find_nums))) - used_digits


def solve(grid_to_solve: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid_to_solve
    Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid) # doctest: +NORMALIZE_WHITESPACE
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
    ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
    ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
    ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
    ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
    ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
    ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
    ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
    ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_space = find_empty_positions(grid_to_solve)
    if not empty_space:
        return grid_to_solve
    possible_values = find_possible_values(grid_to_solve, (empty_space[0], empty_space[1]))
    if not possible_values:
        return None
    for value in possible_values:
        grid_to_solve[empty_space[0]][empty_space[1]] = value
        grid_solution = solve(grid_to_solve)
        if grid_solution:
            return grid_solution
        grid_to_solve[empty_space[0]][empty_space[1]] = "."

    return None


def check_solution(solution_to_check: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False
    >>> sudoku = [
    ...    ["9", "2", "6", "5", "8", "3", "4", "7", "1"],
    ...    ["7", "1", "3", "4", "2", "6", "9", "8", "5"],
    ...    ["5", "4", "8", "9", "7", "1", "3", "6", "2"],
    ...    ["6", "3", "7", "8", "1", "5", "2", "4", "9"],
    ...    ["4", "8", "2", "7", "3", "9", "1", "5", "6"],
    ...    ["1", "5", "9", "2", "6", "4", "8", "3", "7"],
    ...    ["3", "7", "4", "1", "5", "2", "6", "9", "8"],
    ...    ["8", "9", "1", "6", "4", "7", "5", "2", "3"],
    ...    ["2", "6", "5", "3", "9", "8", "7", "1", "4"]
    ... ]
    >>> check_solution(sudoku)
    True

    >>> sudoku = [
    ...    ["9", "2", "6", "5", "8", "3", "4", "7", "1"],
    ...    ["7", "1", "3", "4", "2", "6", "9", "8", "5"],
    ...    ["9", "4", "8", "5", "7", "1", "3", "6", "2"],
    ...    ["6", "3", "7", "8", "1", "5", "2", "4", "9"],
    ...    ["4", "8", "2", "7", "3", "9", "1", "5", "6"],
    ...    ["1", "5", "9", "2", "6", "4", "8", "3", "7"],
    ...    ["3", "7", "4", "1", "5", "2", "6", "9", "8"],
    ...    ["8", "9", "1", "6", "4", "7", "5", "2", "3"],
    ...    ["2", "6", "5", "3", "9", "8", "7", "1", "4"]
    ... ]
    >>> check_solution(sudoku)
    False

    >>> sudoku = [
    ...    ["9", "2", "6", "5", "8", "3", "4", "7", "1"],
    ...    ["7", "1", "3", "4", "2", "6", "9", "8", "5"],
    ...    ["5", "4", "9", "8", "7", "1", "3", "6", "2"],
    ...    ["6", "3", "7", "8", "1", "5", "2", "4", "9"],
    ...    ["4", "8", "2", "7", "3", "9", "1", "5", "6"],
    ...    ["1", "5", "9", "2", "6", "4", "8", "3", "7"],
    ...    ["3", "7", "4", "1", "5", "2", "6", "9", "8"],
    ...    ["8", "9", "1", "6", "4", "7", "5", "2", "3"],
    ...    ["2", "6", "5", "3", "9", "8", "7", "1", "4"]
    ... ]
    >>> check_solution(sudoku)
    False

    >>> sudoku = [
    ...    ["9", "2", "6", "5", "8", "3", "4", "7", "1"],
    ...    ["7", "1", "3", "4", "2", "6", "9", "8", "5"],
    ...    ["5", "4", "8", "9", "7", "1", "3", "6", "2"],
    ...    ["6", "3", "7", "8", "1", "5", "2", "4", "9"],
    ...    ["4", "8", "2", "7", "3", "9", "1", "5", "6"],
    ...    ["1", "5", "9", "2", "6", ".", "8", "3", "7"],
    ...    ["3", "7", "4", "1", "5", "2", "6", "9", "8"],
    ...    ["8", "9", "1", "6", "4", "7", "5", "2", "3"],
    ...    ["2", "6", "5", "3", "9", "8", "7", "1", "4"]
    ... ]
    >>> check_solution(sudoku)
    False
    """

    for i, row in enumerate(solution_to_check):
        row_set = set(row)
        col_set = set(solution_to_check[j][i] for j in range(len(solution_to_check)))
        if row_set != set(str(num + 1) for num in range(len(solution_to_check))) or col_set != set(
            str(num + 1) for num in range(len(solution_to_check))
        ):
            return False

    for i in range(0, len(solution_to_check), 3):
        for j in range(0, len(solution_to_check), 3):
            block = set()
            for x in range(3):
                for y in range(3):
                    block.add(solution_to_check[i + x][j + y])
            if block != set(str(i + 1) for i in range(len(solution_to_check))):
                return False
    return True


def generate_solved_sudoku() -> tp.List[tp.List[str]]:
    """Генерация уже решённого судоку
    >>> check_solution(generate_solved_sudoku())
    True
    """

    base_sudoku = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["7", "8", "9", "1", "2", "3", "4", "5", "6"],
        ["4", "5", "6", "7", "8", "9", "1", "2", "3"],
        ["2", "3", "4", "5", "6", "7", "8", "9", "1"],
        ["8", "9", "1", "2", "3", "4", "5", "6", "7"],
        ["5", "6", "7", "8", "9", "1", "2", "3", "4"],
        ["3", "4", "5", "6", "7", "8", "9", "1", "2"],
        ["9", "1", "2", "3", "4", "5", "6", "7", "8"],
        ["6", "7", "8", "9", "1", "2", "3", "4", "5"],
    ]

    shuffled_digits = random.sample([str(i) for i in range(1, 10)], 9)

    for row in range(9):
        for col in range(9):
            base_sudoku[row][col] = shuffled_digits[int(base_sudoku[row][col]) - 1]

    return base_sudoku


def generate_sudoku(digits_in_sudoku: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    full_sudoku = generate_solved_sudoku()
    digits_left = min(81, digits_in_sudoku)
    empty_positions = random.sample(list(range(81)), 81 - digits_left)

    for pos in empty_positions:
        row, col = pos // 9, pos % 9
        full_sudoku[row][col] = "."

    return full_sudoku


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
