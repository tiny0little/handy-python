#!/usr/bin/python3.8

"""
43. Multiply Strings
https://leetcode.com/problems/multiply-strings/

Runtime: 32 ms, faster than 85.06% of Python3 online submissions for Multiply Strings.
Memory Usage: 14.2 MB, less than 54.83% of Python3 online submissions for Multiply Strings
"""


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if not num1.isnumeric() or not num2.isnumeric(): return '0'

        num1 = num1[::-1]
        num2 = num2[::-1]
        num1int = 0
        num2int = 0

        for i in range(len(num1)): num1int += int(num1[i]) * 10 ** i
        for i in range(len(num2)): num2int += int(num2[i]) * 10 ** i

        return str(num1int * num2int)


#
#

sol = Solution()
print(sol.multiply(num1="123", num2="456"))
