# Problem: Pascal's Triangle
# Platform: NeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/pascals-triangle/
# Topic: Array & Hashing
# Sub-topic: Array Construction
# Problem Type: Iterative row building
# Constraint: Return the first numRows rows of Pascal's triangle
# Technique Used: Dynamic row construction
# Pattern Recognition: Each row depends only on the previous row
# Approach Summary: Build each row from left to right using the previous row, setting the edges to 1 and each inner value as the sum of the two values above it.
# Analysis of LeetCode/NeetCode: This is the standard linear-per-row construction and is easy to reason about.
# Tags: array, construction, dynamic-programming, pascals-triangle
# Time Taken: 24 minutes
# Attempts: 1
#
#Quote of the Day: "Walking with a friend in the dark is better than walking alone in the light."
#
# Time Complexity: O(numRows^2)
# Space Complexity: O(numRows^2)
# Better Approach?: No, this direct construction is the cleanest approach for the problem.
# Optimization Idea: Use the previous row only while building the current row if you want to reduce working memory.
# Key Insight You Missed: The ends of each row are always 1, and every other value is the sum of two adjacent values from the row above.


from typing import List


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        ans = []
        prev = []

        for i in range(numRows):
            row = [1] * (i + 1)

            for j in range(1, i):
                row[j] = prev[j - 1] + prev[j]

            ans.append(row)
            prev = row

        return ans
