#!/usr/bin/python3

"""
3. Longest Substring Without Repeating Characters
Medium

https://www.geeksforgeeks.org/print-longest-substring-without-repeating-characters/
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        substr_maxlen = 0
        substr_start_index = 0

        for i in range(len(s)):


sol = Solution()
print(sol.lengthOfLongestSubstring(s="abcabcbb"))
