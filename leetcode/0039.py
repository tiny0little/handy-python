#!/usr/bin/python3
"""
39. Combination Sum
Difficulty: Medium

Success
Runtime: 44 ms, faster than 99.07% of Python3 online submissions
Memory Usage: 14.8 MB, less than 8.29% of Python3 online submissions
"""
from typing import List
import time


class Solution:

    def combinationSum_dp(self, candidates: List[int], target: int) -> List[List[int]]:
        dp_list = [[] for _ in range(target + 1)]
        for c in candidates:
            for i in range(c, len(dp_list)):
                if i == c: dp_list[i].append([c])
                for dp0 in dp_list[i - c]:
                    dp_list[i].append(dp0 + [c])

        return dp_list[-1]

    def combinationSum_bruteforce(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        result = []
        max_weight_mask = [0] * len(candidates)
        for i in range(len(max_weight_mask)): max_weight_mask[i] = int(target / candidates[i])
        weight_mask = [0] * len(max_weight_mask)

        while weight_mask != max_weight_mask:
            result0 = []
            weight_mask[0] += 1
            overflow = False
            for i in range(len(weight_mask)):
                if overflow:
                    weight_mask[i] += 1
                    overflow = False
                if weight_mask[i] > max_weight_mask[i]:
                    weight_mask[i] = 0
                    overflow = True
                if not overflow: break

            for i in range(len(weight_mask)):
                for j in range(weight_mask[i]): result0.append(candidates[i])

            if sum(result0) == target: result.append(result0)

        return result


sol = Solution()

# stime = time.time()
# print(sol.combinationSum(candidates=[2, 3, 6, 7], target=7))
# print(f'runtime: {time.time() - stime:.1f}sec')
#
# stime = time.time()
# print(sol.combinationSum(candidates=[2, 3, 5], target=8))
# print(f'runtime: {time.time() - stime:.1f}sec')
#
# print(sol.combinationSum(candidates=[2], target=1))
# print(sol.combinationSum(candidates=[1], target=1))
# print(sol.combinationSum(candidates=[1], target=2))


stime = time.time()
result = sol.combinationSum_dp(candidates=[8, 10, 6, 3, 4, 12, 11, 5, 9], target=28)
print(result)
print(f'runtime: {time.time() - stime:.1f}sec')
