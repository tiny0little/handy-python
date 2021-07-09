#!/usr/bin/python3
"""
30. Substring with Concatenation of All Words
Difficulty: Hard

"""
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        result = []
        hash_dict = {}
        i = 0
        while i < len(s):
            for w in words:
                if s[i:i + len(w)] == w:
                    hash_dict[i] = w
                    i += len(w) - 1
                    break
            i += 1

        just_added = False
        for key in hash_dict:
            if just_added:
                just_added = False
                continue
            if key + len(hash_dict[key]) in hash_dict:
                if hash_dict[key] != hash_dict[key + len(hash_dict[key])]:
                    result.append(key)
                    just_added = True
                    continue

        return result


sol = Solution()
print(sol.findSubstring(s="wordgoodgoodgoodbestword", words=["word", "good", "best", "word"]))

if sol.findSubstring(s="barfoothefoobarman", words=["foo", "bar"]) != [0, 9]: print('err-1')
if sol.findSubstring(s="wordgoodgoodgoodbestword", words=["word", "good", "best", "word"]) != []: print('err-2')
