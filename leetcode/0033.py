#!/usr/bin/python3
"""
33. Search in Rotated Sorted Array

"""
from typing import List


class Solution:
    def list_avg(self, nums: List[int]) -> float:
        if len(nums) == 0: return 1
        return sum(nums) / len(nums)

    def search(self, nums: List[int], target: int) -> int:
        if len(nums) == 0: return -1

        search_gap = 20
        avg_list_elements_gap_list = []
        rotated = -nums[0]

        for i in range(search_gap * 2):
            if (i >= 0) and (i < len(nums) - 1):
                if abs(nums[i] - nums[i + 1]) < 10 * self.list_avg(avg_list_elements_gap_list):
                    avg_list_elements_gap_list.append(abs(nums[i] - nums[i + 1]))

        avg_list_elements_gap = self.list_avg(avg_list_elements_gap_list)

        for i in range(-search_gap, search_gap):
            idx = i + int(rotated / avg_list_elements_gap) + target
            if idx > len(nums): idx = idx - len(nums)
            if (idx >= 0) and (idx < len(nums)):
                if nums[idx] == target:
                    return idx
        return -1


sol = Solution()
print(sol.search(
    nums=[266, 267, 268, 269, 271, 278, 282, 292, 293, 298, 6, 9, 15, 19, 21, 26, 33, 35, 37, 38, 39, 46, 49, 54, 65,
          71, 74, 77, 79, 82, 83, 88, 92, 93, 94, 97, 104, 108, 114, 115, 117, 122, 123, 127, 128, 129, 134, 137, 141,
          142, 144, 147, 150, 154, 160, 163, 166, 169, 172, 173, 177, 180, 183, 184, 188, 198, 203, 208, 210, 214, 218,
          220, 223, 224, 233, 236, 241, 243, 253, 256, 257, 262, 263], target=208))

if sol.search(nums=[4, 5, 6, 7, 0, 1, 2], target=0) != 4: print('err-1')
if sol.search(nums=[4, 5, 6, 7, 0, 1, 2], target=3) != -1: print('err-2')
if sol.search(nums=[1], target=0) != -1: print('err-3')
if sol.search(nums=[6, 7, 1, 2, 3, 4, 5], target=6) != 0: print('err-4')
if sol.search(nums=[9, 0, 4, 8], target=0) != 1: print('err-5')
if sol.search(nums=[15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], target=25) != 4: print('err-6')
if sol.search(
        nums=[266, 267, 268, 269, 271, 278, 282, 292, 293, 298, 6, 9, 15, 19, 21, 26, 33, 35, 37, 38, 39, 46, 49, 54,
              65,
              71, 74, 77, 79, 82, 83, 88, 92, 93, 94, 97, 104, 108, 114, 115, 117, 122, 123, 127, 128, 129, 134, 137,
              141,
              142, 144, 147, 150, 154, 160, 163, 166, 169, 172, 173, 177, 180, 183, 184, 188, 198, 203, 208, 210, 214,
              218,
              220, 223, 224, 233, 236, 241, 243, 253, 256, 257, 262, 263], target=208) != 67: print('err-7')

if sol.search(
    nums=[57, 58, 59, 62, 63, 66, 68, 72, 73, 74, 75, 76, 77, 78, 80, 81, 86, 95, 96, 97, 98, 100, 101, 102, 103, 110,
          119, 120, 121, 123, 125, 126, 127, 132, 136, 144, 145, 148, 149, 151, 152, 160, 161, 163, 166, 168, 169, 170,
          173, 174, 175, 178, 182, 188, 189, 192, 193, 196, 198, 199, 200, 201, 202, 212, 218, 219, 220, 224, 225, 229,
          231, 232, 234, 237, 238, 242, 248, 249, 250, 252, 253, 254, 255, 257, 260, 266, 268, 270, 273, 276, 280, 281,
          283, 288, 290, 291, 292, 294, 295, 298, 299, 4, 10, 13, 15, 16, 17, 18, 20, 22, 25, 26, 27, 30, 31, 34, 38,
          39, 40, 47, 53, 54], target=30) != 113: print('err-8')
