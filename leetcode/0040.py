#!/usr/bin/python3
"""
40. Combination Sum II
Difficulty: Medium

Success
Runtime: 172 ms, faster than 11.66% of Python3 online submissions
Memory Usage: 14.4 MB, less than 19.42% of Python3 online submissions
"""
from typing import List
import time


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        def sublist(lst1, lst2):
            ls1 = [element for element in lst1 if element in lst2]
            ls2 = [element for element in lst2 if element in lst1]
            if set(ls1) == set(ls2):
                for el in lst1:
                    if lst1.count(el) > lst2.count(el):
                        return False
            else:
                return False
            return True

        #

        dp_list = [[] for _ in range(target + 1)]

        for candi in candidates:
            for i in range(candi, len(dp_list)):
                if i == candi:
                    if [candi] not in dp_list[candi]: dp_list[candi].append([candi])
                for dp0 in dp_list[i - candi]:
                    l0 = sorted(dp0 + [candi])
                    if (sublist(l0, candidates)) and l0 not in dp_list[i]: dp_list[i].append(l0)

        return dp_list[-1]


sol = Solution()

# stime = time.time()
# print(sol.combinationSum2(candidates=[10, 1, 2, 7, 6, 1, 5], target=8))
# print(f'runtime: {time.time() - stime:.1f}sec')
#
# stime = time.time()
# print(sol.combinationSum2(candidates=[2, 5, 2, 1, 2], target=5))
# print(f'runtime: {time.time() - stime:.1f}sec')

stime = time.time()
print(sol.combinationSum2(candidates=[1, 1], target=1))
print(f'runtime: {time.time() - stime:.1f}sec')
