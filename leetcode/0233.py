#!/usr/bin/python3
"""
233. Number of Digit One
Difficulty: Hard

"""
from typing import List
import time


class Solution:
    def __init__(self):
        self.dp_list = [0, 1]

    def countDigitOne(self, n: int) -> int:

        # building dp_list
        s = str(n)
        digits = len(s)
        for digit_position in range(digits + 1):
            if len(self.dp_list) >= digit_position + 1: continue
            min_num = 10 ** (digit_position - 1)
            self.dp_list.append(min_num + sum(self.dp_list) * 9)

        result = 0
        digit_position = 1
        while len(s) > 0:
            d = int(s[-1])
            s = s[:-1]
            result0 = 0
            for i in range(digit_position): result0 += self.dp_list[i]
            min_num = 10 ** (digit_position - 1)
            if d == 1:
                result +=
            elif d > 1:
                result += min_num + d * result0

            digit_position += 1

        return result


sol = Solution()

stime = time.time()
print(sol.countDigitOne(n=100))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.countDigitOne(n=13) != 6: print('err-1')
if sol.countDigitOne(n=123) != 57: print('err-1a')
if sol.countDigitOne(n=100) != 21: print('err-1b')
if sol.countDigitOne(n=111) != 36: print('err-1c')
if sol.countDigitOne(n=101) != 23: print('err-1d')
if sol.countDigitOne(n=0) != 0: print('err-2')
if sol.countDigitOne(n=999) != 300: print('err-3')
if sol.countDigitOne(n=90909) != 46281: print('err-4')
if sol.countDigitOne(n=824883294) != 767944060: print('err-35')
print(sol.dp_list)
