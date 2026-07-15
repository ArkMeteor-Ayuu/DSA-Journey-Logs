# Problem: Valid Anagram
# Platform: NeetCode 
# Difficulty: Easy
# Link: https://neetcode.io/problems/is-anagram
# Topic: Array & Hashing
# Sub-topic: Frequency Counting
# Problem Type: String comparison
# Constraint: Determine if two strings have identical character frequencies
# Technique Used: Hash map / Counter
# Pattern Recognition: Counting
# Approach Summary: Count each string with Counter and compare the maps.
# Analysis of LeetCode/NeetCode: Correct hashing approach with linear time over input size.
# Tags: string, hashmap, counter
# Time Taken: 32m
# Attempts: 2
#
# Quote of the Day: "No one has a greater asset for his business than a man's pride in his work."
# Time Complexity: O(n) none mentioned
# Space Complexity: O(k) none mentioned
# Better Approach?: Sorting approach exists but is slower at O(n log n).
# Optimization Idea: Quick length check before building counters can skip extra work.
# Key Insight You Missed: Equal lengths are a necessary condition for anagrams.

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        count1 = Counter(s)
        count2 = Counter(t)
        if (count1 != count2) or len(s) != len(t):
            return False
        else:
            return True