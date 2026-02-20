# Problem: Score of a String
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/score-of-a-string/question?list=allNC
#
# Time Complexity: O(n) none mentioned
# Space Complexity: O(n) none mentioned

class Solution:
    def scoreOfString(self, s: str) -> int:
        score = 0
        for i in range(1, len(s)):
            score += abs(ord(s[i]) - ord(s[i - 1])) # ord gives ASCII value of a character and abs returns absolute value without negative or so
        return score