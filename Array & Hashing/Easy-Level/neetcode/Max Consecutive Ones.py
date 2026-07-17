# Problem: Max Consecutive Ones
# Platform: NeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/max-consecutive-ones/
# Topic: Array & Hashing
# Sub-topic: Counting Streaks
# Problem Type: Maximum consecutive sequence in array
# Constraint: nums contains only 0 or 1 values
# Technique Used: Single pass with running count
# Pattern Recognition: Streak counting
# Approach Summary: Count current run of 1s, reset on 0, and track the maximum run.
# Analysis of LeetCode/NeetCode: Optimal linear scan with constant extra space.
# Tags: array, counting
# Time Taken: 4 mins
# Attempts: 1
#
# Quote of the Day: "Start with what is right rather than what is acceptable."
#
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No, this is already optimal for the constraints.
# Optimization Idea: Keep only current and best streak counters in one pass.
# Key Insight You Missed: Consecutive-run problems usually need increment-on-match and reset-on-break.


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        count = 0
        ans = 0

        for num in nums:
            if num == 1:
                count += 1
                ans = max(ans, count)
            else:
                count = 0

        return ans