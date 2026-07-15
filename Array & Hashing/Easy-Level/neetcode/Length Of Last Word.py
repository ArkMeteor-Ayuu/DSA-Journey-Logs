# Problem: Length of Last Word
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/length-of-last-word
# Topic: Array & Hashing
# Sub-topic: Strings
# Problem Type: String traversal
# Constraint: Return the length of the final word in a string
# Technique Used: Reverse scan
# Pattern Recognition: Skip trailing spaces, then count the final word
# Approach Summary: Walk backward to ignore trailing spaces, then count characters until the next space or the start of the string.
# Analysis of LeetCode/NeetCode: This is a linear-time solution with constant extra space.
# Tags: string, traversal, reverse-scan
# Time Taken: 9 mins
# Attempts: 1
#
# Quote of the Day: "The first wealth is health."
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No, this is already optimal for the problem.
# Optimization Idea: A reverse scan avoids splitting the string or storing words.
# Key Insight You Missed: Trailing spaces must be skipped before counting the final word.


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        length = 0

        while i >= 0 and s[i] == " ":
            i -= 1

        while i >= 0 and s[i] != " ":
            length += 1
            i -= 1

        return length