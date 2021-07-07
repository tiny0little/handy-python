#!/usr/bin/python3

"""
3. Longest Substring Without Repeating Characters
Difficulty: Medium
Runtime: 48 ms, faster than 96.45% of Python3 online submissions
Memory Usage: 14.1 MB, less than 98.86% of Python3 online submissions
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str):
        if len(s) <= 1: return len(s)
        result_substr_len = 0
        result_substr_start_index = 0
        current_substr_len = 0
        current_substr_start_index = 0
        s_hash = {}

        for i, l in enumerate(s):
            if l in s_hash:
                if s_hash[l] >= current_substr_start_index:
                    current_substr_len = i - current_substr_start_index
                    if result_substr_len < current_substr_len:
                        result_substr_len = current_substr_len
                        result_substr_start_index = current_substr_start_index
                    current_substr_start_index = s_hash[l] + 1
            s_hash[l] = i

        current_substr_len = len(s) - current_substr_start_index
        if result_substr_len < current_substr_len:
            result_substr_len = len(s) - current_substr_start_index
            result_substr_start_index = current_substr_start_index

        return s[result_substr_start_index:result_substr_start_index + result_substr_len]
        # return result_substr_len


sol = Solution()
# if sol.lengthOfLongestSubstring(s="abcabcbb") != 3: print('err 1')
# if sol.lengthOfLongestSubstring(s="bbbbb") != 1: print('err 2')
# if sol.lengthOfLongestSubstring(s="pwwkew") != 3: print('err 3')

print(sol.lengthOfLongestSubstring(s="abcsybertyabca"))
