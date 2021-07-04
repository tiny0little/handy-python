#!/usr/bin/python3

"""
5801. Eliminate Maximum Number of Monsters
Medium

"""
from typing import List


class Solution:
    def eliminateMaximum(self, dist: List[int], speed: List[int]) -> int:
        result = 0
        while True:
            i = 0
            while i < len(dist) - 1:
                print(dist)
                if dist[i] <= 0:
                    if result == 0: result = 1
                    return result
                if dist[i] == min(dist):
                    dist.pop(i)
                    speed.pop(i)
                    i -= 1
                    result += 1
                else:
                    dist[i] -= speed[i]
                i += 1


sol = Solution()
print(sol.eliminateMaximum(dist=[1, 3, 4], speed=[1, 1, 1]))
