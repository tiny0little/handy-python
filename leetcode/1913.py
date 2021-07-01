#!/usr/bin/python3.8

"""
1913. Maximum Product Difference Between Two Pairs
247th LeetCode Weekly Contest
https://leetcode.com/contest/weekly-contest-247/problems/maximum-product-difference-between-two-pairs/

"""

from typing import List


class Solution:
    def maxProductDifference(self, nums: List[int]) -> int:
        nums.sort()
        return (nums[-1] * nums[-2]) - (nums[0] * nums[1])


#
#

sol = Solution()
print(sol.maxProductDifference(nums=[5, 6, 2, 7, 4]))
