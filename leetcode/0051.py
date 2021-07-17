#!/usr/bin/python3
"""
51. N-Queens
Difficulty: Hard

Success
Runtime: 272 ms, faster than 10.69% of Python3 online submissions for N-Queens
Memory Usage: 14.7 MB, less than 72.35% of Python3 online submissions for N-Queens
"""
from typing import List
import time


class Solution:

    def __init__(self):
        self.board = []

    # returns True if queen can be placed in [y][x] position
    def is_position_valid(self, x: int, y: int) -> bool:
        if self.board[y][x] == 'Q': return False

        for i in range(len(self.board)):
            if (self.board[i][x] == 'Q') or (self.board[y][i] == 'Q'): return False

        x0 = x
        y0 = y
        while (x0 > 0) and (y0 > 0):
            if x0 > 0: x0 -= 1
            if y0 > 0: y0 -= 1
            if (y != y0) and (x != x0) and (self.board[y0][x0] == 'Q'): return False

        x0 = x
        y0 = y
        while (x0 < len(self.board) - 1) and (y0 < len(self.board) - 1):
            if x0 < len(self.board) - 1: x0 += 1
            if y0 < len(self.board) - 1: y0 += 1
            if (y != y0) and (x != x0) and (self.board[y0][x0] == 'Q'): return False

        x0 = x
        y0 = y
        while (x0 > 0) and (y0 < len(self.board) - 1):
            if x0 > 0: x0 -= 1
            if y0 < len(self.board) - 1: y0 += 1
            if (y != y0) and (x != x0) and (self.board[y0][x0] == 'Q'): return False

        x0 = x
        y0 = y
        while (x0 < len(self.board) - 1) and (y0 > 0):
            if x0 < len(self.board): x0 += 1
            if y0 > 0: y0 -= 1
            if (y != y0) and (x != x0) and (self.board[y0][x0] == 'Q'): return False

        return True

    def solveNQueens(self, n: int) -> List[List[str]]:

        def backtracker(queen_number: int):
            if queen_number == 0:
                result0 = [''.join(self.board[_]) for _ in range(len(self.board))]
                if result0 not in result: result.append(result0)
                return

            y = queen_number - 1
            for x in range(n):
                if self.is_position_valid(x=x, y=y):
                    # note that board's coordinates are swapped -> [y][x]
                    self.board[y][x] = 'Q'
                    backtracker(queen_number - 1)
                    self.board[y][x] = '.'


        self.board = [['.' for _ in range(n)] for _ in range(n)]
        result = []

        backtracker(n)

        return result


sol = Solution()
stime = time.time()
print(sol.solveNQueens(n=7))
print(f'runtime: {time.time() - stime:.2f}sec')
