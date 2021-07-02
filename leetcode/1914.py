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
        # result = grid.copy()

        while k > 0:

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

                if ((len(grid) - 2 * m_delta) <= 2) and ((len(grid[0]) - 2 * n_delta) <= 2): break
                if (len(grid) - 2 * m_delta) > 2: m_delta += 1
                if (len(grid[0]) - 2 * n_delta) > 2: n_delta += 1

            grid = result[:]
            k -= 1

        return result


#

sol = Solution()
print(sol.rotateGrid(grid=[[40, 10], [30, 20]], k=2))
