#!/usr/bin/python3.8

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        output = [[]]

        for num in nums:
            output += [curr + [num] for curr in output]

        return output


sol = Solution()
print(sol.subsets(nums=[1, 2, 3]))
