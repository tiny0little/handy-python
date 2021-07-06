#!/usr/bin/python3
"""
128. Longest Consecutive Sequence
Difficulty: Medium
"""
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if len(nums) <= 1: return len(nums)

        nums_gaps = [0] * len(nums)
        result_start_idx = 0
        result_end_idx = 1
        candidate_start_idx = 0
        candidate_end_idx = 1
        nums.sort()

        nums_gaps[0] = 1
        for i in range(1, len(nums)):
            nums_gaps[i] = nums[i] - nums[i - 1]
            if min(nums[candidate_start_idx:i]) == 0:
                zero_delta = 1
            else:
                zero_delta = 0
            if sum(nums_gaps[candidate_start_idx:i]) == len(nums_gaps[candidate_start_idx:i]) - zero_delta:
                candidate_end_idx = i
            else:
                candidate_start_idx = i
            if candidate_end_idx - candidate_start_idx > result_end_idx - result_start_idx:
                result_start_idx = candidate_start_idx
                result_end_idx = candidate_end_idx

        print(nums[result_start_idx:result_end_idx])
        return result_end_idx - result_start_idx


sol = Solution()
print(sol.longestConsecutive(nums=[100, 1, 4, 200, 1, 3, 2]))
# nums = [100,4,200,1,3,2] -> 4
# nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1] -> 9
# nums=[0,0] -> 1
