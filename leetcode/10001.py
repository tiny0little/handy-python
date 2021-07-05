#!/usr/bin/python3

"""
Longest Substring Without Repeating Characters
"""
from typing import List
import subprocess

for line in subprocess.getoutput("cat /home/user/src/handy-tools/a_list").split("\n"):
    print(f"'{line}', ")

# def lengthOfLongestSubstring(s: str):
#
#
# print(lengthOfLongestSubstring('abcsybertyabca'))

# if lengthOfLongestSubstring(s="abcabcbb") != 3: print('err 1')
# if lengthOfLongestSubstring(s="bbbbb") != 1: print('err 2')
# if lengthOfLongestSubstring(s="pwwkew") != 3: print('err 3')
