#!/usr/bin/python3

"""
3. Longest Substring Without Repeating Characters
Medium

"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        right = len(s)
        while True:
            sub_str = s[left:right]


sol = Solution()
print(sol.lengthOfLongestSubstring(s="abcabcbb"))
