#!/usr/bin/python3

"""
65. Valid Number
https://leetcode.com/problems/valid-number/

Runtime: 28 ms, faster than 94.35% of Python3 online submissions for Valid Number.
Memory Usage: 14.4 MB, less than 29.62% of Python3 online submissions for Valid Number.
"""


class Solution:
    def isNumber(self, s: str) -> bool:
        result = True
        result_str = ''
        sign_in_result = False
        numbers_in_result = False
        dot_in_result = False
        e_in_result = False
        e_sign_in_result = False
        numbers_after_e_in_result = False

        s = s.strip()
        pre_l = ''

        for l in s:
            if not dot_in_result and (l == '.'):
                result_str += l
                pre_l = l.lower()
                dot_in_result = True
                continue
            if dot_in_result and (l == '.'):
                result = False
                break
            if l in '-+':
                if dot_in_result and not numbers_in_result:
                    result = False
                    break
                if not sign_in_result and not numbers_in_result:
                    result_str += l
                    pre_l = l.lower()
                    sign_in_result = True
                    continue
                if sign_in_result and not e_in_result:
                    result = False
                    break
                if (pre_l == 'e') and e_in_result:
                    result_str += l
                    pre_l = l.lower()
                    e_sign_in_result = True
                    continue
            if l.isnumeric():
                if e_in_result and not numbers_in_result:
                    result = False
                    break
                if e_in_result: numbers_after_e_in_result = True
                result_str += l
                pre_l = l.lower()
                numbers_in_result = True
                sign_in_result = True
                continue
            if l.lower() == 'e':
                if not e_in_result:
                    result_str += l
                    pre_l = l.lower()
                    e_in_result = True
                    dot_in_result = True
                    continue
                else:
                    result = False
                    break
            if l == ' ':
                result = False
                break
            if not l.isnumeric():
                result = False
                break

        if e_in_result and not numbers_in_result: result = False
        if e_in_result and not numbers_after_e_in_result: result = False
        if dot_in_result and not numbers_in_result: result = False

        return result


#
#

sol = Solution()
print('--- valid ---')
for st in ["2", "0089", "-0.1", "+3.14", "4.", "-.9", "2e10", "-90E3", "3e+7", "+6e-1", "53.5e93", "-123.456e789"]:
    print(st, end=' > ')
    print(sol.isNumber(st))
print()
print('--- not valid ---')
for st in [".-4", "abc", "1a", "1e", ".", "e3", "99e2.5", "--6", "-+3", "95a54e53"]:
    print(st, end=' > ')
    print(sol.isNumber(st))
