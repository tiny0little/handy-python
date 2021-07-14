#!/usr/bin/python3
"""
37. Sudoku Solver
Difficulty: Hard

"""
from typing import List
import time


class Solution:

    def __init__(self):
        self.board_copy = [['0' for x in range(9)] for y in range(9)]
        self.solutions_list = {}  # [xy] = [[list of possible solutions], current_solution_idx]

    def best_cell(self, _board: List[List[str]], already_tried: List[List[int]]) -> List[int]:
        result = [-1, -1]
        dot_result = 20
        for x in range(9):
            for y in range(9):
                if ([x, y] not in already_tried) and (_board[y][x] == '.'):
                    dot_counter = 0
                    for i in range(9):
                        if (_board[i][x] == '.') and (i != y): dot_counter += 1
                        if (_board[y][i] == '.') and (i != x): dot_counter += 1
                    if dot_counter < dot_result:
                        dot_result = dot_counter
                        result = [x, y]

        return result

    def best_cells_list(self, _board: List[List[str]]) -> List[List[int]]:
        result = []
        while True:
            cell = self.best_cell(_board, result)
            if cell != [-1, -1]:
                result.append(cell)
            else:
                break
        return result

    def solution_validator(self, _board: List[List[str]]) -> bool:
        for i in range(len(_board)):
            column = []
            row = []
            for col in range(len(_board)):
                col_val = _board[col][i]
                row_val = _board[i][col]
                if col_val != '.': column.append(col_val)
                if row_val != '.': row.append(row_val)
            if (len(column) != len(set(column))) or (len(row) != len(set(row))): return False

        for x_delta in range(0, 9, 3):
            for y_delta in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        val = _board[y_delta + i][x_delta + j]
                        if val != '.': box.append(val)
                if len(box) != len(set(box)): return False

        return True

    def already_solved(self, _board: List[List[str]]) -> bool:
        for x in range(9):
            for y in range(9):
                if _board[y][x] == '.': return False
        return True

    def has_backup(self) -> bool:
        return self.board_copy[0][0] != '0'

    def backup_board(self, _board: List[List[str]]) -> None:
        for x in range(9):
            for y in range(9):
                self.board_copy[y][x] = _board[y][x]

    def restore_board(self, _board: List[List[str]]) -> None:
        for x in range(9):
            for y in range(9):
                _board[y][x] = self.board_copy[y][x]

    def print_board(self, _board: List[List[str]]) -> None:
        for i in range(9): print(f'{_board[i]},')

    def print_solutions_list(self) -> None:
        for key in list(self.solutions_list):
            print(f'[{key}] {self.solutions_list[key]}')

    def count_empty_cells(self, _board: List[List[str]]) -> int:
        result = 0
        for x in range(9):
            for y in range(9):
                if _board[y][x] == '.': result += 1
        return result

    def solution_list_builder(self, _board: List[List[str]]) -> None:
        self.solutions_list = {}
        best_cells = self.best_cells_list(_board)
        for cell in best_cells:
            x = cell[0]
            y = cell[1]
            list0 = []
            if _board[y][x] == '.':
                for n in range(1, 10):
                    _board[y][x] = str(n)
                    if self.solution_validator(_board): list0.append(str(n))
                _board[y][x] = '.'
            self.solutions_list[f'{x}{y}'] = [list0, -1]

    def solveSudoku(self, board: List[List[str]]) -> None:
        solved_counter = 0
        enough_is_enough_counter = 0
        prev_solved_counter = 0
        parallel_cells_number = 2

        while True:

            #
            # we have a counter, in case of difficult to solve puzzle
            if solved_counter == prev_solved_counter:
                enough_is_enough_counter += 1
            else:
                enough_is_enough_counter = 0
                prev_solved_counter = solved_counter

            #
            # logic for lack of single solution
            if enough_is_enough_counter > 7:
                enough_is_enough_counter = 0
                if self.has_backup():
                    self.restore_board(board)
                else:
                    self.backup_board(board)

                if len(self.solutions_list) == 0: self.solution_list_builder(board)

                for key in self.solutions_list:
                    if self.solutions_list[key][1] != -2:
                        self.solutions_list[key][1] += 1
                        saved_key = key
                        break

                parallel_cells_counter = 0
                increasing_next = False
                for key in self.solutions_list:
                    if self.solutions_list[key][1] != -2:
                        parallel_cells_counter += 1
                        if increasing_next:
                            self.solutions_list[key][1] += 1
                            increasing_next = False
                        if self.solutions_list[key][1] > len(self.solutions_list[key][0]) - 1:
                            self.solutions_list[key][1] = 0
                            increasing_next = True
                        if not increasing_next: break

                if parallel_cells_counter > parallel_cells_number: self.solutions_list[saved_key][1] = -2

                for key in self.solutions_list:
                    if self.solutions_list[key][1] >= 0:
                        board[int(key[1])][int(key[0])] = self.solutions_list[key][0][self.solutions_list[key][1]]

                # print('trying this')
                # self.print_board(board)

                # a_counter = 0
                # for key in self.solutions_list:
                #     if self.solutions_list[key][1] == -2: a_counter += 1
                # print(f'{a_counter} / {len(self.solutions_list) - parallel_cells_number}')

                # self.print_solutions_list()
                # break

            #
            # stop if already solved
            if self.already_solved(board): break

            #
            # stop if not able to solve
            if len(self.solutions_list) > 0:
                cant_solve = 0
                for key in self.solutions_list:
                    if self.solutions_list[key][1] == -2: cant_solve += 1
                if cant_solve >= len(self.solutions_list) - parallel_cells_number:
                    print('ERROR: not able to solve')
                    break

            #
            # basic solver, looking for single possible solution
            for x in range(9):
                for y in range(9):
                    if board[y][x] == '.':
                        solution_counter = 0
                        candidate = 0
                        for n in range(1, 10):
                            board[y][x] = str(n)
                            if self.solution_validator(board):
                                solution_counter += 1
                                candidate = n
                            if solution_counter > 1: break
                        if solution_counter == 1:
                            board[y][x] = str(candidate)
                            solved_counter = +1
                        else:
                            board[y][x] = '.'


board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
sol = Solution()
stime = time.time()
sol.solveSudoku(board)
sol.print_board(board)
print(f'runtime: {time.time() - stime:.1f}sec')
print()

board = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
         ["7", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", "2", ".", "1", ".", "9", ".", ".", "."],
         [".", ".", "7", ".", ".", ".", "2", "4", "."],
         [".", "6", "4", ".", "1", ".", "5", "9", "."],
         [".", "9", "8", ".", ".", ".", "3", ".", "."],
         [".", ".", ".", "8", ".", "3", ".", "2", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", "6"],
         [".", ".", ".", "2", "7", "5", "9", ".", "."]]
sol = Solution()
start_time = time.time()
sol.solveSudoku(board)
sol.print_board(board)
print(f'runtime: {time.time() - start_time:.1f}sec')
print()

board = [[".", ".", ".", "2", ".", ".", ".", "6", "3"],
         ["3", ".", ".", ".", ".", "5", "4", ".", "1"],
         [".", ".", "1", ".", ".", "3", "9", "8", "."],
         [".", ".", ".", ".", ".", ".", ".", "9", "."],
         [".", ".", ".", "5", "3", "8", ".", ".", "."],
         [".", "3", ".", ".", ".", ".", ".", ".", "."],
         [".", "2", "6", "3", ".", ".", "5", ".", "."],
         ["5", ".", "3", "7", ".", ".", ".", ".", "8"],
         ["4", "7", ".", ".", ".", "1", ".", ".", "."]]
sol = Solution()
start_time = time.time()
sol.solveSudoku(board)
sol.print_board(board)
print(f'runtime: {time.time() - start_time:.1f}sec')
print()

board = [[".", ".", ".", ".", ".", "7", ".", ".", "9"],
         [".", "4", ".", ".", "8", "1", "2", ".", "."],
         [".", ".", ".", "9", ".", ".", ".", "1", "."],
         [".", ".", "5", "3", ".", ".", ".", "7", "2"],
         ["2", "9", "3", ".", ".", ".", ".", "5", "."],
         [".", ".", ".", ".", ".", "5", "3", ".", "."],
         ["8", ".", ".", ".", "2", "3", ".", ".", "."],
         ["7", ".", ".", ".", "5", ".", ".", "4", "."],
         ["5", "3", "1", ".", "7", ".", ".", ".", "."]]
sol = Solution()
start_time = time.time()
sol.solveSudoku(board)
sol.print_board(board)
print(f'runtime: {time.time() - start_time:.1f}sec')
print()

board = [["1", ".", ".", ".", "7", ".", ".", "3", "."],
         ["8", "3", ".", "6", ".", ".", ".", ".", "."],
         [".", ".", "2", "9", ".", ".", "6", ".", "8"],
         ["6", ".", ".", ".", ".", "4", "9", ".", "7"],
         [".", "9", ".", ".", ".", ".", ".", "5", "."],
         ["3", ".", "7", "5", ".", ".", ".", ".", "4"],
         ["2", ".", "3", ".", ".", "9", "1", ".", "."],
         [".", ".", ".", ".", ".", "2", ".", "4", "3"],
         [".", "4", ".", ".", "8", ".", ".", ".", "9"]]
sol = Solution()
start_time = time.time()
sol.solveSudoku(board=board)
sol.print_board(board)
print(f'runtime: {time.time() - start_time:.1f}sec')
print()
