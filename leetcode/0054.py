#!/usr/bin/python3
"""
54. Spiral Matrix
Difficulty: Medium

Success
Runtime: 16 ms, faster than 99.93% of Python3 online submissions for Spiral Matrix
Memory Usage: 14.3 MB, less than 58.27% of Python3 online submissions for Spiral Matrix
"""
from typing import List
import time


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:

        def extractor(mat: List[List[int]]) -> List[int]:
            mat_len = len(mat)
            if mat_len == 1: return mat[0]
            if mat_len == 0: return []
            if len(mat[0]) == 0: return []

            # first row
            result0 = mat[0][:]

            # last column
            for y in range(1, mat_len - 1): result0.append(mat[y][-1])

            # last row
            list0 = mat[mat_len - 1][:]
            list0.reverse()
            result0 = result0 + list0

            # first column
            if len(mat[0]) > 1:
                for y in range(mat_len - 2, 0, -1): result0.append(mat[y][0])

            mat0 = [mat[i][1:-1] for i in range(1, mat_len - 1)]
            return result0 + extractor(mat0)

        return extractor(matrix)


sol = Solution()
stime = time.time()
print(sol.spiralOrder(matrix=[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.spiralOrder(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) != [1, 2, 3, 6, 9, 8, 7, 4, 5]: print('err-1')
if sol.spiralOrder(matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) != [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]:
    print('err-2')
if sol.spiralOrder(matrix=[[7], [9], [6]]) != [7, 9, 6]: print('err-10')
if sol.spiralOrder(matrix=[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]) != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    print('err-11')
