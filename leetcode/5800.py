#!/usr/bin/python3

"""
5800. Build Array from Permutation

"""
from typing import List


class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        ans = []
        for i in range(len(nums)):
            ans.append(nums[nums[i]])

        return ans


sol = Solution()
print(sol.buildArray(nums=[5, 0, 1, 2, 3, 4]))
