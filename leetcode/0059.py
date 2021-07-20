#!/usr/bin/python3
"""
59. Spiral Matrix II
Difficulty: Medium

Success
Runtime: 28 ms, faster than 88.64% of Python3 online submissions for Spiral Matrix II.
Memory Usage: 14.4 MB, less than 46.03% of Python3 online submissions for Spiral Matrix II.
"""
from typing import List
import time


class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        result = [[0 for _ in range(n)] for _ in range(n)]
        nums_len = n ** 2 + 1

        def populator(num: int, x: int, y: int):
            # first row
            if num < nums_len:
                for x0 in range(x, n - x):
                    result[y][x0] = num
                    num += 1

            # last column
            if num < nums_len:
                for y0 in range(y + 1, n - y - 1):
                    result[y0][-1 - x] = num
                    num += 1

            # last row
            if num < nums_len:
                for x0 in range(n - x - 1, x - 1, -1):
                    result[n - y - 1][x0] = num
                    num += 1

            # first column
            if num < nums_len:
                for y0 in range(n - y - 2, y, -1):
                    result[y0][x] = num
                    num += 1

            if num >= nums_len: return
            populator(num, x + 1, y + 1)

        populator(1, 0, 0)
        return result


sol = Solution()
stime = time.time()
print(sol.generateMatrix(n=15))
print(f'runtime: {time.time() - stime:.2f}sec')
