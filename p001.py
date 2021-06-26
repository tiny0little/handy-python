#!/usr/bin/python3.8

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        for i in range(len(nums)):
            for j in range(i + 1):
                print(nums[j], end=' ')
            print()


sol = Solution()
print(sol.subsets(nums=[1, 2, 3]))
