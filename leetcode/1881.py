#!/usr/bin/python3

"""
1881. Maximum Value after Insertion
Difficulty: Medium
Status: Accepted Runtime: 2068 ms Memory Usage: 15.5 MB
"""


class Solution:
    def maxValue(self, n: str, x: int) -> str:
        if int(n) > 0:
            for i in range(len(n)):
                if int(n[i]) < x:
                    return n[:i] + str(x) + n[i:]
            return n + str(x)
        else:
            for i in range(1, len(n)):
                if int(n[i]) > x:
                    r1 = int(n[:i] + str(x) + n[i:])
                    r2 = int(n[:i + 1] + str(x) + n[i + 1:])
                    return str(max(r1, r2))
            return n + str(x)


sol = Solution()
print(sol.maxValue(n="469975787943862651173569913153377", x=3))

"""
test cases
'-13',2 -> -123
'-648468153646', 5 -> -5648468153646
'469975787943862651173569913153377',3 -> 4699757879438632651173569913153377
"""
