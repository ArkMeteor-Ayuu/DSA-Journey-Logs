# Problem: Longest Common Prefix
# Platform: NeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/longest-common-prefix/
# Topic: Array & Hashing
# Sub-topic: Common prefix / Strings
# Problem Type: Prefix computation across list of strings
# Constraint: 1 <= strs.length <= 200, 0 <= strs[i].length <= 200; strs[i] lowercase if non-empty
# Technique Used: Iterative prefix trimming
# Pattern Recognition: Pairwise prefix reduction
# Approach Summary: Start with the first string as candidate prefix, iteratively trim it using each subsequent word until it matches the prefix of all strings.
# Analysis of LeetCode/NeetCode: Linear scan across characters with early termination is optimal given constraints.
# Tags: array, strings, prefix
# Time Taken: 22 min
# Attempts: 1
#
# Quote of the Day: "It is far better to be alone, than to be in bad company."
#
# Time Complexity: O(S) where S is the sum of all characters in input strings
# Space Complexity: O(1) extra


class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        prefix = strs[0]

        for word in strs[1:]:
            i = 0

            while i < len(prefix) and i < len(word):
                if prefix[i] != word[i]:
                    break
                i += 1

            prefix = prefix[:i]

            if prefix == "":
                return ""

        return prefix
