#!/usr/bin/python3
"""
216. Combination Sum III
Difficulty: Medium

Success
Runtime: 1560 ms, faster than 5.35% of Python3 online submissions
Memory Usage: 14.6 MB, less than 5.27% of Python3 online submissions
"""
from typing import List
import time


class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        num_set = [_ for _ in range(1, 10)]
        result = []
        cur_result = []

        def backtracker(k0: int):
            if k0 == 0:
                if (sum(cur_result) == n) and (sorted(cur_result) not in result): result.append(sorted(cur_result)[:])
                return

            for i in range(len(num_set)):
                if num_set[i] not in cur_result:
                    cur_result.append(num_set[i])
                    backtracker(k0 - 1)
                    cur_result.pop(-1)

        backtracker(k)
        return result


sol = Solution()
stime = time.time()
print(sol.combinationSum3(k=9, n=45))
print(f'runtime: {time.time() - stime:.2f}sec')
