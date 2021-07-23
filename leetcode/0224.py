#!/usr/bin/python3
"""
224. Basic Calculator
Difficulty: Hard
"""
from typing import List
import time


class Solution:
    def calculate(self, s: str) -> int:

        def calc_unit(s0: str) -> int:
            sub_unit = [-1, -1]
            i = 0
            while True:
                if s0[i] == '(':
                    sub_unit[0] = i + 1
                    

sol = Solution()
stime = time.time()
print(sol.calculate(s="(1+(4+5+2)-3)+(6+8)"))
print(f'runtime: {time.time() - stime:.2f}sec')
