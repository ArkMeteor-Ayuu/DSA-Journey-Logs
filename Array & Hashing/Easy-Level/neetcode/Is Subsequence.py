# Problem: Is Subsequence
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/is-subsequence
# Topic: Array & Hashing
# Sub-topic: Two Pointers
# Problem Type: String subsequence check
# Constraint: Determine whether s appears in t in order
# Technique Used: Two pointers
# Pattern Recognition: Linear scan
# Approach Summary: Walk through both strings with two pointers and advance the s pointer only when characters match.
# Analysis of LeetCode/NeetCode: This is the standard linear-time solution for a single subsequence query.
# Tags: string, two-pointers, subsequence
# Time Taken: 0 minutes
# Attempts: 1
#
#Quote of the Day: "Only way to predict the future is to forge one yourself."
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No for a single query; the two-pointer scan is optimal.
# Optimization Idea: Return early when s is fully matched.
# Key Insight You Missed: A subsequence only needs relative order, not contiguity.


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        j = 0

        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1

        return i == len(s)


# Follow-up idea:
# If there are many queries against the same t, preprocess t into a map from character
# to sorted index positions. For each s, use binary search to jump to the next valid
# occurrence after the previous match instead of rescanning t.