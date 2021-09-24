from typing import List
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # O(Nlogk) time complexity and O(k) space complexity
        return heapq.nlargest(k, nums)[-1]
        # O(NlogN) time complexity and O(1) space complexity
        # return sorted(nums)[-k]