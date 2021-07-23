#!/usr/bin/python3
"""
128. Longest Consecutive Sequence
Difficulty: Medium

Success
Runtime: 220 ms, faster than 61.68% of Python3 online submissions for Longest Consecutive Sequence.
Memory Usage: 32.4 MB, less than 13.97% of Python3 online submissions for Longest Consecutive Sequence.
"""
from typing import List
import time


class Solution:
    def longestConsecutive_bf(self, nums: List[int]) -> int:
        already_tested = []
        result = 0
        nums.sort()
        nums_len = len(nums)
        for i in range(nums_len):
            if nums[i] not in already_tested:
                candidate = 1
                already_tested.append(nums[i])
                for j in range(1, nums_len):
                    if nums[i] + j in nums:
                        already_tested.append(nums[i] + j)
                        candidate += 1
                    else:
                        break
                if candidate > result: result = candidate
        return result

    def longestConsecutive(self, nums: List[int]) -> int:
        hash_list = {}
        result = 1
        nums = list(set(nums))
        nums.sort()
        nums_len = len(nums)
        if nums_len == 0: return 0
        for i in range(nums_len): hash_list[nums[i]] = i
        i = 0
        while i < nums_len:
            candidate = result
            for j in range(result, nums_len):
                if nums[i] + j in hash_list:
                    if hash_list[nums[i] + j] == i + j: candidate += 1
                else:
                    break
            if candidate > result:
                result = candidate
                i += j
            else:
                i += 1

        return result


sol = Solution()
stime = time.time()
nums0 = [_ for _ in range(100000, -100000, -1)]
print(sol.longestConsecutive(nums=nums0))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.longestConsecutive(nums=[100, 4, 200, 1, 3, 2]) != 4: print('err-1')
if sol.longestConsecutive(nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) != 9: print('err-2')
if sol.longestConsecutive(nums=[]) != 0: print('err-69')
