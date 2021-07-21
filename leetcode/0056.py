#!/usr/bin/python3
"""
56. Merge Intervals
Difficulty: Medium

Success
Runtime: 96 ms, faster than 29.73% of Python3 online submissions for Merge Intervals.
Memory Usage: 16.2 MB, less than 54.45% of Python3 online submissions for Merge Intervals.
"""
from typing import List
import time


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        intervals_len = len(intervals)
        result = []

        i = 0
        while i < intervals_len:
            result0 = [intervals[i]]

            # let's see how many intervals overlap
            j = i + 1
            while j < intervals_len:
                if result0[-1][1] >= intervals[j][0]:
                    result0.append([min(result0[-1][0], intervals[j][0]), max(result0[-1][1], intervals[j][1])])
                else:
                    break
                j += 1

            i = j
            result.append(result0[-1])
        return result


sol = Solution()
stime = time.time()
print(sol.merge(intervals=[[1, 4], [0, 2], [3, 5]]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.merge(intervals=[[1, 3], [2, 6], [8, 10], [15, 18]]) != [[1, 6], [8, 10], [15, 18]]: print('err-1')
if sol.merge(intervals=[[1, 4], [2, 3]]) != [[1, 4]]: print('err-40')
if sol.merge(intervals=[[1, 4], [0, 2], [3, 5]]) != [[0, 5]]: print('err-44')
