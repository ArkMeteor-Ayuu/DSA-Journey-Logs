# Problem: Replace Elements with Greatest Element on Right Side
# Platform: LeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/
# Topic: Array & Hashing
# Sub-topic: Reverse Traversal
# Problem Type: In-place array transformation
# Constraint: Replace each value with the greatest value to its right
# Technique Used: Running maximum
# Pattern Recognition: Suffix maximum
# Approach Summary: Traverse the array from right to left while keeping the greatest value seen so far and overwrite each position with that running maximum.
# Analysis of LeetCode/NeetCode: This is the optimal in-place solution with linear time and constant extra space.
# Tags: array, traversal, inplace, greedy
# Time Taken: 11 mins
# Attempts: 1
#
# Quote of the Day: "We don't stop playing because we grow old; we grow old because we stop playing."
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No, a backward pass with a running maximum is the standard optimal solution.
# Optimization Idea: Update the array in place while scanning from the end so no extra storage is needed.
# Key Insight You Missed: Once you move right-to-left, the best value to the right is already known.



class Solution:
    def replaceElements(self, arr: list[int]) -> list[int]:
        max = -1

        for i in range(len(arr) - 1, -1, -1):
            temp = arr[i]
            arr[i] = max

            if temp > max:
                max = temp

        return arr