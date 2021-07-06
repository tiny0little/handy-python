#!/usr/bin/python3

"""
1641 Count Sorted Vowel Strings
Difficulty: Medium
Success
Runtime: 32 ms, faster than 70.49% of Python3 online submissions
Memory Usage: 14.1 MB, less than 92.04% of Python3 online submissions
"""


class Solution:
    vowels = ['a', 'e', 'i', 'o', 'u']
    dp_table = []

    def build_dp_table(self, n: int):
        if len(self.dp_table) == 0:
            self.dp_table.append(self.vowels)

        for i in range(n):
            if len(self.dp_table) > i: continue
            dp_row = []
            for vowel in self.vowels:
                for j in range(len(self.dp_table[i - 1])):
                    str0 = vowel + self.dp_table[i - 1][j]
                    str0 = ''.join(sorted(str0))
                    if str0 not in dp_row: dp_row.append(str0)
            self.dp_table.append(dp_row)

    def countVowelStrings(self, n: int) -> int:
        self.build_dp_table(n)
        print(len(self.dp_table[n - 1]))

        # formula from https://home.ubalt.edu/ntsbarsh/business-stat/otherapplets/comcount.htm
        # combination of n objects in a group of size k with repetitions
        set_len = len(self.vowels)
        d = 1
        f = 1
        t = set_len + n - 1
        while t > set_len - 1:
            d *= t
            t -= 1
        while n > 0:
            f *= n
            n -= 1

        return int(round(d / f))


sol = Solution()
print(sol.countVowelStrings(n=17))
