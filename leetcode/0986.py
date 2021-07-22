#!/usr/bin/python3
"""
986. Interval List Intersections
Difficulty: Medium

brute force
Runtime: 2344 ms, faster than 5.33% of Python3 online submissions for Interval List Intersections
Memory Usage: 14.9 MB, less than 80.48% of Python3 online submissions for Interval List Intersections

two pointers
Runtime: 928 ms, faster than 5.33% of Python3 online submissions for Interval List Intersections
Memory Usage: 15.1 MB, less than 39.03% of Python3 online submissions for Interval List Intersections
"""
from typing import List
import time


class Solution:

    def is_overlap(self, lst1: List[int], lst2: List[int]) -> bool:
        if (lst1[0] >= lst2[0]) and (lst1[0] <= lst2[1]): return True
        if (lst2[0] >= lst1[0]) and (lst2[0] <= lst1[1]): return True
        return False

    def get_overlap(self, lst1: List[int], lst2: List[int]) -> List[int]:
        start_idx = max(lst1[0], lst2[0])
        end_idx = min(lst1[1], lst2[1])
        return [start_idx, end_idx]

    def intervalIntersection_bf(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        firstList_len = len(firstList)
        secondList_len = len(secondList)
        if (firstList_len == 0) or (secondList_len == 0): return []

        result = []
        for fl_idx in range(firstList_len):
            for sl_idx in range(secondList_len):
                if self.is_overlap(firstList[fl_idx], secondList[sl_idx]):
                    result.append(self.get_overlap(firstList[fl_idx], secondList[sl_idx]))

        return result

    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        firstList_len = len(firstList)
        secondList_len = len(secondList)
        if (firstList_len == 0) or (secondList_len == 0): return []

        result = []
        fl_idx = 0
        sl_idx = 0
        while True:
            for f in range(-2, 2):
                for s in range(-2, 2):
                    if (fl_idx + f in range(0, firstList_len)) and (sl_idx + s in range(0, secondList_len)):
                        if self.is_overlap(firstList[fl_idx + f], secondList[sl_idx + s]):
                            result0 = self.get_overlap(firstList[fl_idx + f], secondList[sl_idx + s])
                            if result0 not in result: result.append(result0)

            if (fl_idx >= firstList_len - 1) and (sl_idx >= secondList_len - 1): break

            if firstList[fl_idx][0] > secondList[sl_idx][0]:
                if sl_idx in range(0, secondList_len - 1):
                    sl_idx += 1
                else:
                    if fl_idx in range(0, firstList_len - 1): fl_idx += 1
            else:
                if fl_idx in range(0, firstList_len - 1):
                    fl_idx += 1
                else:
                    if sl_idx in range(0, secondList_len - 1): sl_idx += 1

        return result


sol = Solution()
stime = time.time()
print(sol.intervalIntersection(firstList=[[0, 4], [5, 6], [9, 10], [11, 15], [17, 19]],
                               secondList=[[1, 11], [12, 14]]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.intervalIntersection(firstList=[[0, 2], [5, 10], [13, 23], [24, 25]],
                            secondList=[[1, 5], [8, 12], [15, 24], [25, 26]]) != \
        [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]: print('err-1')
if sol.intervalIntersection(firstList=[[1, 7]], secondList=[[3, 10]]) != [[3, 7]]: print('err-2')
if sol.intervalIntersection(firstList=[[5, 10]], secondList=[[3, 10]]) != [[5, 10]]: print('err-6')
if sol.intervalIntersection(firstList=[[8, 15]], secondList=[[2, 6], [8, 10], [12, 20]]) != [[8, 10], [12, 15]]:
    print('err-12')
if sol.intervalIntersection(firstList=[[0, 4], [5, 6], [9, 10], [11, 15], [17, 19]],
                            secondList=[[1, 11], [12, 14]]) != [[1, 4], [5, 6], [9, 10], [11, 11], [12, 14]]: \
        print('err-61')
