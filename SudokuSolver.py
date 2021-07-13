import itertools
import copy


class Grid:

    def __init__(self):
        self.data = []

    def get_list(self):
        return self.data

    def get_grid(self):
        grid = []
        for i in range(0, len(self.data), 9):
            grid.append(self.data[i:i + 9])
        return grid

    def set_list(self, list):
        self.data = list

    def set_grid(self, grid):
        # flatten 2d array into 1d array
        self.data = list(itertools.chain(*grid))


class SudokuSolver:

    def __init__(self, board: Grid):
        self.board = copy.deepcopy(board)
        self.check_board = copy.deepcopy(board)
        self.working_index = 0

    def solve(self):
        while(0 in self.check_board.get_list() or not SudokuValidator.is_valid_grid(self.check_board)):
            self.test_next_value_at_index()

            if(self.check_board.get_list()[self.working_index] > 9):
                self.move_index_backward()
                continue

            if(SudokuValidator.is_valid_grid(self.check_board) and (0 in self.check_board.get_list())):
                self.move_index_forward()
                continue

        return self.check_board

    def move_index_forward(self):
        self.working_index += 1
        while(self.board.get_list()[self.working_index] != 0):
            self.working_index += 1

    def move_index_backward(self):
        self.check_board.data[self.working_index] = 0
        self.working_index -= 1
        while(self.board.get_list()[self.working_index] != 0):
            self.working_index -= 1

    def test_next_value_at_index(self):
        self.check_board.data[self.working_index] += 1


class SudokuValidator:

    @ staticmethod
    def is_valid_grid(grid: Grid):
        is_valid = True
        is_valid = is_valid and SudokuValidator.has_valid_rows(grid)
        is_valid = is_valid and SudokuValidator.has_valid_columns(grid)
        is_valid = is_valid and SudokuValidator.has_valid_squares(grid)
        return is_valid

    @ staticmethod
    def sudoku_ok(sudoku_collection):
        is_collection_with_only_unique_elements = sum(
            sudoku_collection) == sum(set(sudoku_collection))
        is_correct_length = len(sudoku_collection) == 9
        return is_collection_with_only_unique_elements and is_correct_length

    @ staticmethod
    def has_valid_rows(grid: Grid):
        rows = grid.get_grid()
        return not ([row for row in rows if not SudokuValidator.sudoku_ok(row)])

    @ staticmethod
    def has_valid_columns(grid: Grid):
        columns = [list(i)
                   for i in zip(*grid.get_grid())]  # transposes the grid
        return not ([columns for columns in columns if not SudokuValidator.sudoku_ok(columns)])

    @ staticmethod
    def has_valid_squares(grid: Grid):
        squares = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square = list(itertools.chain(
                    *([row[j:j+3] for row in grid.get_grid()[i:i+3]])))
                squares.append(square)
        return not ([square for square in squares if not SudokuValidator.sudoku_ok(square)])


if(__name__ == "__main__"):
    board = Grid()
    board.set_list([0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 0, 0, 8, 0, 0, 9, 0, 7, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 7, 5, 0, 0, 8, 0, 5, 6,
                    0, 9, 1, 3, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 3, 0, 0, 1, 0, 0, 0, 5, 7, 0, 0, 4, 0, 3])
    solver = SudokuSolver(board=board)
    solvedGrid = solver.solve()
    print(solvedGrid.get_grid())
