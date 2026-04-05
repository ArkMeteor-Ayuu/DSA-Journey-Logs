# Problem: 27. Remove Element
# Platform: LeetCode
# Difficulty: Easy
# Link: https://leetcode.com/problems/remove-element/
#
# Time Complexity: O(n) (O(n) suggested) 
# Space Complexity: O(1) (O(1) suggested) 

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        x = 0
        for i in range (0, len(nums)):
            if nums[i] != val:
                nums[x] = nums[i]
                x += 1
        return x