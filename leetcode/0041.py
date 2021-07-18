#!/usr/bin/python3

"""
41. First Missing Positive
Difficulty: Hard

Success
Runtime: 864 ms, faster than 20.04% of Python3 online submissions
Memory Usage: 87.1 MB, less than 5.02% of Python3 online submissions
"""
from typing import List
import time


class Solution:

    def firstMissingPositive_hash(self, nums: List[int]) -> int:
        hash_list = {}
        result = 0
        nums.sort()

        if nums[0] > 1: return 1
        if max(nums) < 0: return 1

        # building hash list
        for i in range(len(nums)):
            if nums[i] > 0: hash_list[nums[i]] = i

        if len(hash_list) == 0: return 1
        if list(hash_list)[0] > 1: return 1

        for i in list(hash_list):
            if i + 1 not in hash_list:
                return i + 1

        return max(nums) + 1

    def firstMissingPositive_bf(self, nums: List[int]) -> int:
        last_positive = 0

        nums.sort()
        for i in range(len(nums)):
            if nums[i] >= 1:
                if (nums[i] > 1) and (last_positive == 0):
                    return 1
                else:
                    if nums[i] - last_positive > 1:
                        return last_positive + 1
                    last_positive = nums[i]

        return last_positive + 1


sol = Solution()
stime = time.time()
print(sol.firstMissingPositive_hash(nums=[-1, -2, -60, 40, 43]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.firstMissingPositive_hash(nums=[1, 2, 0]) != 3: print('err-1')
if sol.firstMissingPositive_hash(nums=[3, 4, -1, 1]) != 2: print('err-2')
if sol.firstMissingPositive_hash(nums=[7, 8, 9, 11, 12]) != 1: print('err-3')
if sol.firstMissingPositive_hash(nums=[0]) != 1: print('err-4')
if sol.firstMissingPositive_hash(nums=[-5]) != 1: print('err-5')
if sol.firstMissingPositive_hash(nums=[-1, -2, -60, 40, 43]) != 1: print('err-6')
