#!/usr/bin/python3

"""
5801 Eliminate Maximum Number of Monsters
https://leetcode.com/contest/weekly-contest-248

Difficulty: Medium

"""
from typing import List


class Solution:
    def eliminateMaximum(self, dist: List[int], speed: List[int]) -> int:
        result = 0
        while len(dist) > 0:
            monster_to_kill = 0
            print(dist)
            for i in range(len(dist)):
                if dist[i] <= 0: return result
                if dist[i] - speed[i] < dist[monster_to_kill] - speed[monster_to_kill]: monster_to_kill = i
                dist[i] -= speed[i]
            print(f'monster to kill ={monster_to_kill}')
            dist.pop(monster_to_kill)
            speed.pop(monster_to_kill)
            result += 1

        return result


sol = Solution()

# if sol.eliminateMaximum(dist=[4, 2, 8], speed=[2, 1, 4]) != 1: print('error 1')
# if sol.eliminateMaximum(dist=[1, 3, 4], speed=[1, 1, 1]) != 3: print('error 2')
#
if sol.eliminateMaximum(dist=[4, 3, 4], speed=[1, 1, 2]) != 3: print(f'error 3')
#
# if sol.eliminateMaximum(dist=[1, 1, 2, 3], speed=[1, 1, 1, 1]) != 1: print('error 4]')
# if sol.eliminateMaximum(dist=[3, 2, 4], speed=[5, 3, 2]) != 1: print('error 5')
# if sol.eliminateMaximum(dist=[4, 3, 3, 3, 4], speed=[1, 1, 1, 1, 4]) != 3: print('error 6')
