#!/usr/bin/python3
"""
31. Next Permutation
Difficulty: Medium

"""
from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:


sol = Solution()
print(sol.nextPermutation(nums=[1, 2, 3]))

if (sol.nextPermutation(nums=[1, 2, 3])) != [1, 3, 2]: print('err-1')
