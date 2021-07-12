#!/usr/bin/python3
"""
37. Sudoku Solver
Difficulty: Hard

"""
from typing import List
import copy


class Solution:
    def best_cell(self, board: List[List[str]], already_tried: List[str]) -> List[int]:
        result = [0, 0]
        result_values = [9, 9]
        for x in range(9):
            for y in range(9):
                if (f'{x}{y}' not in already_tried) and (board[x][y] == '.'):
                    x_counter = 0
                    y_counter = 0
                    for i in range(9):
                        if board[i][y] != '.': x_counter += 1
                        if board[x][i] != '.': y_counter += 1
                    if x_counter + y_counter < result_values[0] + result_values[1]:
                        result_values[0] = x_counter
                        result_values[1] = y_counter
                        result = [x, y]

        return result

    def solution_validator(self, board: List[List[str]]) -> bool:
        for i in range(len(board)):
            column = []
            row = []
            for col in range(len(board)):
                col_val = board[col][i]
                row_val = board[i][col]
                if col_val != '.': column.append(col_val)
                if row_val != '.': row.append(row_val)
            if (len(column) != len(set(column))) or (len(row) != len(set(row))): return False

        for x_delta in range(0, 9, 3):
            for y_delta in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        val = board[x_delta + i][y_delta + j]
                        if val != '.': box.append(val)
                if len(box) != len(set(box)): return False

        return True

    def solveSudoku(self, board: List[List[str]]) -> None:
        solved_counter = 0
        enough_is_enough_counter = 0
        prev_solved_counter = 0
        solutions_stack = {}  # ['xy'] = [give_up_this_cell_flag, [list of solutions tried]]
        board_copy = []
        board_copy0 = []
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
            if enough_is_enough_counter > 100:
                enough_is_enough_counter = 0
                solutions_stack_exhausted = True
                if len(board_copy) > 0: board = [x[:] for x in board_copy]
                if len(solutions_stack) > 0:
                    keep_looping = True
                    for cell_xy in list(solutions_stack):
                        if not keep_looping: break
                        if not solutions_stack[cell_xy][0]:
                            solutions_stack_exhausted = False
                            no_more_solutions = True
                            for n in range(1, 10):
                                if str(n) not in solutions_stack[cell_xy][1]:
                                    board[int(cell_xy[0])][int(cell_xy[1])] = str(n)
                                    if self.solution_validator(board):
                                        no_more_solutions = False
                                        list0 = solutions_stack[cell_xy][1]
                                        list0.append(str(n))
                                        solutions_stack[f'{cell_xy[0]}{cell_xy[1]}'] = [False, list0]
                                        keep_looping = False
                                        break
                            if no_more_solutions:
                                solutions_stack_exhausted = True
                                solutions_stack[f'{cell_xy[0]}{cell_xy[1]}'][0] = True
                                board = [x[:] for x in board_copy]

                if solutions_stack_exhausted:
                    tried_cells = []
                    for cell_xy in list(solutions_stack): tried_cells.append(cell_xy)
                    cell_xy = self.best_cell(board, tried_cells)
                    board_copy0 = [x[:] for x in board]
                    for n in range(1, 10):
                        board[int(cell_xy[0])][int(cell_xy[1])] = str(n)
                        if self.solution_validator(board):
                            solutions_stack[f'{cell_xy[0]}{cell_xy[1]}'] = [False, [str(n)]]
                            board_copy = [x[:] for x in board_copy0]
                            break

            #
            # if already solved, no need to loop any more
            already_solved = True
            for x in range(9):
                for y in range(9):
                    if board[x][y] == '.':
                        already_solved = False
                        break
                if not already_solved: break
            if already_solved: break

            #
            # main solver
            for x in range(9):
                for y in range(9):
                    if board[x][y] == '.':
                        solution_counter = 0
                        candidate = 0
                        for n in range(1, 10):
                            board[x][y] = str(n)
                            if self.solution_validator(board):
                                solution_counter += 1
                                candidate = n
                            if solution_counter > 1: break
                        if solution_counter == 1:
                            board[x][y] = str(candidate)
                            solved_counter = +1
                        else:
                            board[x][y] = '.'


sol = Solution()
board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
# sol.solveSudoku(board=board)
# print(board)

board = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
         ["7", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", "2", ".", "1", ".", "9", ".", ".", "."],
         [".", ".", "7", ".", ".", ".", "2", "4", "."],
         [".", "6", "4", ".", "1", ".", "5", "9", "."],
         [".", "9", "8", ".", ".", ".", "3", ".", "."],
         [".", ".", ".", "8", ".", "3", ".", "2", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", "6"],
         [".", ".", ".", "2", "7", "5", "9", ".", "."]]
sol.solveSudoku(board=board)
print(board)
