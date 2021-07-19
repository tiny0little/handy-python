#!/usr/bin/python3
"""
46. Permutations
47. Permutations II
Difficulty: Medium

Success
Runtime: 88 ms, faster than 7.02% of Python3 online submissions for Permutations.
Memory Usage: 14.5 MB, less than 14.58% of Python3 online submissions for Permutations.

Success
Runtime: 344 ms, faster than 21.90% of Python3 online submissions for Permutations II.
Memory Usage: 14.7 MB, less than 43.38% of Python3 online submissions for Permutations II.
"""
from typing import List
import time


class Solution:
    def is_sublist(self, lst1: List, lst2: List) -> bool:
        ls1 = [element for element in lst1 if element in lst2]
        ls2 = [element for element in lst2 if element in lst1]
        if set(ls1) == set(ls2):
            for el in lst1:
                if lst1.count(el) > lst2.count(el):
                    return False
        else:
            return False
        return True

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        return self.permute_dp(nums)

    def permute_dp(self, nums: List[int]) -> List[List[int]]:
        nums_len = len(nums)
        dp_list = [[] for _ in range(nums_len + 1)]

        # dp for size=1
        for n in nums: dp_list[1].append([n])

        # dp for size=2 and up
        for i in range(2, nums_len + 1):
            for n in nums:
                for dp0 in dp_list[i - 1]:
                    dp1 = [n] + dp0
                    if (self.is_sublist(dp1, nums)) and (dp1 not in dp_list[i]): dp_list[i].append(dp1)

        return dp_list[nums_len]

    def permute_rc(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtracker(nums0: List[int], l_idx: int, r_idx: int):
            if l_idx == r_idx:
                result.append(nums0[:])
            else:
                for i in range(l_idx, r_idx + 1):
                    nums0[l_idx], nums0[i] = nums0[i], nums0[l_idx]
                    backtracker(nums0, l_idx + 1, r_idx)
                    nums0[l_idx], nums0[i] = nums0[i], nums0[l_idx]

        backtracker(nums, 0, len(nums) - 1)
        return result

    def permute_bt(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtracker(nums0: List[int], result0: List[int]):
            if len(nums0) == 0:
                result.append(result0)
            else:
                for i in range(len(nums0)):
                    backtracker(nums0[:i] + nums0[i + 1:], result0 + [nums0[i]])

        backtracker(nums, [])
        return result


sol = Solution()
nums0 = [1, 2, 3, 4, 5, 6, 7, 8]

stime = time.time()
r = sol.permute_dp(nums=nums0)
print(len(r))
print(f'>>> runtime: {time.time() - stime:.2f}sec')

stime = time.time()
r = sol.permute_rc(nums=nums0)
print(len(r))
print(f'>>> runtime: {time.time() - stime:.2f}sec')

stime = time.time()
r = sol.permute_bt(nums=nums0)
print(len(r))
print(f'>>> runtime: {time.time() - stime:.2f}sec')
