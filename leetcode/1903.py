#!/usr/bin/python3

"""
1903. Largest Odd Number in String
https://leetcode.com/contest/weekly-contest-246/problems/largest-odd-number-in-string/

Difficulty: Easy

"""


class Solution:
    def largestOddNumber(self, num: str) -> str:
        left = 0
        right = len(num) - 1
        while True:
            candidate = num[left:right]


sol = Solution()
num = "52"
print(sol.largestOddNumber(num=num))
