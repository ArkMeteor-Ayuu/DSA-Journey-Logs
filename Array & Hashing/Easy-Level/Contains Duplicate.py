# Problem: Contains Duplicate
# Platform: NeetCode
# Difficulty: Easy
# Link: https://neetcode.io/problems/score-of-a-string/question?list=allNC
#
# Time Complexity: O(n)
# Space Complexity: O(n)

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        dup = set()
        duplicate = 0
        for i in nums:
            if i in dup:
                duplicate = 1
                break
            else: 
                dup.add(i)

        if duplicate:
            return True
        else:
            return False