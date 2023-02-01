from easonsi import utils
from easonsi.util.leetcode import *
def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
== 要求数字长度
1673. 找出最具竞争力的子序列 #medium #题型
    从长度为k的子序列中找到字典序最小的.



"""
class Solution:
    """ 1673. 找出最具竞争力的子序列 #medium #题型
从长度为k的子序列中找到字典序最小的.
思路: 采用 #最小堆. 如何保证最后剩余的堆大小至少为k? 对于长n的给定序列, 位置i往后的长度为n-i, 因此堆剩余的大小至少为 `k-(n-i)`
"""
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        h = []
        n = len(nums)
        for i,num in enumerate(nums):
            # 保证剩余堆的大小至少为k
            while len(h) >= max(1, k-n+i + 1) and num<h[-1]:
                h.pop()
            h.append(num)
        return h[:k]
    
    
    
    
    
    
""" 0295. 数据流的中位数 #hard 实现一个数据结构, 可以加入数据, 并计算当前数据 #中位数.
思路1: 维护两个「平衡的」 #优先队列. 一个最大堆, 一个最小堆.
    我们分别用 mn,mx 最大堆最小堆维护 最小的一半和较大的一半数据, 并保持 size(mn) = size(mx) or size(mx)+1
    查询: 根据两个堆的大小关系返回
    插入: 根据与堆顶元素的大小关系插入, 再维护平衡性. 复杂度 O(logn)
思路2: 可以用 #有序集合 SortedList 维护数据, 并用 #双指针 记录中位数位置
进阶1: 若数据范围在 [0,100], 可以用 「计数排序统计每一类数的数量，并使用双指针维护中位数」
进阶2: 若 99% 的整数都在 0 到 100 范围内. 则可以直接用数组保存超过该范围的数字 (因为大概率没用), 若小概率中位数在这范围内的话, 暴力搜索即可.
[official](https://leetcode.cn/problems/find-median-from-data-stream/solution/shu-ju-liu-de-zhong-wei-shu-by-leetcode-ktkst/)
"""
class MedianFinder:
    def __init__(self):
        self.mn = []
        self.mx = []

    def addNum(self, num: int) -> None:
        if self.mn and num < -self.mn[0]:
            heappush(self.mn, -num)
            if len(self.mn) > len(self.mx)+1:
                heappush(self.mx, -heappop(self.mn))
        else:
            heappush(self.mx, num)
            if len(self.mx) > len(self.mn):
                heappush(self.mn, -heappop(self.mx))

    def findMedian(self) -> float:
        if len(self.mn)==len(self.mx): return (-self.mn[0]+self.mx[0])/2
        else: return -self.mn[0]

    
sol = Solution()
result = [
    # sol.mostCompetitive(nums = [3,5,2,6], k = 2),
    # sol.mostCompetitive(nums = [2,4,3,3,5,4,9,6], k = 4),
#     testClass("""["MedianFinder","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian"]
# [[],[6],[],[10],[],[2],[],[6],[],[5],[],[0],[],[6],[],[3],[],[1],[],[0],[],[0],[]]""")

]
for r in result:
    print(r)
