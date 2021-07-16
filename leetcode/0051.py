#!/usr/bin/python3
"""
51. N-Queens
Difficulty: Hard

"""
from typing import List
import time


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:


sol = Solution()
stime = time.time()
print(sol.solveNQueens(n=4))
print(f'runtime: {time.time() - stime:.2f}sec')
