#!/usr/bin/python3

from typing import List

"""
17 Letter Combinations of a Phone Number
Difficulty: Medium

Runtime: 32 ms, faster than 61.61% of Python3 online submissions for Letter Combinations of a Phone Number.
Memory Usage: 14.3 MB, less than 61.08% of Python3 online submissions for Letter Combinations of a Phone Number.
"""

class Solution:

    def letterCombinations(self, digits: str) -> List[str]:
        if len(digits) < 1: return []
        if not digits.isnumeric(): return []
        for digit in digits:
            if not (int(digit) in range(2, 10)):
                return []

        #

        digit_to_letters_seed = ['', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
        digit_to_letters = []
        for digit in digits: digit_to_letters.append(digit_to_letters_seed[int(digit)])

        counter_list = [0] * len(digit_to_letters)
        counter_list[-1] = -1
        result = []
        while True:
            counter_list[-1] += 1
            for i in range(len(counter_list) - 1, -1, -1):
                if (counter_list[i] > len(digit_to_letters[i]) - 1) and (i > 0):
                    counter_list[i] = 0
                    counter_list[i - 1] += 1

            result_str = ''
            for i in range(len(digit_to_letters)):
                result_str += digit_to_letters[i][counter_list[i]]
            result.append(result_str)

            reached_the_end = True
            for i in range(len(counter_list)):
                if counter_list[i] < len(digit_to_letters[i]) - 1:
                    reached_the_end = False
                    break
            if reached_the_end: break

        return result


#
#

sol = Solution()
print(sol.letterCombinations(digits="92"))
