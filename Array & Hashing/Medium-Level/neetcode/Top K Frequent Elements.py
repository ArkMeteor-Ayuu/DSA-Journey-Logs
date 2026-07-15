# Problem: Top K Frequent Elements
# Platform: NeetCode
# Difficulty: Medium
# Link: https://neetcode.io/problems/top-k-frequent-elements
# Topic: Array & Hashing
# Sub-topic: Hash Map
# Problem Type: Frequency-based selection
# Constraint: Return the k most frequent integers
# Technique Used: Bucket sort
# Pattern Recognition: Frequency buckets
# Approach Summary: Count each number, place values into buckets by frequency, then scan from highest frequency down until k elements are collected.
# Analysis of LeetCode/NeetCode: This achieves linear time relative to the input size and the number of distinct values.
# Tags: array, hashing, hashmap, bucket-sort, frequency
# Time Taken: 6 minutes
# Attempts: 1
#
#Quote of the Day: "A smile is a curve that sets everything straight."
#
# Time Complexity: O(n)
# Space Complexity: O(n)
# Better Approach?: No, this bucket-based solution is optimal for the stated constraints.
# Optimization Idea: Use a frequency map plus indexed buckets to avoid sorting by count.
# Key Insight You Missed: The maximum possible frequency is the array length, so a bucket array gives direct access to elements by count.


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = {}
        buckets = [[] for _ in range(len(nums) + 1)]

        for num in nums:
            counts[num] = counts.get(num, 0) + 1

        for num, freq in counts.items():
            buckets[freq].append(num)

        answer = []

        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                answer.append(num)
                if len(answer) == k:
                    return answer