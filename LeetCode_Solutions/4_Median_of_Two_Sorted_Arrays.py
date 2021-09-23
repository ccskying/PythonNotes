import statistics
from typing import List
class Solution:
    # this problem require an algorithm with time complexity O(log (m+n))

    # https://leetcode.com/problems/median-of-two-sorted-arrays/discuss/2567/Python-O(log(min(mn))-solution
    def findMedianSortedArrays(self, A, B):
        l=len(A)+len(B)
        return self.findKth(A,B,l//2) if l%2==1 else (self.findKth(A,B,l//2-1)+self.findKth(A,B,l//2))/2.0
    def kth(self, A, B, k):
        if len(A) > len(B):
            A, B = (B, A)
        if not A:
            return B[k]
        if k == len(A) + len(B) - 1:
            return max(A[-1], B[-1])
    
        i = min(len(A)-1, k/2)
        j = min(len(B)-1, k-i)
    
        if A[i] > B[j]:
            return self.kth(A[:i], B[j:], i)
        else:
            return self.kth(A[i:], B[:j], j)

    # time complexity of this solution is much higher than requirement but it's short
    def findMedianSortedArrays_statistics(self, nums1: List[int], nums2: List[int]) -> float:
        nums3 = nums1 + nums2
        nums3 = sorted(nums3)
        return statistics.median(nums3)