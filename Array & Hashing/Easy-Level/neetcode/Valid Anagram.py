# Problem: Concatenation of Array
# Platform: NeetCode 
# Difficulty: Easy
# Link: https://neetcode.io/problems/concatenation-of-array/question?list=allNC
#
# Time Complexity: O(n) none mentioned
# Space Complexity: O(k) none mentioned

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        count1 = Counter(s)
        count2 = Counter(t)
        if (count1 != count2) or len(s) != len(t):
            return False
        else:
            return True