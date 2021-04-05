"""
在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

输入: [3,2,1,5,6,4] 和 k = 2
输出: 5

输入: [3,2,3,1,2,4,5,5,6] 和 k = 4
输出: 4

"""
from typing import List
class Solution:
    """
    方法二：基于堆排序的选择方法
    """
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def maxHeapify(i, heapSize):
            l = i*2+1
            r = i*2+2
            largest = i

            if l<heapSize and nums[l]>nums[largest]:
                largest = l
            if r<heapSize and nums[r]>nums[largest]:
                largest = r
            if largest!=i:
                nums[i], nums[largest] = nums[largest], nums[i]
                # 递归调用
                maxHeapify(largest, heapSize)

        def buildMaxHeap(heapSize):
            for i in range(heapSize//2, -1, -1):
                maxHeapify(i, heapSize)

        heapSize = len(nums)
        buildMaxHeap(heapSize)
        for i in range(len(nums)-1, len(nums)-k, -1):
            nums[0] = nums[i]
            heapSize -= 1
            maxHeapify(0, heapSize)
        return nums[0]

    """
    方法一，基于快排
    """
    def findKthLargest2(self, nums: List[int], k: int) -> int:
        import random
        def partition(l, r):
            pivot = nums[r]
            i = l-1
            for j in range(l, r):
                if nums[j] <= pivot:
                    i += 1
                    nums[j], nums[i] = nums[i], nums[j]
            nums[i+1], nums[r] = nums[r], nums[i+1]
            return i+1
        def randomSelect(l, r):
            i = random.randint(l, r)
            nums[i], nums[r] = nums[r], nums[i]
            return partition(l, r)

        def quickSecelt(l, r, k):
            if l<r:
                q = randomSelect(l, r)
                if q==k:
                    return nums[q]
                if q<k:
                    return quickSecelt(q+1, r, k)
                else:
                    return quickSecelt(l, q-1, k)
        return quickSecelt(0, len(nums)-1, len(nums)-k)


nums = [3,2,3,1,2,4,5,5,6] ; k=4
print(Solution().findKthLargest2(nums, k))

