import math

def can_be_placed(current_solution):
    last_row = len(current_solution) - 1
    for row in range(last_row):
        diff = math.fabs(current_solution[row] - current_solution[last_row])
        if diff == 0 or diff == math.fabs(last_row - row):
            return False
    return True

def solve_n_queens(board_size, row, current_solution, results):
    if row == board_size:
        results.append(current_solution.copy())
    else:
        for column in range(board_size):
            current_solution.append(column)
            if can_be_placed(current_solution):
                solve_n_queens(board_size, row + 1, current_solution, results)
            current_solution.pop()

def n_queens(board_size):
    results = []
    current_solution = []
    solve_n_queens(board_size, 0, current_solution, results)
    return len(results)
