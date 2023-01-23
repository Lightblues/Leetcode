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
list from [灵神](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/solution/liang-zhang-tu-miao-dong-dan-diao-dui-li-9fvh/)
单调队列：
    面试题 59-II. 队列的最大值（单调队列模板题）
    0239. 滑动窗口最大值
    1438. 绝对差不超过限制的最长连续子数组
    0862. 和至少为 K 的最短子数组 #hard 给定一个数组 (元素可以是负数), 要求找到其中和至少为k的非空的最短子数组, 返回这个最短长度.

中间两道题见 [slide]

Easonsi @2023 """
class Solution:
    """ 0862. 和至少为 K 的最短子数组 #hard 给定一个数组 (元素可以是负数), 要求找到其中和至少为k的非空的最短子数组, 返回这个最短长度. 限制: n 1e5; k 1e9
思路1: 错了. 尝试用 #双指针. 但是, 不能处理负数的情况.
    错误的例子 [84,-37,32,40,95], 167
思路2: 采用 #单调队列, 并且考虑 #前缀和. 
    先说答案: 先计算出前缀和. 在遍历过程中, 维护单调递增的队列结构. (优化2, 见图)
        换言之: 前缀和中的单调递增结构才可能构成答案. 
    见 [灵神](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/solution/liang-zhang-tu-miao-dong-dan-diao-dui-li-9fvh/)
关联: 「0209. 长度最小的子数组」 #medium 区别在于都是正数了
"""
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # 思路2: 采用 #单调队列, 并且考虑 #前缀和.
        accs = list(accumulate(nums, initial=0))    # 需要用到哨兵
        q = deque()
        ans = inf
        for i,s in enumerate(accs):
            while q and s <= accs[q[-1]]:
                # 优化2: 递增
                q.pop()
            while q and s-accs[q[0]] >= k:
                # 优化1: 匹配过的left 不会产生更短的合法区间
                idx = q.popleft()
                ans = min(ans, i-idx)
            q.append(i)
        return ans if ans!=inf else -1

    
    
    
    
""" 面试题59 - II. 队列的最大值 #hard 要求实现一个队列, 能够得到当前元素最大值. 要求三个操作的复杂度均为 O(1). 
思路1: 用一个递减的 #单调队列 来维护可能的最大值
"""
class MaxQueue:
    def __init__(self):
        self.q = deque()
        self.mxQ = deque()

    def max_value(self) -> int:
        if len(self.q)==0: return -1
        return self.mxQ[0]

    def push_back(self, value: int) -> None:
        self.q.append(value)
        while self.mxQ and self.mxQ[-1]<value: 
            self.mxQ.pop()
        self.mxQ.append(value)

    def pop_front(self) -> int:
        if len(self.q)==0: return -1
        v = self.q.popleft()
        if self.mxQ[0]==v: self.mxQ.popleft()
        return v

sol = Solution()
result = [
    # sol.shortestSubarray(nums = [2,-1,2], k = 3),
    # sol.shortestSubarray([1,2], 4),
    # sol.shortestSubarray([84,-37,32,40,95], 167),
#     testClass("""["MaxQueue","pop_front","max_value"]
# [[],[],[]]"""),
    
]
for r in result:
    print(r)
