#!/usr/bin/python3
"""
227. Basic Calculator II
Difficulty: Medium

"""
from typing import List
import time


class Solution:
    def processor(self, s: str, sign: str) -> str:
        s = ''.join(s.split())

        while True:
            s = ' ' + s + ' '
            sign_idx = s.find(sign)
            if sign_idx < 0: break
            op1 = ''
            op2 = ''
            i = sign_idx - 1
            while op1 == '':
                if not s[i].isnumeric(): op1 = s[i + 1:sign_idx]
                i -= 1
            start_idx = i + 1
            i = sign_idx + 1
            while op2 == '':
                if not s[i].isnumeric(): op2 = s[sign_idx + 1:i]
                i += 1
            end_idx = i - 1

            if sign == '*':
                s0 = str(int(op1) * int(op2))
            elif sign == '/':
                s0 = str(int(int(op1) / int(op2)))
            elif sign == '+':
                s0 = str(int(op1) + int(op2))
            elif sign == '-':
                s0 = str(int(op1) + int(op2))
            else:
                s0 = ''

            s = s[:start_idx + 1] + s0 + s[end_idx:]

        s = ''.join(s.split())
        return s

    def calculate(self, s: str) -> int:
        s = self.processor(s, '*')
        s = self.processor(s, '/')
        s = self.processor(s, '+')
        s = self.processor(s, '-')
        return int(s)


sol = Solution()
print(sol.calculate(s=" 3/2 "))

# stime = time.time()
# print(f'runtime: {time.time() - stime:.2f}sec')


if sol.calculate(s="3+2*2") != 7: print('err-1')
if sol.calculate(s=" 3/2 ") != 1: print('err-2')
if sol.calculate(s=" 3+5 / 2 ") != 5: print('err-3')
