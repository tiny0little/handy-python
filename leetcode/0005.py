#!/usr/bin/python3

"""
5. Longest Palindromic Substring
Difficulty: Medium
Success
Runtime: 4088 ms, faster than 30.34% of Python3 online submissions
Memory Usage: 239.3 MB, less than 6.13% of Python3 online submissions
"""


class Solution:
    dp_list = []

    def palindromizer(self, s: str, n: int):
        self.dp_list = []
        need_to_add = 2 - len(self.dp_list)
        for i in range(need_to_add): self.dp_list.append({})

        # building dp_list for len = 2 and 3
        for i in range(2, 4):
            if len(self.dp_list) < i + 1:
                dp_row = {}
                for j in range(len(s) - i + 1):
                    s0 = s[j:j + i]
                    if s0 == s0[::-1]: dp_row[j] = s0
                self.dp_list.append(dp_row)

        for i in range(4, n + 1):
            dp_row = {}
            for j in self.dp_list[i - 2]:
                val = self.dp_list[i - 2][j]
                if (j > 0) and (j + len(val) < len(s)):
                    s0 = s[j - 1:j + len(val) + 1]
                    if s0 == s0[::-1]: dp_row[j - 1] = s0
            self.dp_list.append(dp_row)

        return None

    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2: return s

        result = ''
        self.palindromizer(s=s, n=len(s))
        for i in range(len(self.dp_list) - 1, -1, -1):
            if len(self.dp_list[i]) > 0:
                result = list(self.dp_list[i].values())[0]
                break
        if result == '': result = s[0]
        return result


sol = Solution()
print(sol.longestPalindrome(s="aaaa"))

# if sol.longestPalindrome(s="cbbd") != 'bb': print('err-1')
# if sol.longestPalindrome(s="aaaa") != 'aaaa': print('err-2')
