"""
设计一个支持以下两种操作的数据结构：

void addNum(int num) - 从数据流中添加一个整数到数据结构中。
double findMedian() - 返回目前所有元素的中位数。


addNum(1)
addNum(2)
findMedian() -> 1.5
addNum(3)
findMedian() -> 2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-median-from-data-stream
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class MedianFinder:
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.nums = []
        self.count = 0

    def addNum(self, num: int) -> None:
        # 采用二分查找可加速
        self.count += 1
        for i in range(self.count-1):
            if self.nums[i] > num:
                self.nums.insert(i, num)
                return
        self.nums.append(num)

    def findMedian(self) -> float:
        if self.count % 2:
            return self.nums[self.count//2]
        else:
            return sum(self.nums[self.count//2-1: self.count//2+1]) / 2


import heapq
class MedianFinder2:
    def __init__(self):
        self.lo = []
        self.hi = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)   # 最大堆
        heapq.heappush(self.hi, -self.lo[0])
        heapq.heappop(self.lo)

        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -self.hi[0])
            heapq.heappop(self.hi)

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        else:
            return (self.hi[0] - self.lo[0]) / 2


sol = MedianFinder2()
sol.addNum(1)
sol.addNum(2)
print(sol.findMedian())
sol.addNum(3)
print(sol.findMedian())


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()


