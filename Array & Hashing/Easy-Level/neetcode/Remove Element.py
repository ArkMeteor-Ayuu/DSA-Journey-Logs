# Problem: 27. Remove Element
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/remove-element
# Topic: Array & Hashing
# Sub-topic: Two Pointers
# Problem Type: In-place filtering
# Constraint: Remove all target values in-place with O(1) extra space
# Technique Used: Two pointers
# Pattern Recognition: Two Pointers
# Approach Summary: Iterate once and copy non-target values to the next write position.
# Analysis of LeetCode/NeetCode: Efficient one-pass in-place solution; aligns with the expected approach.
# Tags: array, two-pointers, in-place
# Time Taken: 12 minutes
# Attempts: 1
#
# Quote of the Day: "A people free to choose will always choose peace."
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: Equivalent alternatives exist but complexity remains the same.
# Optimization Idea: Swap-with-end variant may reduce writes when target appears frequently.
# Key Insight You Missed: Tracking a write index is enough to rebuild the valid prefix in-place.


from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
    k = 0

    for i in range(len(nums)):
            if nums[i] != val:
        nums[k] = nums[i]
        k += 1

    return k