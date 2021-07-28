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

    def removeInvalidParentheses(self, s: str) -> List[str]:
        s = ''.join(s.split())
        s_len = len(s)
        result = []
        invalid_parentheses = self.count_invalid_parentheses(s)

        for i in range(s_len):
            bit_mask = invalid_parentheses[:]
            s_candidate = s
            j = i
            while j < len(s_candidate):
                if (bit_mask[0] > 0) and (s_candidate[j] == '('):
                    s_candidate = s_candidate[:j] + s_candidate[j + 1:]
                    bit_mask[0] -= 1
                    continue
                if (bit_mask[1] > 0) and (s_candidate[j] == ')'):
                    s_candidate = s_candidate[:j] + s_candidate[j + 1:]
                    bit_mask[1] -= 1
                    continue
                if sum(bit_mask) == 0: break
                j += 1
            if sum(bit_mask) > 0: continue
            if self.count_invalid_parentheses(s_candidate) == [0, 0]:
                if s_candidate not in result: result.append(s_candidate)

        return result


sol = Solution()
print(sol.removeInvalidParentheses(s=")()("))

exit()

# stime = time.time()
# print(f'runtime: {time.time() - stime:.2f}sec')
if sol.removeInvalidParentheses(s="()())()") != ['(())()', '()()()']: print('err-1')
if sol.removeInvalidParentheses(s="(a)())()") != ['(a())()', '(a)()()']: print('err-2')
if sol.removeInvalidParentheses(s=")(") != ['']: print('err-3')
if sol.removeInvalidParentheses(s=")()(") != ['()']: print('err-53')
