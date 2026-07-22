# Problem: String Matching in an Array
# Platform: NeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/string-matching-in-an-array/
# Topic: Array & Hashing
# Sub-topic: Substring detection
# Problem Type: Find strings that are substrings of other strings
# Constraint: Each word is unique, length up to 30, and there are at most 100 words
# Technique Used: Sorting by length and substring check
# Pattern Recognition: Substring containment via nested checks
# Approach Summary: Sort words by length, then for each word check whether it is a substring of any longer word using a simple containment check.
# Analysis of LeetCode/NeetCode: Sorting by length reduces redundant checks and keeps the solution efficient for the given constraints.
# Tags: array, strings, substring
# Time Taken: 34 mins
# Attempts: 1
#
# Quote of the Day: "You can't cross the sea merely by standing and staring at the water."
#
# Time Complexity: O(n^2 * L^2) in the worst case
# Space Complexity: O(n)
# Better Approach?: Using sorting plus substring checks is straightforward and efficient enough for the constraints.
# Optimization Idea: Check only against longer words and stop as soon as a match is found.
# Key Insight You Missed: A word only needs to be compared with strings that are longer than itself.


class Solution:
    def stringMatching(self, words: list[str]) -> list[str]:
        words.sort(key=len)
        result = []

        for i, word in enumerate(words):
            for j in range(i + 1, len(words)):
                if word in words[j]:
                    result.append(word)
                    break

        return result


