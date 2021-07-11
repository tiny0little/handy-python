#!/usr/bin/python3
"""
1925. Count Square Sum Triples

"""


class Solution:
    def countTriples(self, n: int) -> int:
        n0 = n + 1
        result = 0
        for a in range(1, n0):
            for b in range(1, n0):
                ab = max(a, b)
                for c in range(ab, n0):
                    if c * c == a * a + b * b:
                        result += 1

        return result


sol = Solution()
print(sol.countTriples(n=250))
