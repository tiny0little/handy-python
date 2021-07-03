#!/usr/bin/python3

"""
1910. Remove All Occurrences of a Substring
Difficulty:Medium
Status: Accepted
Runtime: 28 ms
Memory Usage: 14.2 MB
"""


class Solution:
    def removeOccurrences(self, s: str, part: str) -> str:
        part_len = len(part)
        while True:
            i = s.find(part)
            if i >= 0:
                s = s[:i] + s[i + part_len:]
            else:
                break
        return s


sol = Solution()

s = "eemckxmckx"
part = "emckx"

print(sol.removeOccurrences(s=s, part=part))
