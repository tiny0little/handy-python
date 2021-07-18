#!/usr/bin/python3

"""
1079. Letter Tile Possibilities
Difficulty: Medium

Success
"""
from typing import List
import time


class Solution:

    def is_substr(self, subs: str, s: str) -> bool:
        for l in subs:
            if subs.count(l) > s.count(l):
                return False
        return True

    #
    # dynamic programming
    def numTilePossibilities_dp(self, tiles: str) -> int:
        dp_list = [[] for _ in range(len(tiles) + 1)]

        # dp for 1
        for i in range(len(tiles)):
            if tiles[i] not in dp_list[1]: dp_list[1].append(tiles[i])

        # dp for 2 and up
        for i in range(2, len(tiles) + 1):
            for j in range(len(tiles)):
                for dp0 in dp_list[i - 1]:
                    s0 = tiles[j] + dp0
                    if (s0 not in dp_list[i]) and (self.is_substr(s0, tiles)):
                        dp_list[i].append(s0)

        result = 0
        for i in range(len(dp_list)):
            result += len(dp_list[i])

        return result


sol = Solution()
stime = time.time()
print(sol.numTilePossibilities_dp(tiles="ABCDEFG"))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.numTilePossibilities_dp(tiles="AAB") != 8: print('err-1')
if sol.numTilePossibilities_dp(tiles="ABCD") != 64: print('err-2')
if sol.numTilePossibilities_dp(tiles="AAABBC") != 188: print('err-3')
if sol.numTilePossibilities_dp(tiles="V") != 1: print('err-4')
