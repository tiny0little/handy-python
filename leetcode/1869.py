#!/usr/bin/python3

"""
1869. Longer Contiguous Segments of Ones than Zeros
Difficulty:Easy
Status: Accepted Runtime: 32 ms Memory Usage: 14.2 MB
"""


class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        longest_ones = 0
        longest_zeros = 0
        one_counter = 0
        zero_counter = 0
        for d in s:
            if d == '1':
                one_counter += 1
                if zero_counter > longest_zeros: longest_zeros = zero_counter
                zero_counter = 0
            else:
                zero_counter += 1
                if one_counter > longest_ones: longest_ones = one_counter
                one_counter = 0

        if zero_counter > longest_zeros: longest_zeros = zero_counter
        if one_counter > longest_ones: longest_ones = one_counter

        return longest_ones > longest_zeros


sol = Solution()
s = "111000"
print(sol.checkZeroOnes(s=s))
