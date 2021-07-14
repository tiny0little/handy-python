#!/usr/bin/python3

"""
77. Combinations
Difficulty: Medium

"""
from typing import List
import time


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        dp_list = [[] * k]
        
    def combine_brute(self, n: int, k: int) -> List[List[int]]:
        char_set = [v for v in range(1, n + 1)]
        bit_map = [v for v in range(k)]
        result = []

        while True:
            result0 = []
            for i in range(len(bit_map)): result0.append(char_set[bit_map[i]])
            if list(set(result0)) == list(result0): result.append(result0)

            bit_map[-1] += 1
            over_flow = False
            for i in range(len(bit_map) - 1, -1, -1):
                if over_flow:
                    bit_map[i] += 1
                    over_flow = False
                if bit_map[i] >= n:
                    over_flow = True
                    bit_map[i] = 0
                if not over_flow: break
            if (k > 1) and (sum(bit_map) >= (n - 1) * k): break
            if (k == 1) and (sum(bit_map) == 0): break

        return result


sol = Solution()


stime = time.time()
print(sol.combine_brute(n=10, k=7))
print(f'runtime: {time.time() - stime:.1f}sec')
