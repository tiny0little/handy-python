#!/usr/bin/python3
"""
128. Longest Consecutive Sequence
"""
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums.sort()
        result = 1
        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] == 1:
                result += 1
            else:
                break
        return result


sol = Solution()
print(sol.longestConsecutive(nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
