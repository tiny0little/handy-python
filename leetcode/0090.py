#!/usr/bin/python3
"""
90. Subsets II
Difficulty: Medium

Success
Runtime: 7800 ms, faster than 6.04% of Python3 online submissions for Subsets II.
Memory Usage: 14.5 MB, less than 57.19% of Python3 online submissions for Subsets II.
"""
from typing import List
import time


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        result = [[]]

        def backtracker(nums0: List[int]):
            nums0len = len(nums0)
            if nums0len == 0: return
            for i in range(1, nums0len + 1):
                candidate = sorted(nums0[0:i])
                if candidate not in result: result.append(candidate)
            for i in range(nums0len - 1): backtracker(nums0[:i] + nums0[i + 1:])

        backtracker(nums)
        return result


sol = Solution()
stime = time.time()
o = sol.subsetsWithDup(nums=[4, 4, 4, 1, 4])
print(f'{len(o)} {o}')
print(f'runtime: {time.time() - stime:.2f}sec')

if len(sol.subsetsWithDup(nums=[1, 2, 3])) != 8: print('err-7')
if len(sol.subsetsWithDup(nums=[4, 4, 4, 1, 4])) != 10: print('err-15')
