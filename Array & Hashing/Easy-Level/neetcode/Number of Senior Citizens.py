# Problem: Number of Senior Citizens
# Platform: LeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/number-of-senior-citizens/
# Topic: Array & Hashing
# Sub-topic: Strings
# Problem Type: String slicing and counting
# Constraint: Count passengers strictly more than 60 years old
# Technique Used: String slice comparison
# Pattern Recognition: The age is always stored in fixed positions
# Approach Summary: Read the two-digit age from each string and count entries whose age slice is greater than 60.
# Analysis of LeetCode/NeetCode: This is a direct linear scan with constant extra space.
# Tags: string, slicing, counting
# Question: Given a 0-indexed array of strings details, where each 15-character string encodes a passenger, return the number of passengers who are strictly more than 60 years old.
# Time Taken: 6 mins
# Attempts: 1
#
# Quote of the Day: "The future belongs to those who believe in the beauty of their dreams."
# Time Complexity: O(n)
# Space Complexity: O(1)
# Better Approach?: No, this is already optimal.
# Optimization Idea: Compare the age slice directly instead of converting it to an integer.
# Key Insight You Missed: The age is always stored at indices 11 and 12.


class Solution:
    def countSeniors(self, details: list[str]) -> int:
        return sum(detail[11:13] > "60" for detail in details)