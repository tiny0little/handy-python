#!/usr/bin/python3

"""
1395. Count Number of Teams
Difficulty: Medium

"""
from typing import List


class Solution:

    def numTeams(self, rating: List[int]) -> int:
        dp_list = [[], [], []]
        for r in rating: dp_list[0].append([r])
        for r in rating:
            dp_row = []
            for i in range(2):
                dp_row.append()

        print(dp_list)


sol = Solution()
print(sol.numTeams(rating=[2, 5, 3, 4, 1]))
