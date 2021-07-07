#!/usr/bin/python3
"""
1904. The Number of Full Rounds You Have Played
Difficulty: Medium

"""


class Solution:
    def numberOfRounds(self, startTime: str, finishTime: str) -> int:
        result = 0
        start_hour = int(startTime[:2])
        finish_hour = int(finishTime[:2])

        if finish_hour > start_hour:
            result = (finish_hour - start_hour) * 4
        elif start_hour > finish_hour:
            result = (24 - start_hour + finish_hour) * 4

        start_min = int(startTime[-2:])
        
        finish_min = int(finishTime[-2:])

        if finish_hour == start_hour:
            result += finish_min - start_min
        else:
            result += finish_min + start_min

        return result


sol = Solution()
print(sol.numberOfRounds(startTime="12:01", finishTime="12:47"))

# if sol.numberOfRounds(startTime="12:01", finishTime="12:44") != 1: print('err-1')
# if sol.numberOfRounds(startTime="20:00", finishTime="06:00") != 40: print('err-2')
# if sol.numberOfRounds(startTime="00:00", finishTime="23:59") != 95: print('err-3')
