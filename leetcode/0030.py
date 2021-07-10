#!/usr/bin/python3
"""
30. Substring with Concatenation of All Words
Difficulty: Hard

Success
Runtime: 4248 ms, faster than 10.91% of Python3 online submissions
Memory Usage: 14.6 MB, less than 27.74% of Python3 online submissions
"""
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        result = []
        hash_dict = {}
        words.sort()

        i = 0
        while i < len(s):
            for w in words:
                if s[i:i + len(w)] == w:
                    hash_dict[i] = w
                    break
            i += 1

        for key in hash_dict:
            next_key = key
            words_candidate = []
            for w in words:
                if next_key in hash_dict:
                    words_candidate.append(hash_dict[next_key])
                    next_key = next_key + len(hash_dict[next_key])
                else:
                    break
            words_candidate.sort()
            if words_candidate[:] == words[:]: result.append(key)

        # print(hash_dict)
        return result


sol = Solution()
print(sol.findSubstring(s="aaaaaaaaaaaaaa", words=["aa", "aa"]))

if sol.findSubstring(s="barfoothefoobarman", words=["foo", "bar"]) != [0, 9]: print('err-1')
if sol.findSubstring(s="wordgoodgoodgoodbestword", words=["word", "good", "best", "word"]) != []: print('err-2')
if sol.findSubstring(s="barfoofoobarthefoobarman", words=["bar", "foo", "the"]) != [6, 9, 12]: print('err-3')
if sol.findSubstring(s="aaaaaaaaaaaaaa", words=["aa", "aa"]) != [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]: print('err-4')
