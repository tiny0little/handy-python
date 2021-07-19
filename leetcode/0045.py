#!/usr/bin/python3
"""
45. Jump Game II
Difficulty: Medium

Success
Runtime: 6300 ms, faster than 16.64% of Python3 online submissions for Jump Game II
Memory Usage: 16.3 MB, less than 6.64% of Python3 online submissions for Jump Game II
"""
from typing import List
import time


class Solution:
    def jump(self, nums: List[int]) -> int:
        nums_len = len(nums)
        if nums_len <= 1: return 0
        dp_list = {0: 0}

        for i in range(nums_len):
            for j in range(1, nums[i] + 1):
                n0 = dp_list[i] + 1
                if j + i in dp_list:
                    if n0 < dp_list[j + i]:
                        dp_list[j + i] = n0
                else:
                    dp_list[j + i] = n0

        return dp_list[nums_len - 1]


sol = Solution()
stime = time.time()
print(sol.jump(nums=[2, 3, 0, 1, 4]))
print(f'>>> runtime: {time.time() - stime:.2f}sec')

if sol.jump(nums=[2, 3, 1, 1, 4]) != 2: print('err-1')
if sol.jump(nums=[2, 3, 0, 1, 4]) != 2: print('err-2')
if sol.jump(nums=[0]) != 0: print('err-3')
