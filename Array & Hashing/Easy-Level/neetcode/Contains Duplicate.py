# Problem: Contains Duplicate
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/duplicate-integer
# Topic: Array & Hashing
# Sub-topic: Hash Set Membership
# Problem Type: Duplicate detection
# Constraint: Detect duplicate efficiently in one pass if possible
# Technique Used: Hash set
# Pattern Recognition: Hashing for lookup
# Approach Summary: Track seen numbers in a set and return true on first repeat.
# Analysis of LeetCode/NeetCode: Good linear-time approach; hash set lookup provides average O(1) checks.
# Tags: array, hashing, set
# Time Taken: 18m
# Attempts: 1
#
# Quote of the Day: "Living well is the best revenge."
# Time Complexity: O(n)
# Space Complexity: O(n)
# Better Approach?: Sorting gives O(n log n) with O(1)/O(log n) extra space tradeoff.
# Optimization Idea: Return immediately on duplicate and avoid extra flag variable.
# Key Insight You Missed: Membership checks in sets can short-circuit as soon as a repeat appears.

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        dup = set()
        duplicate = 0
        for i in nums:
            if i in dup:
                duplicate = 1
                break
            else: 
                dup.add(i)

        if duplicate:
            return True
        else:
            return False