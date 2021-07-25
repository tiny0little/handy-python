#!/usr/bin/python3
"""
684. Redundant Connection
Difficulty: Medium

NOT FINISHED
"""
from typing import List
import time


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        node_list = []
        edges_len = len(edges)
        for i in range(edges_len):
            for j in range(2):
                if edges[i][j] not in node_list: node_list.append(edges[i][j])

        def validator(edges0: List[List[int]]) -> bool:
            node_list0 = node_list[:]

            while True:
                if edges0[0][0] in node_list0: node_list0.remove(edges0[0][0])
                if edges0[0][1] in node_list0: node_list0.remove(edges0[0][1])
                if len(edges0) == 1: break
                found_linked_node = False
                for i0 in range(1, len(edges0)):
                    if (min(edges0[i0]) == min(edges0[0])) or (max(edges0[i0]) == max(edges0[0])) or \
                            (min(edges0[i0]) == max(edges0[0])):
                        found_linked_node = True
                        edges0.pop(0)
                        break
                if not found_linked_node: return False

            return len(node_list0) == 0

        for i in range(edges_len - 1, -1, -1):
            edges1 = edges[:i] + edges[i + 1:]
            if validator(edges1): return edges[i]


sol = Solution()
stime = time.time()
print(sol.findRedundantConnection(edges=[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))
print(f'runtime: {time.time() - stime:.2f}sec')

if sol.findRedundantConnection(edges=[[1, 2], [1, 3], [2, 3]]) != [2, 3]: print('err-1')
if sol.findRedundantConnection(edges=[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) != [1, 4]: print('err-2')
