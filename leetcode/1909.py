#!/usr/bin/python3

"""
1909. Remove One Element to Make the Array Strictly Increasing
https://leetcode.com/contest/biweekly-contest-55/problems/remove-one-element-to-make-the-array-strictly-increasing/

Difficulty: Easy
Status: Accepted
Runtime: 504 ms
Memory Usage: 14.4 MB
"""

from typing import List


class Solution:
    def is_strictly_increasing(self, nums: List[int]) -> bool:
        for i in range(1, len(nums)):
            if nums[i] <= nums[i - 1]:
                return False
        return True

    def canBeIncreasing(self, nums: List[int]) -> bool:
        if self.is_strictly_increasing(nums): return True
        for i in range(len(nums)):
            candidate = nums[:]
            candidate.pop(i)
            if self.is_strictly_increasing(candidate): return True
        return False


sol = Solution()

nums = [1, 2, 3]
print(sol.canBeIncreasing(nums=nums))
