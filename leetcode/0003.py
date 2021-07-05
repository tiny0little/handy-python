#!/usr/bin/python3

"""
3. Longest Substring Without Repeating Characters
Medium

https://www.geeksforgeeks.org/print-longest-substring-without-repeating-characters/
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        result_substr_len = 0
        result_substr_start_index = 0
        current_substr_start_index = 0
        s_hash = {}

        for i, l in enumerate(s):
            if l in s_hash:
                print(f'{i} {l} {current_substr_start_index} {s_hash} {result_substr_start_index} {result_substr_len}')
                if s_hash[l] >= current_substr_start_index:
                    if result_substr_len < i - current_substr_start_index:
                        result_substr_len = i - s_hash[l]
                        result_substr_start_index = current_substr_start_index
                        current_substr_start_index = s_hash[l] + 1
                else:
                    s_hash[l] = i
            else:
                s_hash[l] = i

        if result_substr_len < i - current_substr_start_index:
            result_substr_len = i - current_substr_start_index
            result_substr_start_index = current_substr_start_index
            
        print(f'{i} {l} {current_substr_start_index} {s_hash} {result_substr_start_index} {result_substr_len}')
        return len(s[result_substr_start_index:result_substr_start_index + result_substr_len])


sol = Solution()
# if sol.lengthOfLongestSubstring(s="abcabcbb") != 3: print('err 1')
# if sol.lengthOfLongestSubstring(s="bbbbb") != 1: print('err 2')
# if sol.lengthOfLongestSubstring(s="pwwkew") != 3: print('err 3')

print(sol.lengthOfLongestSubstring(s="abcabcbb"))
