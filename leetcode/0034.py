#!/usr/bin/python3
"""
34. Find First and Last Position of Element in Sorted Array
Difficulty: Medium

Success
Runtime: 156 ms, faster than 5.21% of Python3 online submissions
Memory Usage: 15.5 MB, less than 11.04% of Python3 online submissions
"""
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        result = [-1, -1]
        i = 0
        while i < len(nums):
            if target == nums[i]:
                start_idx = i
                while target == nums[i]:
                    if i < len(nums) - 1:
                        i += 1
                    else:
                        i += 1
                        break
                result = [start_idx, i - 1]
                break
            if target < nums[i]: break
            i += 1

        return result


sol = Solution()
print(sol.searchRange(nums=[2, 2], target=2))

if sol.searchRange(nums=[5, 7, 7, 8, 8, 10], target=8) != [3, 4]: print('err-1')
if sol.searchRange(nums=[5, 7, 7, 8, 8, 10], target=6) != [-1, -1]: print('err-2')
if sol.searchRange(nums=[], target=0) != [-1, -1]: print('err-3')
if sol.searchRange(nums=[1], target=1) != [0, 0]: print('err-4')
if sol.searchRange(nums=[2, 2], target=2) != [0, 1]: print('err-5')
