#!/usr/bin/python3

"""
5802. Count Good Numbers

"""


class Solution:
    def countGoodNumbers(self, n: int) -> int:
        even_numbers = '02468'
        prime_numbers = '2357'

        result = 0
        result_str = ''
        for i in range(n):
            if i % 2 == 0:
                result_str += even_numbers[]


sol = Solution()
print(sol.countGoodNumbers(n=1))
