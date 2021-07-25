#!/usr/bin/python3
"""
73. Set Matrix Zeroes
Difficulty: Medium

Success
Runtime: 104 ms, faster than 100.00% of Python3 online submissions for Set Matrix Zeroes.
Memory Usage: 15.2 MB, less than 45.57% of Python3 online submissions for Set Matrix Zeroes.
"""
from typing import List
import time


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        x_zeros = []
        x_len = len(matrix[0])
        y_len = len(matrix)
        for y in range(y_len):
            if 0 in matrix[y]:
                x_zeros0 = []
                for j in range(matrix[y].count(0)):
                    if len(x_zeros0) == 0:
                        x_zeros0.append(matrix[y].index(0))
                    else:
                        x_zeros0.append(matrix[y].index(0, x_zeros0[-1] + 1))
                x_zeros += x_zeros0
                matrix[y] = [0 for _ in range(x_len)]
        x_zeros = list(set(x_zeros))
        for y in range(y_len):
            if matrix[y][0] != 0:
                for x in x_zeros: matrix[y][x] = 0


sol = Solution()
stime = time.time()
matrix0 = [[0, 0, 0, 5], [4, 3, 1, 4], [0, 1, 1, 4], [1, 2, 1, 3], [0, 0, 1, 1]]
sol.setZeroes(matrix=matrix0)
print(matrix0)
print(f'runtime: {time.time() - stime:.2f}sec')

matrix0 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
sol.setZeroes(matrix=matrix0)
if matrix0 != [[1, 0, 1], [0, 0, 0], [1, 0, 1]]: print('err-1')

matrix0 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
sol.setZeroes(matrix=matrix0)
if matrix0 != [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]: print('err-2')

matrix0 = [[1, 2, 3, 4], [5, 0, 7, 8], [0, 10, 11, 12], [13, 14, 15, 0]]
sol.setZeroes(matrix=matrix0)
if matrix0 != [[0, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]: print('err-19')

matrix0 = [[0, 0, 0, 5], [4, 3, 1, 4], [0, 1, 1, 4], [1, 2, 1, 3], [0, 0, 1, 1]]
sol.setZeroes(matrix=matrix0)
if matrix0 != [[0, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 3], [0, 0, 0, 0]]: print('err-148')
