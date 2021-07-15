#!/usr/bin/python3

"""
77. Combinations
Difficulty: Medium

"""
from typing import List
import time


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        char_set = [_ for _ in range(1, n + 1)]
        dp_list = [[] for _ in range(k + 1)]
        for c in char_set: dp_list[1].append([c])
        for i in range(2, k + 1):
            for c in char_set:
                for l in dp_list[i - 1]:
                    l0 = sorted(l + [c])
                    list(dict.fromkeys(l0))
                    if (list(dict.fromkeys(l0)) == list(l0)) and (l0 not in dp_list[i]): dp_list[i].append(l0)

        return dp_list[k]

    def combine_brute(self, n: int, k: int) -> List[List[int]]:
        char_set = [v for v in range(1, n + 1)]
        bit_map = [v for v in range(k)]
        result = []

        while True:
            result0 = []
            for i in range(len(bit_map)): result0.append(char_set[bit_map[i]])
            result0.sort()
            if (list(dict.fromkeys(result0)) == list(result0)) and (result0 not in result): result.append(result0)

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
o = sol.combine(n=17, k=16)
print(f'{len(o)} {o}')
print(f'runtime: {time.time() - stime:.1f}sec')
