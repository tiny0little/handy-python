#!/usr/bin/python3.8

class Solution(object):
    def arrayStringsAreEqual(self, word1, word2):
        """
        :type word1: List[str]
        :type word2: List[str]
        :rtype: bool
        """

        w1 = ''
        w2 = ''
        for w01 in word1: w1 += w01
        for w02 in word2: w2 += w02

        return w1 == w2


s = Solution()
print(s.arrayStringsAreEqual(word1=["a", "cb"], word2=["ab", "c"]))
