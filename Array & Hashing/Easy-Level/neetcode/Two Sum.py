# Problem: Two Sum
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/two-integer-sum/question?list=neetcode150
# Topic: Array & Hashing
# Sub-topic: Hash Map
# Problem Type: Pair sum lookup
# Constraint: Return indices of two numbers that sum to target
# Technique Used: Hash map
# Pattern Recognition: Complement lookup
# Approach Summary: Use a hash map to store the indices of elements we've seen so far. For each element, calculate its complement and check if the complement is already in the hash map.
# Analysis of LeetCode/NeetCode: This approach has a time complexity of O(n) and space complexity of O(n), making it efficient for this problem.
# Tags: array, hashing, hashmap
# Time Taken: 17 minutes
# Attempts: 1
#
#Quote of the Day: "Do what you can, with what you have, where you are."
#
# Time Complexity: O(n)
# Space Complexity: O(n)
# Better Approach?: No, this one-pass hash map approach is the standard optimal solution.
# Optimization Idea: Return immediately when the complement is found and store the current value only after checking.
# Key Insight You Missed: The complement of each value can be checked while scanning once, so a nested loop is unnecessary.

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i in range(len(nums)):
            n = nums[i]
            comp = target - n
            if comp in seen:
                return [seen[comp], i]
            seen[n] = i