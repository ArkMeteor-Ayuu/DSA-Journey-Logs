# Problem: Concatenation of Array
# Platform: NeetCode 
# Difficulty: Easy
# Link: https://neetcode.io/problems/concatenation-of-array/question?list=allNC
#
# Time Complexity: O(n) none mentioned
# Space Complexity: O(n) none mentioned

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = nums + nums
        return ans