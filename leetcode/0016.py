#!/usr/bin/python3

"""
16. 3Sum Closest
Difficulty: Medium

"""
from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        if (len(nums)) <= 3: return sum(nums)

        nums.sort()
        result_idx = []
        result_sum = nums[0] + nums[1] + nums[2]
        candidate_idx = [0, 1, 2]  # 0 = left_pointer 1 = mid_pointer 2 = right pointer
        candidate_sum = nums[0]
        gap = 7

        trigger = False
        for i in range(len(nums)):
            if ((target >= 0) and (target <= nums[i])) or ((target < 0) and (target >= nums[i])):
                candidate_idx[1] = i - gap
                trigger = True
                break
        if not trigger: candidate_idx[1] = len(nums) - gap
        if candidate_idx[1] < 1: candidate_idx[1] = 1

        steps_forward = gap * 2
        while steps_forward > 0:
            if candidate_idx[1] >= len(nums): break
            candidate_idx[0] = candidate_idx[1]
            candidate_idx[2] = candidate_idx[1]
            for i in range(1, gap * 2):
                for j in range(1, gap * 2):
                    candidate_idx[0] = candidate_idx[1] - i
                    candidate_idx[2] = candidate_idx[1] + j
                    if candidate_idx[0] < 0: candidate_idx[0] = 0
                    if candidate_idx[2] >= len(nums): candidate_idx[2] = len(nums) - 1
                    if (candidate_idx[0] != candidate_idx[1]) and (candidate_idx[0] != candidate_idx[2]) and (
                            candidate_idx[1] != candidate_idx[2]):
                        candidate_sum = nums[candidate_idx[0]] + nums[candidate_idx[1]] + nums[candidate_idx[2]]
                        if abs(candidate_sum - target) < abs(result_sum - target):
                            result_sum = candidate_sum
                            result_idx = candidate_idx[:]
            candidate_idx[1] += 1

            steps_forward -= 1

        print(nums)
        print(result_idx)
        return result_sum


sol = Solution()
print(sol.threeSumClosest(
    nums=[0, -16, -11, -4, 6, 20, -17, 10, 14, -11, -16, 17, -14, -11, 8, -4, 0, -2, 10, 15, 0, -2, -3, 19, 17, -18, 8,
          -16, -4, -16, -20, 16, -16, 5, -3, -18, -12, -18, -9, 11, 3, -14, -18, 8, 11, -9, -1, 6, 1, -17, -9, -7, 11,
          -10, 18, -1, 4, -8, 1, -20, -19, -19, 12, 13, 14, 15, 0, 18, 3, 8, -4, 18, -1, 6, -19, -11, 11, 14, 12, 11,
          -15, 2, 4, -1, 5, 3, -17, 15, -1, -15, 3, 16, -11, -14, 14, 4, -7, -20, -2, -14, -8, -12, -12, 18, 4, -12,
          16], target=-31))

# if sol.threeSumClosest(nums=[1, 1, 1, 1], target=0) != 3: print('err-1')
# if sol.threeSumClosest(nums=[-1, 2, 1, -4], target=1) != 2: print('err-2')
# if sol.threeSumClosest(nums=[1, 2, 4, 8, 16, 32, 64, 128], target=82) != 82: print('err-3')
# if sol.threeSumClosest(nums=[0, 2, 1, -3], target=1) != 0: print('err-4')
# if sol.threeSumClosest(nums=[0, 5, -1, -2, 4, -1, 0, -3, 4, -5], target=1) != 1: print('err-5')
# if sol.threeSumClosest(nums=[-10, 0, -2, 3, -8, 1, -10, 8, -8, 6, -7, 0, -7, 2, 2, -5, -8, 1, -4, 6],
#                        target=18) != 17: print('err-6')
# if sol.threeSumClosest(
#         nums=[0, -16, -11, -4, 6, 20, -17, 10, 14, -11, -16, 17, -14, -11, 8, -4, 0, -2, 10, 15, 0, -2, -3, 19, 17, -18,
#               8,
#               -16, -4, -16, -20, 16, -16, 5, -3, -18, -12, -18, -9, 11, 3, -14, -18, 8, 11, -9, -1, 6, 1, -17, -9, -7,
#               11,
#               -10, 18, -1, 4, -8, 1, -20, -19, -19, 12, 13, 14, 15, 0, 18, 3, 8, -4, 18, -1, 6, -19, -11, 11, 14, 12,
#               11,
#               -15, 2, 4, -1, 5, 3, -17, 15, -1, -15, 3, 16, -11, -14, 14, 4, -7, -20, -2, -14, -8, -12, -12, 18, 4, -12,
#               16], target=-31) != -31: print('err-7')
