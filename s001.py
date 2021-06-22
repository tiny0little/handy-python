#!/usr/bin/python3.8

class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        result = True
        while len(ransomNote) > 0:
            magazine_index = magazine.find(ransomNote[0])
            if magazine_index > -1:
                ransomNote = ransomNote[1:]
                magazine = magazine[:magazine_index] + magazine[magazine_index + 1:]
            else:
                result = False
                break

        return result


sol = Solution()
print(sol.canConstruct(ransomNote="aa", magazine="aab"))
# print(sol.canConstruct(ransomNote="fffbfg", magazine="effjfggbffjdgbjjhhdegh"))
