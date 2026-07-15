# Problem: 27. Remove Element
# Platform: LeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/remove-element/
# Topic: Array & Hashing
# Sub-topic: Two Pointers
# Problem Type: In-place filtering
# Constraint: Remove all target values in-place with O(1) extra space
# Technique Used: Two pointers
# Pattern Recognition: Two Pointers
# Approach Summary: Iterate once and copy non-target values to the next write position.
# Analysis of LeetCode/NeetCode: Efficient one-pass in-place solution; aligns with the expected approach.
# Tags: array, two-pointers, in-place
# Time Taken: 25m
# Attempts: 1
#
# Quote of the Day: "Laughter is the sun that drives winter from the human face."
# Time Complexity: O(n) (O(n) suggested) 
# Space Complexity: O(1) (O(1) suggested) 
# Better Approach?: Equivalent alternatives exist but complexity remains the same.
# Optimization Idea: Swap-with-end variant may reduce writes when target appears frequently.
# Key Insight You Missed: Tracking a write index is enough to rebuild the valid prefix in-place.

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        x = 0
        for i in range (0, len(nums)):
            if nums[i] != val:
                nums[x] = nums[i]
                x += 1
        return x