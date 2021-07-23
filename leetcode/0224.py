#!/usr/bin/python3
"""
224. Basic Calculator
Difficulty: Hard
"""
from typing import List
import time


class Solution:

    # calculate simple expression, without parentheses
    def calc_simple_unit(self, s0: str) -> str:
        s0 += ' '
        i = 0
        operation_type = ''
        operation_start_idx = -1
        nums = []
        while not ''.join(s0.split()).lstrip('-').isnumeric():
            if (len(nums) > 0) and ((s0[i] == '+') or (s0[i] == '-')): operation_type = s0[i]
            if (s0[i].isnumeric()) or \
                    ((len(nums) == 0) and ((s0[i] == '+') or (s0[i] == '-'))):
                if operation_start_idx == -1: operation_start_idx = i
                for j in range(i + 1, len(s0)):
                    if not s0[j].isnumeric():
                        nums.append(s0[i:j])
                        i = j - 1
                        if (len(nums) == 2) and (operation_type != ''):
                            if operation_type == '+':
                                r0 = int(nums[0]) + int(nums[1])
                            else:
                                r0 = int(nums[0]) - int(nums[1])
                            s0 = s0[:operation_start_idx] + str(r0) + s0[j:]
                            operation_type = ''
                            operation_start_idx = -1
                            nums = []
                            i = -1
                        break

            i += 1
        return s0

    def calculate(self, s: str) -> int:

        def calc_one_unit(s0: str) -> str:
            i = 0
            while not s0.isnumeric():
                print(s0)

                if s0[i] == '(':
                    sub_parentheses = 0
                    sub_unit_start_idx = i + 1
                    sub_parentheses += 1
                    for j in range(i + 1, len(s0)):
                        if s0[j] == '(': sub_parentheses += 1
                        if s0[j] == ')':
                            sub_parentheses -= 1
                            if sub_parentheses == 0:
                                s0 = s0[:sub_unit_start_idx - 1] + calc_one_unit(s0[sub_unit_start_idx:j]) + s0[j + 1:]
                                break
                    i = 0
                    continue

                i += 1

            return s0

        s = ''.join(s.split())
        return calc_one_unit(s)


sol = Solution()
stime = time.time()
print(sol.calc_simple_unit('-6+6+6-6+1'))
# print(sol.calculate(s="(1+(4+5+2)-3)+(6+8)"))
print(f'runtime: {time.time() - stime:.2f}sec')
