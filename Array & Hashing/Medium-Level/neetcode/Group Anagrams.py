# Problem: Group Anagrams
# Platform: NeetCode
# Difficulty: Medium
# Link: https://neetcode.io/problems/group-anagrams
# Topic: Array & Hashing
# Sub-topic: Hash Map
# Problem Type: String grouping
# Constraint: Group strings that share the same character counts
# Technique Used: Hash map
# Pattern Recognition: Frequency signature
# Approach Summary: Build a 26-count signature for each word and group words by that signature.
# Analysis of LeetCode/NeetCode: This is an efficient grouping approach with linear work over the total characters processed.
# Tags: string, hashing, hashmap, grouping
# Time Taken: 21 minutes
# Attempts: 1
#
#Quote of the Day: "Be kind whenever possible. It is always possible."
#
# Time Complexity: O(n * k)
# Space Complexity: O(n * k)
# Better Approach?: No, this frequency-signature approach is the standard optimal solution for lowercase strings.
# Optimization Idea: Reuse a fixed-size count array and convert it to a tuple for a stable hashable key.
# Key Insight You Missed: Anagrams share the same character frequency profile even when their order differs.


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = {}

        for word in strs:
            count = [0] * 26

            for ch in word:
                count[ord(ch) - ord('a')] += 1

            key = tuple(count)

            if key not in groups:
                groups[key] = []

            groups[key].append(word)

        return list(groups.values())
