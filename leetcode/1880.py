#!/usr/bin/python3

"""
1880. Check if Word Equals Summation of Two Words
Difficulty: Easy
Status: Accepted Runtime: 32 ms Memory Usage: 14.4 MB
"""


class Solution:
    def isSumEqual(self, firstWord: str, secondWord: str, targetWord: str) -> bool:
        alphabet = 'abcdefghij'

        firstNumber_str = ''
        for l in firstWord:
            firstNumber_str += str(alphabet.find(l))

        secondNumber_str = ''
        for l in secondWord:
            secondNumber_str += str(alphabet.find(l))

        targetNumber_str = ''
        for l in targetWord:
            targetNumber_str += str(alphabet.find(l))

        return int(targetNumber_str) == int(firstNumber_str) + int(secondNumber_str)


sol = Solution()
print(sol.isSumEqual(firstWord="aaa", secondWord="a", targetWord="aaaa"))
