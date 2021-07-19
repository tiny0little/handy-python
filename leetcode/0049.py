#!/usr/bin/python3
"""
49. Group Anagrams
Difficulty: Medium

Runtime: 100 ms, faster than 60.11% of Python3 online submissions
Memory Usage: 17.3 MB, less than 71.68% of Python3 online submissions
"""
from typing import List


class Solution:

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if len(strs) <= 1: return [strs]

        strs.sort()
        result_list = []
        hash_list = {}

        while len(strs) > 0:
            str0 = ''.join(sorted(strs[0]))
            if str0 in hash_list:
                result_list[hash_list[str0]].append(strs[0])
            else:
                result_list.append([strs[0]])
                hash_list[str0] = len(result_list) - 1
            strs.pop(0)

        # print(len(result_list))
        return result_list


sol = Solution()
# strs = ["ddddddddddg", "dgggggggggg"]
# strs = ["", "b", ""]
# strs = ["eat", ""]
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(sol.groupAnagrams(strs=strs))
