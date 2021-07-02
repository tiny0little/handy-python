#!/usr/bin/python3

"""
1914. Cyclically Rotating a Grid
247th LeetCode Weekly Contest
https://leetcode.com/contest/weekly-contest-247/problems/cyclically-rotating-a-grid/

"""

from typing import List


class Solution:

    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        result = [i[:] for i in grid]
        m = len(grid)
        n = len(grid[0])
        m_delta = 0
        n_delta = 0
        while True:
            k0 = k % ((n - n_delta + m - m_delta - 2) * 2)
            while k0 > 0:

                # top and bottom rows
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

                # 2nd to -2nd rows
                for i in range(1 + m_delta, m - m_delta - 1):
                    result[i][n_delta] = grid[i - 1][n_delta]
                    result[i][n - n_delta - 1] = grid[i + 1][n - n_delta - 1]

                k0 -= 1
                grid = [x[:] for x in result]

            if ((len(grid) - 2 * m_delta) <= 2) or ((len(grid[0]) - 2 * n_delta) <= 2): break
            if (len(grid) - 2 * m_delta) > 2: m_delta += 1
            if (len(grid[0]) - 2 * n_delta) > 2: n_delta += 1

        return result


#

sol = Solution()
grid0 = [[3970, 1906, 3608, 298, 3072, 3546, 1502, 773, 4388, 3115, 747, 3937],
         [2822, 304, 4179, 1780, 1709, 1058, 3645, 681, 2910, 2513, 4357, 1038],
         [4471, 2443, 218, 550, 2766, 4780, 1997, 1672, 4095, 161, 4645, 3838],
         [2035, 2350, 3653, 4127, 3208, 4717, 4347, 3452, 1601, 3725, 3060, 2270],
         [188, 2278, 81, 3454, 3204, 1897, 2862, 4381, 3704, 2587, 743, 3832],
         [996, 4499, 66, 2742, 1761, 1189, 608, 509, 2344, 3271, 3076, 108],
         [3274, 2042, 2157, 3226, 2938, 3766, 2610, 4510, 219, 1276, 3712, 4143],
         [744, 234, 2159, 4478, 4161, 4549, 4214, 4272, 701, 4376, 3110, 4896],
         [4431, 1011, 757, 2690, 83, 3546, 946, 1122, 2216, 3944, 2715, 2842],
         [898, 4087, 703, 4153, 3297, 2968, 3268, 4717, 1922, 2527, 3139, 1516],
         [1086, 1090, 302, 1273, 2292, 234, 3268, 2284, 4203, 3838, 2227, 3651],
         [2055, 4406, 2278, 3351, 3217, 2506, 4525, 233, 3829, 63, 4470, 3170],
         [3797, 3276, 1755, 1727, 1131, 4108, 3633, 1835, 1345, 1293, 2778, 2805],
         [1215, 84, 282, 2721, 2360, 2321, 1435, 2617, 1202, 2876, 3420, 3034]]

# print(sol.rotateGrid(grid=grid0, k=123))
i = 1
delta = 2
while i < 10 ** 10:
    if list(sol.rotateGrid(grid=grid0, k=i))[delta][delta:-delta] == list(grid0)[delta][delta:-delta]:
        print(i)
        break
    i += 1
