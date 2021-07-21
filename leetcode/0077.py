#!/usr/bin/python3
"""
77. Combinations
Difficulty: Medium

Success
Runtime: 600 ms, faster than 23.89% of Python3 online submissions
Memory Usage: 15.8 MB, less than 52.46% of Python3 online submissions
"""
from typing import List
import time


class Solution:
    def combine_dfs(self, n: int, k: int) -> List[List[int]]:
        char_set = [_ for _ in range(1, n + 1)]
        r = []

        def dfs(cur, pos):
            if len(cur) == k: r.append(cur)
            if pos == len(char_set): return

            if type(char_set) is list:
                for i in range(pos, len(char_set)):
                    dfs(cur + [char_set[i]], i + 1)
            else:
                for i in range(pos, len(char_set)):
                    dfs(cur + char_set[i], i + 1)

        dfs([], 0)
        return r

    def combine_dp(self, n: int, k: int) -> List[List[int]]:
        char_set = [_ for _ in range(1, n + 1)]
        dp_list = [[] for _ in range(k + 1)]

        # dp for k=1
        for c in char_set: dp_list[1].append([c])

        for i in range(2, k + 1):
            for c in char_set:
                for list0 in dp_list[i - 1]:
                    list1 = sorted(list0 + [c])
                    if (list(dict.fromkeys(list1)) == list(list1)) and (list1 not in dp_list[i]):
                        dp_list[i].append(list1)

        return dp_list[k]

    def combine_bf(self, n: int, k: int) -> List[List[int]]:
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
o = sol.combine_dfs(n=5, k=3)
print(f'{len(o)} {o}')
print(f'runtime: {time.time() - stime:.2f}sec')

"""
dfs(n=20, k=15) 0.3sec
dfs(n=20, k=10) 0.5sec
dp(n=17, k=14) 118sec dfs(n=17, k=14) 0sec
dp(n=17, k=13) 115sec dfs(n=17, k=13) 0sec
dp(n=16, k=13) 28sec dfs(n=16, k=13) 0sec
dp(n=16, k=14) 27sec dp(n=16, k=14) 0sec
bf(n=11, k=8) 310sec dp(n=11, k=8) 0sec
bf(n=11, k=7) 29sec dp(n=11, k=7) 0sec
"""
