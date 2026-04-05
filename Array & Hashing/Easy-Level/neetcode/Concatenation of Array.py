# Problem: Concatenation of Array
# Platform: NeetCode 
# Difficulty: Easy
# Link: https://neetcode.io/problems/concatenation-of-array/question?list=allNC
# Topic: Array & Hashing
# Sub-topic: Array Simulation
# Problem Type: Array construction
# Constraint: Return array of length 2n using original order
# Technique Used: Direct concatenation
# Pattern Recognition: Array Traversal
# Approach Summary: Build result by concatenating nums with itself.
# Analysis of LeetCode/NeetCode: Straightforward and optimal for readability; uses required output space.
# Tags: array, simulation
# Time Taken: 25m
# Attempts: 2
#
# Time Complexity: O(n) none mentioned
# Space Complexity: O(n) none mentioned
# Better Approach?: No significant improvement beyond direct construction.
# Optimization Idea: Preallocate and fill with index math to avoid temporary intermediates.
# Key Insight You Missed: Output size itself is 2n, so O(n) extra space is unavoidable.

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = nums + nums
        return ans