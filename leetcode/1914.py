#!/usr/bin/python3.8

"""
1914. Cyclically Rotating a Grid
247th LeetCode Weekly Contest
https://leetcode.com/contest/weekly-contest-247/problems/cyclically-rotating-a-grid/

"""

from typing import List


class Solution:

    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        result = [[0 for col in range(n)] for row in range(m)]

        m_delta = 0
        n_delta = 0

        while True:

            for i in range(n_delta, n - n_delta):
                if i == n_delta:
                    result[m_delta][i] = grid[m_delta][i + 1]
                    result[m - m_delta - 1][i] = grid[m - m_delta - 2][i]
                elif i == n - n_delta - 1:
                    result[m_delta][i] = grid[m_delta + 1][i]
                    result[m - m_delta - 1][i] = grid[m - m_delta - 1][i - 1]
                else:
                    result[m_delta][i] = grid[m_delta][i + 1]
                    result[m - m_delta - 1][i] = grid[m - m_delta - 1][i - 1]

            for i in range(1 + m_delta, m - m_delta - 1):
                result[i][n_delta] = grid[i - 1][n_delta]
                result[i][n - n_delta - 1] = grid[i + 1][n - n_delta - 1]

        return result


#

sol = Solution()
print(sol.rotateGrid(grid=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], k=2))
