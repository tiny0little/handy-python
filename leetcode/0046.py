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
        return self.permute(nums)

    def permute(self, nums: List[int]) -> List[List[int]]:
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


sol = Solution()
stime = time.time()
print(sol.permute(nums=[1, 1, 2]))
print(f'>>> runtime: {time.time() - stime:.2f}sec')
