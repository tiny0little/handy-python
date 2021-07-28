#!/usr/bin/python3
"""
301. Remove Invalid Parentheses
Difficulty: Hard
"""
from typing import List
import time


class Solution:
    def count_invalid_parentheses(self, s: str) -> List[int]:
        left_p_count = 0
        right_p_count = 0
        for i in range(len(s)):
            if s[i] == '(': left_p_count += 1
            if s[i] == ')':
                if left_p_count > 0:
                    left_p_count -= 1
                else:
                    right_p_count += 1

        return [left_p_count, right_p_count]

    def bit_mask_increaser(self, bit_mask: List[int]) -> List[int]:
        bit_mask[-1] += 1
        for i in range(len(bit_mask) - 1, 0, -1):
            if bit_mask[i] > 1:
                bit_mask[i] = 0
                bit_mask[i - 1] += 1
        if bit_mask[0] > 1: bit_mask[0] = 0
        return bit_mask

    def removeInvalidParentheses(self, s: str) -> List[str]:
        s = ''.join(s.split())
        s_len = len(s)
        result = []
        invalid_parentheses = self.count_invalid_parentheses(s)
        if sum(invalid_parentheses) == 0: return [s]
        bit_mask = [0 for _ in range(s_len)]

        counter = 2 ** s_len
        while counter > 0:
            # will use bit_mask which has same number of 1s as number of invalid parentheses
            while sum(self.bit_mask_increaser(bit_mask)) != sum(invalid_parentheses): pass

            # will keep bit positions which are '0'
            s_candidate = ''
            for i in range(len(bit_mask)):
                if bit_mask[i] == 0:
                    s_candidate += s[i]

            if self.count_invalid_parentheses(s_candidate) == [0, 0]:
                if s_candidate not in result: result.append(s_candidate)

            counter -= 1

        if len(result) == 0: result.append('')
        return result


sol = Solution()
print(sol.removeInvalidParentheses(s="()())()"))

# stime = time.time()
# print(f'runtime: {time.time() - stime:.2f}sec')
if sorted(sol.removeInvalidParentheses(s="()())()")) != sorted(['(())()', '()()()']): print('err-1')
if sorted(sol.removeInvalidParentheses(s="(a)())()")) != sorted(['(a())()', '(a)()()']): print('err-2')
if sol.removeInvalidParentheses(s=")(") != ['']: print('err-3')
if sol.removeInvalidParentheses(s=")()(") != ['()']: print('err-53')
if sol.removeInvalidParentheses(s="n") != ['n']: print('err-40')
if sol.removeInvalidParentheses(s=")(f") != ['f']: print('err-43')
