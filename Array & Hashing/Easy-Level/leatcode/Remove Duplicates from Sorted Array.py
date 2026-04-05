# Problem: Remove Duplicates from Sorted Array
# Platform: LeetCode 
# Difficulty: Easy
# Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
#
# Time Complexity: O(n) (O(n) suggested) 
# Space Complexity: O(1) (O(1) suggested) 

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        x = 1
        for i in range(1,len(nums) ):
            if nums[i] != nums[i-1]:
                nums[x] = nums[i]
                x += 1
        return x