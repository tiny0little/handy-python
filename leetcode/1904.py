#!/usr/bin/python3
"""
1904. The Number of Full Rounds You Have Played
Difficulty: Medium
Success
Runtime: 28 ms, faster than 86.71% of Python3 online submissions
Memory Usage: 14.4 MB, less than 29.32% of Python3 online submissions
"""


class Solution:

    def numberOfRounds(self, startTime: str, finishTime: str) -> int:
        # counting hours
        start_hour = int(startTime[:2])
        finish_hour = int(finishTime[:2])
        start_min = int(startTime[-2:])
        finish_min = int(finishTime[-2:])
        result = 24 + finish_hour - start_hour
        if result > 24:
            result -= 24
        elif (result == 24) and (finish_min > start_min):
            result -= 24

        # counting minutes
        if start_min % 15 != 0: start_min += 15 - start_min % 15
        finish_min -= finish_min % 15

        result *= 60
        result += finish_min - start_min

        if result < 0: result = 0
        return int(result / 15)


sol = Solution()
print(sol.numberOfRounds(startTime="00:01", finishTime="00:02"))

if sol.numberOfRounds(startTime="12:01", finishTime="12:44") != 1: print('err-1')
if sol.numberOfRounds(startTime="20:00", finishTime="06:00") != 40: print('err-2')
if sol.numberOfRounds(startTime="00:00", finishTime="23:59") != 95: print('err-3')
if sol.numberOfRounds(startTime="00:01", finishTime="00:00") != 95: print('err-4')
if sol.numberOfRounds(startTime="00:01", finishTime="00:02") != 0: print('err-5')
if sol.numberOfRounds(startTime="00:00", finishTime="00:14") != 0: print('err-6')
