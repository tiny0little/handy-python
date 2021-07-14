#!/usr/bin/python3

"""
77. Combinations
Difficulty: Medium

"""
from typing import List
import time


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:


sol = Solution()

stime = time.time()
print(sol.combine(n=4, k=2))
print(f'runtime: {time.time() - stime:.1f}sec')
