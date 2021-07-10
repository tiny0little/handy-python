#!/usr/bin/python3
"""
32. Longest Valid Parentheses
Difficulty: Hard

"""


class Solution:
    def longestValidParentheses(self, s: str) -> int:
        if len(s) < 2: return 0
        

sol = Solution()
print(sol.longestValidParentheses(s="(()"))

if sol.longestValidParentheses(s="(()") != 2: print('err-1')
if sol.longestValidParentheses(s=")()())") != 4: print('err-2')
if sol.longestValidParentheses(s="") != 0: print('err-3')
