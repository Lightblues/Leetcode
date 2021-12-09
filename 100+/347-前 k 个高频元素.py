"""
给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]

输入: nums = [1], k = 1
输出: [1]
"""
from typing import List
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        from collections import Counter
        nCounter = Counter(nums)

        # import queue
        # 有问题，当 queue 满时，优先队列的实现会等待优先级最高的出了再入
        # q = queue.PriorityQueue(k)
        # for k, v in nCounter.items():
        #     q.put((-v, k))
        # res = []
        # for _ in range(k):
        #     res.append(q.get())

        import heapq
        nList = [(v,k) for k, v in nCounter.items()]
        h = nList[:k]
        heapq.heapify(h)
        for item in nList[k:]:
            heapq.heappushpop(h, item)
        # res = heapq.nlargest(k, h)
        res = [v for frq, v in h]
        return res

    def topKFrequent_quicksort(self, nums: List[int], k: int) -> List[int]:
        from collections import Counter
        nCounter = Counter(nums)
        nList = [(v, k) for k, v in nCounter.items()]

        def quicksort(l, r, q):
            # print("Split: ", nList[l:r+1])
            # 基于排序的第 q 的元素划分 nList
            if l<r:
                ret = partition(l, r)
                if ret == q:
                    return
                if ret < q:
                    quicksort(ret+1, r, q)
                else:
                    quicksort(l, ret-1, q)

        def partition(l, r) -> int:
            pivot = nList[r]
            i = l-1
            for j in range(l, r):
                if nList[j] <= pivot:
                    i += 1
                    nList[j], nList[i] = nList[i], nList[j]
            nList[i+1], nList[r] = nList[r], nList[i+1]
            return i+1

        if k==len(nList):
            return [v for fre, v in nList]

        quicksort(0, len(nList)-1, len(nList)-k)
        return [v for fre, v in nList[-k:]]


# nums = [1,1,1,2,2,3]; k = 2
# nums = [1,2]; k=2
nums = [1,1,1,2,2,3]
k = 2
print(Solution().topKFrequent_quicksort(nums, k))




