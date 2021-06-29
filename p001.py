#!/usr/bin/python3.8

from typing import List


class Solution:

    def permutation(self, char_set: str, index: int) -> List[str]:
        if s_index == e_index:
            return char_set
        else:
            for i in range(s_index, e_index + 1):
                char_set[s_index], char_set[i] = char_set[i], char_set[s_index]
                self.permutation(char_set, s_index + 1, e_index)
                char_set[s_index], char_set[i] = char_set[i], char_set[s_index]

    def numTilePossibilities(self, tiles: str) -> int:
        result = []
        set_size = len(tiles)


sol = Solution()
print(sol.permutation([1, 2, 3, 4], 0, 1))
# print(sol.numTilePossibilities(tiles="AAB"))
