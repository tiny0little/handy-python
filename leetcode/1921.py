#!/usr/bin/python3
"""
1921 Eliminate Maximum Number of Monsters
Difficulty: Medium

"""
from typing import List


class Solution:
    def eliminateMaximum(self, dist: List[int], speed: List[int]) -> int:
        monsters_order = []

        # order of monsters to arrive
        while min(dist) > 0:
            # monsters are getting closer
            for i in range(len(dist)): dist[i] -= speed[i]

            next_monster = 0
            for i in range(len(dist)):
                if dist[next_monster] < dist[i]: next_monster = i
            monsters_order.append(next_monster)

        return monsters_order


sol = Solution()
# print(sol.eliminateMaximum(
#     dist=[46, 33, 44, 42, 46, 36, 7, 36, 31, 47, 38, 42, 43, 48, 48, 25, 28, 44, 49, 47, 29, 32, 30, 6, 42, 9, 39, 48,
#           22, 26, 50, 34, 40, 22, 10, 45, 7, 43, 24, 18, 40, 44, 17, 39, 36],
#     speed=[1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 3, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 8,
#            1, 1, 1, 3, 6, 1, 3, 1, 1]))

print(sol.eliminateMaximum(dist=[4, 2, 3], speed=[2, 1, 1]))
# if sol.eliminateMaximum(dist=[1, 3, 4], speed=[1, 1, 1]) != 3: print('err-1')
# if sol.eliminateMaximum(dist=[1, 1, 2, 3], speed=[1, 1, 1, 1]) != 1: print('err-2')
# if sol.eliminateMaximum(dist=[3, 2, 4], speed=[5, 3, 2]) != 1: print('err-3')
# if sol.eliminateMaximum(dist=[4, 2, 3], speed=[2, 1, 1]) != 3: print('err-4')
# if sol.eliminateMaximum(
#         dist=[46, 33, 44, 42, 46, 36, 7, 36, 31, 47, 38, 42, 43, 48, 48, 25, 28, 44, 49, 47, 29, 32, 30, 6, 42, 9, 39,
#               48,
#               22, 26, 50, 34, 40, 22, 10, 45, 7, 43, 24, 18, 40, 44, 17, 39, 36],
#         speed=[1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 3, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1,
#                8,
#                1, 1, 1, 3, 6, 1, 3, 1, 1]) != 7: print('err-5')
