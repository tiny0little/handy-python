#!/usr/bin/python3

"""
Find a pair with the given sum in a list
"""
from typing import List


def find_sublists(nums: List[int], sum: int) -> List[int]:
    hash = {}
    current_sum = 0
    for i in range(len(nums)):
        current_sum += nums[i]

        if (current_sum - sum) in hash:
            print(*[nums[v + 1: i + 1] for v in hash.get(current_sum - sum)], end=' ')
        hash[current_sum] = i

    return []


print(find_sublists(nums=[8, 7, 2, 5, 3, 1], sum=10))
