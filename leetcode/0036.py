#!/usr/bin/python3
"""
36. Valid Sudoku
Difficulty: Medium

Success
Runtime: 108 ms, faster than 28.70% of Python3 online submissions
Memory Usage: 14.3 MB, less than 40.93% of Python3 online submissions
"""
from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
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


sol = Solution()
# print(sol.isValidSudoku(board=
#                         [["8", "3", ".", ".", "7", ".", ".", ".", "."]
#                             , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
#                             , [".", "9", "8", ".", ".", ".", ".", "6", "."]
#                             , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
#                             , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
#                             , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
#                             , [".", "6", ".", ".", ".", ".", "2", "8", "."]
#                             , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
#                             , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]))
#
# if sol.isValidSudoku(board=
#                      [["5", "3", ".", ".", "7", ".", ".", ".", "."]
#                          , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
#                          , [".", "9", "8", ".", ".", ".", ".", "6", "."]
#                          , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
#                          , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
#                          , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
#                          , [".", "6", ".", ".", ".", ".", "2", "8", "."]
#                          , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
#                          , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]) != True: print('err-1')
#
# if sol.isValidSudoku(board=
#                      [["8", "3", ".", ".", "7", ".", ".", ".", "."]
#                          , ["6", ".", ".", "1", "9", "5", ".", ".", "."]
#                          , [".", "9", "8", ".", ".", ".", ".", "6", "."]
#                          , ["8", ".", ".", ".", "6", ".", ".", ".", "3"]
#                          , ["4", ".", ".", "8", ".", "3", ".", ".", "1"]
#                          , ["7", ".", ".", ".", "2", ".", ".", ".", "6"]
#                          , [".", "6", ".", ".", ".", ".", "2", "8", "."]
#                          , [".", ".", ".", "4", "1", "9", ".", ".", "5"]
#                          , [".", ".", ".", ".", "8", ".", ".", "7", "9"]]) != False: print('err-1')

print(sol.isValidSudoku(board=[

]))
