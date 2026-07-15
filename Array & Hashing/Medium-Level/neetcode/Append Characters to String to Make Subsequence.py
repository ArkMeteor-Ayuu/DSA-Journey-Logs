# Problem: Append Characters to String to Make Subsequence
# Platform: NeetCode
# Difficulty: Medium
# Link: https://neetcode.io/problems/append-characters-to-string-to-make-subsequence
# Topic: Array & Hashing
# Sub-topic: Two Pointers
# Problem Type: Subsequence completion
# Constraint: Return the minimum characters to append so t becomes a subsequence of s
# Technique Used: Two pointers
# Pattern Recognition: Greedy matching
# Approach Summary: Scan both strings from left to right, matching as many characters of t inside s as possible, then append the unmatched suffix of t.
# Analysis of LeetCode/NeetCode: This is a linear-time greedy solution that uses only constant extra space.
# Tags: string, two-pointers, greedy, subsequence
# Time Taken: almost none
# Attempts: 1
#
#Quote of the Day: "You must be the change you wish to see in the world."
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No, a single pass is optimal for this problem.
# Optimization Idea: Stop as soon as all of t has been matched.
# Key Insight You Missed: The answer is just the number of characters in t that never matched in order.


class Solution:
    def appendCharacters(self, s: str, t: str) -> int:
        i = 0
        j = 0

        while i < len(t) and j < len(s):
            if t[i] == s[j]:
                i += 1
            j += 1

        return len(t) - i