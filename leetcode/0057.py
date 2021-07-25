#!/usr/bin/python3
"""
57. Insert Interval
Difficulty: Medium

Success
Runtime: 76 ms, faster than 87.73% of Python3 online submissions for Insert Interval
Memory Usage: 17.7 MB, less than 32.74% of Python3 online submissions for Insert Interval
"""
from typing import List
import time


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        intervals_len = len(intervals)
        if intervals_len == 0: return [newInterval]
        # newInterval in front of intervals
        if max(newInterval) < min(intervals[0]): return [newInterval] + intervals
        # newInterval after intervals
        if min(newInterval) > max(intervals[-1]): return intervals + [newInterval]
        # newInterval covers all intervals
        if (newInterval[0] < intervals[0][0]) and (newInterval[1] > intervals[-1][1]): return [newInterval]

        if intervals_len == 1:
            # intervals cover newInterval
            if (intervals[0][0] < newInterval[0]) and (intervals[0][1] > newInterval[1]): return intervals
            # newInterval overlaps intervals from left
            if (newInterval[0] >= intervals[0][0]) and (newInterval[0] <= intervals[0][1]):
                return [[intervals[0][0], max(intervals[0][1], newInterval[1])]]
            # newInterval overlaps intervals from right
            if (newInterval[0] <= intervals[0][0]) and (newInterval[1] <= intervals[0][1]):
                return [[min(newInterval[0], intervals[0][0]), max(newInterval[1], intervals[0][1])]]

        result = []
        start_idx = -1
        end_idx = -1
        for i in range(intervals_len):
            if start_idx == -1:
                # newInterval fits between intervals
                if (i > 0) and (newInterval[0] > intervals[i - 1][1]) and (newInterval[1] < intervals[i][0]):
                    result.append(newInterval)
                    for j in range(i, len(intervals)): result.append(intervals[j])
                    start_idx = 0
                    end_idx = 0
                    break
                if ((newInterval[0] >= intervals[i][0]) and (newInterval[0] <= intervals[i][1])) or \
                        (newInterval[0] < intervals[i][0]):
                    start_idx = min(newInterval[0], intervals[i][0])
                    continue
                result.append(intervals[i])
            else:
                if newInterval[1] < intervals[i][0]:
                    end_idx = max(newInterval[1], intervals[i - 1][1])
                    result.append([start_idx, end_idx])
                    for j in range(i, len(intervals)):
                        if end_idx < intervals[j][1]: result.append(intervals[j])
                    break
                if (newInterval[1] >= intervals[i][0]) and (newInterval[1] <= intervals[i][1]):
                    end_idx = intervals[i][1]
                    result.append([start_idx, end_idx])
                    for j in range(i, len(intervals)):
                        if end_idx < intervals[j][1]: result.append(intervals[j])
                    break
        if start_idx == -1:
            if max(newInterval) < min(intervals[0]):
                result = [newInterval] + result
            else:
                result.append(newInterval)
        if (start_idx != -1) and (end_idx == -1):
            if newInterval[1] >= intervals[-1][0]:
                end_idx = max(newInterval[1], intervals[-1][1])
                result.append([start_idx, end_idx])
            else:
                result.append(newInterval)
                result.append(intervals[-1])

        return result


sol = Solution()
stime = time.time()
print(sol.insert(intervals=[[0, 10], [14, 14], [15, 20]], newInterval=[11, 11]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.insert(intervals=[[1, 3], [6, 9]], newInterval=[2, 5]) != [[1, 5], [6, 9]]: print('err-1')
if sol.insert(intervals=[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], newInterval=[4, 8]) != [[1, 2], [3, 10],
                                                                                             [12, 16]]: print('err-2')
if sol.insert(intervals=[], newInterval=[5, 7]) != [[5, 7]]: print('err-3')
if sol.insert(intervals=[[1, 5]], newInterval=[2, 3]) != [[1, 5]]: print('err-4')
if sol.insert(intervals=[[1, 5]], newInterval=[2, 7]) != [[1, 7]]: print('err-5')
if sol.insert(intervals=[[1, 5]], newInterval=[6, 8]) != [[1, 5], [6, 8]]: print('err-6')
if sol.insert(intervals=[[1, 5]], newInterval=[0, 0]) != [[0, 0], [1, 5]]: print('err-88')
if sol.insert(intervals=[[1, 5], [6, 8]], newInterval=[0, 9]) != [[0, 9]]: print('err-90')
if sol.insert(intervals=[[0, 5], [8, 9]], newInterval=[3, 4]) != [[0, 5], [8, 9]]: print('err-93')
if sol.insert(intervals=[[0, 2], [3, 9]], newInterval=[6, 8]) != [[0, 2], [3, 9]]: print('err-104')
if sol.insert(intervals=[[1, 5], [9, 12]], newInterval=[0, 4]) != [[0, 5], [9, 12]]: print('err-146')
if sol.insert(intervals=[[3, 5], [12, 15]], newInterval=[6, 6]) != [[3, 5], [6, 6], [12, 15]]: print('err-149')
if sol.insert(intervals=[[0, 10], [14, 14], [15, 20]], newInterval=[11, 11]) != [[0, 10], [11, 11], [14, 14],
                                                                                 [15, 20]]: print('err-152')
