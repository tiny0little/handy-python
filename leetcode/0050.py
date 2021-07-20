#!/usr/bin/python3
"""
50. Pow(x, n)
Difficulty: Medium

Success
Runtime: 144 ms, faster than 5.92% of Python3 online submissions for Pow(x, n)
Memory Usage: 14.3 MB, less than 49.63% of Python3 online submissions for Pow(x, n)
"""
from typing import List
import time


class Solution:

    def myPow(self, x: float, n: int) -> float:
        if x == 1: return x
        if (x == -1) and (n > 0): return x
        if (x == -1) and (n < 0): return -x
        if n < 0:
            n0, x0 = -n, 1 / x
        else:
            n0, x0 = n, x

        if n0 > 1000000:
            if x0 > 1:
                if n0 > 0: return float('inf') * x0
                if n0 < 0: return 0
            elif x0 < 1:
                if n0 < 0: return float('inf') * x0
                if n0 > 0: return 0

        if n0 == 0:
            return 1
        elif n0 == 1:
            return x0
        else:
            result = 1
            for _ in range(n0):
                result = x0 * result
            return round(result, 5)


sol = Solution()
stime = time.time()
print(sol.myPow(x=-1.00000, n=-2147483648))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.myPow(x=2.0, n=10) != 1024: print('err-1')
if sol.myPow(x=2.1, n=3) != 9.26100: print('err-2')
if sol.myPow(x=0.00001, n=2147483647) != 0: print('err-291')
if sol.myPow(x=1.00012, n=1024) != 1.13074: print('err-294')
if sol.myPow(x=1.00001, n=123456) != 3.43684: print('err-295')
if sol.myPow(x=-1.00001, n=447125) != -87.46403: print('err-297')
if sol.myPow(x=2.00000, n=-2147483648) != 0: print('err-301')
if sol.myPow(x=-1.00000, n=2147483647) != -1.000: print('err-302')
if sol.myPow(x=-1.00000, n=-2147483648) != 1.000: print('err-303')
if sol.myPow(x=1.00000, n=-2147483648) != 1.000: print('err-303a')
