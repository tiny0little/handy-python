#!/usr/bin/python3
"""
57. Insert Interval
Difficulty: Medium


"""
from typing import List
import time


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        intervals_len = len(intervals)
        if intervals_len == 0: return [newInterval]
        if (intervals_len == 1) and (max(intervals[0]) >= min(newInterval)) and (min(intervals[0]) <= max(newInterval)):
            return [[min(newInterval[0], intervals[0][0]), max(intervals[0][1], newInterval[1])]]

        result = []
        start_idx = -1
        for i in range(intervals_len):
            if start_idx == -1:
                if ((newInterval[0] >= intervals[i][0]) and (newInterval[0] <= intervals[i][1])) \
                        or ((newInterval[0] < intervals[i][0]) and (newInterval[1] > intervals[i][1])):
                    start_idx = min(newInterval[0], intervals[i][0])
                else:
                    result.append(intervals[i])
            else:
                if newInterval[1] < intervals[i][0]:
                    end_idx = newInterval[1]
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
        return result


sol = Solution()
stime = time.time()
print(sol.insert(intervals=[[1, 5], [6, 8]], newInterval=[0, 9]))  # -> [[0,9]]
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
