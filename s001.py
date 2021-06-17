#!/usr/bin/python3.8

class Solution(object):
    def countGoodTriplets(self, arr, a, b, c):
        """
        1534. Count Good Triplets
        :type arr: List[int]
        :type a: int
        :type b: int
        :type c: int
        :rtype: int
        """
        result = []
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                for k in range(j + 1, len(arr)):
                    if (abs(arr[i] - arr[j]) <= a) & \
                            (abs(arr[j] - arr[k]) <= b) & \
                            (abs(arr[i] - arr[k]) <= c):
                        result.append((arr[i], arr[j], arr[k]))

        return len(result)


s = Solution()
print(s.countGoodTriplets(arr=[3, 0, 1, 1, 9, 7], a=7, b=2, c=3))
