#!/usr/bin/python3

"""
4. Median of Two Sorted Arrays
Difficulty: Hard

Success
Runtime: 108 ms, faster than 22.11% of Python3 online submissions
Memory Usage: 14.5 MB, less than 79.57% of Python3 online submissions

"""
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if (len(nums1) == 0) and (len(nums2) == 0): return None
        
        result_list = []
        while True:
            if (len(nums1) == 0) and (len(nums2) == 0): break
            if len(nums1) == 0:
                result_list += nums2
                break
            if len(nums2) == 0:
                result_list += nums1
                break

            if nums1[0] < nums2[0]:
                result_list.append(nums1[0])
                nums1.pop(0)
            else:
                result_list.append(nums2[0])
                nums2.pop(0)

        if len(result_list) % 2 == 0:
            result = (result_list[int(len(result_list) / 2) - 1] + result_list[int(len(result_list) / 2)]) / 2
        else:
            result = result_list[int(len(result_list) / 2)]

        return result


sol = Solution()
print(sol.findMedianSortedArrays(nums1=[], nums2=[]))

if sol.findMedianSortedArrays(nums1=[1, 3], nums2=[2]) != 2: print('err-1')
if sol.findMedianSortedArrays(nums1=[1, 2], nums2=[3, 4]) != 2.5: print('err-2')
if sol.findMedianSortedArrays(nums1=[0, 0], nums2=[0, 0]) != 0: print('err-3')
if sol.findMedianSortedArrays(nums1=[], nums2=[1]) != 1: print('err-4')
if sol.findMedianSortedArrays(nums1=[2], nums2=[]) != 2: print('err-5')
