#!/usr/bin/python3.8

"""
8 String to Integer (atoi)
Difficulty: Medium
Runtime: 36 ms, faster than 60.39% of Python3 online submissions for String to Integer (atoi).
Memory Usage: 14.1 MB, less than 80.23% of Python3 online submissions for String to Integer (atoi).
"""


class Solution:
    def myAtoi(self, s: str) -> int:
        result_str = ''
        sign_in_result = False
        numbers_in_result = False
        s = s.strip()
        for l in s:
            if not sign_in_result and (l in '+-'):
                result_str += l
                sign_in_result = True
                continue
            if sign_in_result and (l in '+-'):
                break
            if l.isnumeric():
                result_str += l
                numbers_in_result = True
                sign_in_result = True
            if l == ' ':
                if numbers_in_result:
                    break
                if sign_in_result and not numbers_in_result:
                    result_str = '0'
                    break
            if not l.isnumeric():
                break

        # print(result_str)

        if len(result_str) == 0: result_str = '0'
        if result_str in '+-': result_str = '0'

        result = int(result_str)
        if result < -2 ** 31: result = -2 ** 31
        if result > (2 ** 31) - 1: result = (2 ** 31) - 1

        return result

#
#

sol = Solution()
print(sol.myAtoi(s="  -4 13"))
