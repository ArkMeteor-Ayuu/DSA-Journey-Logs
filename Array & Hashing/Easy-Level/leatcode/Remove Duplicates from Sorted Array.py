# Problem: Remove Duplicates from Sorted Array
# Platform: LeetCode 
# Difficulty: Easy
# Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
# Topic: Array & Hashing
# Sub-topic: Two Pointers
# Problem Type: In-place array transformation
# Constraint: Sorted array, modify in-place, O(1) extra space
# Technique Used: Two pointers
# Pattern Recognition: Two Pointers
# Approach Summary: Keep one write pointer and overwrite only when current value differs from previous.
# Analysis of LeetCode/NeetCode: Optimal linear scan with constant extra space; matches expected in-place strategy.
# Tags: array, two-pointers, in-place
# Time Taken: 20m
# Attempts: 2
#
# Time Complexity: O(n) (O(n) suggested) 
# Space Complexity: O(1) (O(1) suggested) 
# Better Approach?: No, this is the standard optimal approach.
# Optimization Idea: Early return for empty input can make edge handling explicit.
# Key Insight You Missed: The array is sorted, so duplicate detection only needs adjacent comparison.

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        x = 1
        for i in range(1,len(nums) ):
            if nums[i] != nums[i-1]:
                nums[x] = nums[i]
                x += 1
        return x