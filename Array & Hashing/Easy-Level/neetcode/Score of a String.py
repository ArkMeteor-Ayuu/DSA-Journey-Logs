# Problem: Score of a String
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/score-of-a-string/question?list=allNC
# Topic: Array & Hashing
# Sub-topic: String Traversal
# Problem Type: Adjacent difference accumulation
# Constraint: Sum absolute ASCII differences for adjacent characters
# Technique Used: Single pass iteration
# Pattern Recognition: Adjacent Pair Processing
# Approach Summary: Traverse from index 1 and add absolute difference with previous character.
# Analysis of LeetCode/NeetCode: Clean linear scan; minimal state and easy to reason about.
# Tags: string, traversal, math
# Time Taken: 48m
# Attempts: 5
#
# Time Complexity: O(n) none mentioned
# Space Complexity: O(1) none mentioned
# Better Approach?: Space can be O(1) because no extra structure scales with input.
# Optimization Idea: Keep as-is; already simple and efficient.
# Key Insight You Missed: Only neighboring character comparisons are required.

class Solution:
    def scoreOfString(self, s: str) -> int:
        score = 0
        for i in range(1, len(s)):
            score += abs(ord(s[i]) - ord(s[i - 1])) # ord gives ASCII value of a character and abs returns absolute value without negative or so
        return score