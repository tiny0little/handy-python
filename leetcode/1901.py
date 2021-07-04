#!/usr/bin/python3

"""
1901. Find a Peak Element II
Medium

Success
Runtime: 1320 ms, faster than 13.16% of Python3 online submissions for Find a Peak Element II.
Memory Usage: 45.8 MB, less than 59.14% of Python3 online submissions for Find a Peak Element II.
"""

from typing import List


class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:
        for x in range(len(mat)):
            for y in range(len(mat[0])):
                # print(f"{x}x{y}")
                if (x == 0) and (y == 0):
                    if (mat[x][y] > mat[x + 1][y]) and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]
                elif (x == 0) and (y == len(mat[0]) - 1):
                    if (mat[x][y] > mat[x + 1][y]) and (mat[x][y] > mat[x][y - 1]):
                        return [x, y]
                elif (y == 0) and (x == len(mat) - 1):
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]
                elif (x == len(mat) - 1) and (y == len(mat[0]) - 1):
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x][y - 1]):
                        return [x, y]
                elif x == 0:
                    if (mat[x][y] > mat[x + 1][y]) and (mat[x][y] > mat[x][y - 1]) \
                            and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]
                elif y == 0:
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x + 1][y]) \
                            and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]
                elif x == len(mat) - 1:
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x][y - 1]) \
                            and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]
                elif y == len(mat[0]) - 1:
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x + 1][y]) \
                            and (mat[x][y] > mat[x][y - 1]):
                        return [x, y]
                else:
                    if (mat[x][y] > mat[x - 1][y]) and (mat[x][y] > mat[x + 1][y]) \
                            and (mat[x][y] > mat[x][y - 1]) and (mat[x][y] > mat[x][y + 1]):
                        return [x, y]

        return [-1, -1]


sol = Solution()
print(sol.findPeakGrid(
    [[1, 2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 7, 8, 9, 10], [4, 5, 6, 7, 8, 9, 10, 11]]))

"""
[[78, 96, 64], [37, 100, 30], [78, 46, 29], [82, 25, 80], [33, 87, 97], [93, 99, 85], [88, 18, 81],
         [13, 81, 83], [6, 40, 57], [5, 75, 47], [94, 17, 12], [38, 42, 96], [54, 23, 26], [17, 70, 47], [68, 65, 35],
         [22, 33, 62], [38, 96, 44], [15, 60, 10], [19, 97, 29], [87, 93, 87], [51, 72, 47], [12, 51, 2], [34, 69, 16],
         [59, 48, 87], [96, 87, 34]] -> [1,1]

"""
