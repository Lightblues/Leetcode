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

0862. 和至少为 K 的最短子数组 #hard
    #todo 灵神总结的单调队列的题目. 

@2022 """
class Solution:
    """ 0862. 和至少为 K 的最短子数组 #hard 给定一个数组 (元素可以是负数), 要求找到其中和至少为k的非空的最短子数组, 返回这个最短长度. 限制: n 1e5; k 1e9
思路0: 想参考「最大子数组」, 建立 {val: minL} 字典. 但想了一下并不对! 
    问题在于, 用下面的思路, 只能求到最大和, 并不能求到最短长度. 
思路1: 错了. 尝试用 #双指针 优化思路0. 但是, 不能处理负数的情况.
    错误的例子 [84,-37,32,40,95], 167
    关联: 0209. 长度最小的子数组 #medium 和本题的区别在于, 都是正整数.
思路2: 采用 #单调队列, 并且考虑 #前缀和. 
    先说答案: 先计算出前缀和. 在遍历过程中, 维护单调递增的队列结构. (优化2, 见图)
        换言之: 前缀和中的单调递增结构才可能构成答案. 
    见 [灵神](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/solution/liang-zhang-tu-miao-dong-dan-diao-dui-li-9fvh/)
"""
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # 思路0 #WA
        n = len(nums)
        s2minL = defaultdict(lambda: n+1)
        acc = 0; start_idx = -1
        for i,x in enumerate(nums):
            acc += x
            if acc > 0:
                s2minL[acc] = min(s2minL[acc], i-start_idx)
            else:
                acc = 0; start_idx = i
        # 根据val排序, 顺序找到最小的长度. 
        s2minL = sorted(s2minL.items(), key=lambda x: x[0])
        idx = bisect_left(s2minL, (k, 0))
        return max(i[1] for i in s2minL[idx:]) if idx < len(s2minL) else -1
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # WA. 只能处理正数的情况. 错误的例子 [84,-37,32,40,95], 167
        ans = inf
        l = r = 0
        acc = 0
        for r,x in enumerate(nums):
            acc += x
            if acc <= 0:
                acc = 0; l = r
            else:
                if acc >= k:
                    while l<r and acc-nums[l]>=k:
                        acc -= nums[l]
                        l += 1
                    ans = min(ans, r-l+1)
        return ans if ans!=inf else -1
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

    """ 0209. 长度最小的子数组 #medium 和本题的区别在于, 都是正整数.
    关联: 0862. 和至少为 K 的最短子数组 #hard
    思路1: #双指针. 
    """
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        ans = inf
        l = r = 0
        acc = 0
        for r,x in enumerate(nums):
            acc += x
            if acc <= 0:
                acc = 0; l = r
            else:
                if acc >= target:
                    while l<r and acc-nums[l]>=target:
                        acc -= nums[l]
                        l += 1
                    ans = min(ans, r-l+1)
        return ans if ans!=inf else 0

    
sol = Solution()
result = [
    sol.shortestSubarray(nums = [2,-1,2], k = 3),
    sol.shortestSubarray([1,2], 4),
    sol.shortestSubarray([84,-37,32,40,95], 167)
]
for r in result:
    print(r)
