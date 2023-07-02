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
https://leetcode.cn/contest/weekly-contest-349
https://leetcode.cn/circle/discuss/bvOqiS/

T2因为没有注意到边界条件WA了一次; T3直接暴力求解. 

Easonsi @2023 """
class Solution:
    """ 2733. 既不是最小值也不是最大值 """
    
    """ 2734. 执行子串操作后的字典序最小字符串 """
    def smallestString(self, s: str) -> str:
        ss = list(s)
        used = False
        for i,c in enumerate(ss):
            if c=='a' and used: break
            if c!='a':
                used = True
                ss[i] = chr(ord(c)-1)
        # 必须要执行一次操作
        if used==False:
            ss[-1] = 'z'
        return ''.join(ss)
    
    """ 2735. 收集巧克力 #medium 题目相见 https://leetcode.cn/problems/collecting-chocolates/
限制: n 1e3
思路1: #DP 求解操作x次后每个糖果可以取到的最小值
    复杂度: O(n^2)
[灵神](https://leetcode.cn/problems/collecting-chocolates/solution/qiao-miao-mei-ju-pythonjavacgo-by-endles-5ws2/)
    """
    def minCost(self, nums: List[int], x: int) -> int:
        n = len(nums)
        mcost = nums[:]
        ans = sum(nums)
        nnums = deque(nums)
        for i in range(n-1):
            nnums.appendleft(nnums.pop())
            for j in range(n):
                if nnums[j]<mcost[j]: mcost[j] = nnums[j]
            nans = sum(mcost) + x*(i+1)
            ans = min(ans, nans)
        return ans
    
    """ 2736. 最大和查询 #hard 对于两个长n数组元素分别记为 (x,y), 完成q次查询. 每次从分别大于 (qx,qy) 的组合中, 调出 x+y 最大值
限制: n 1e5; q 1e5
[看成二维平面上的点]
思路1: #单调栈 + #二分; #排序
    首先排序: 对于query[x] 逆序之后, 动态维度满足x的pairs! 观察这些pairs满足什么条件?
    模拟: 假设一开始有 (x=4,y=2, x+y=6), 分类讨论:
        1] 对于更小的 y'<=y, 例如 (x'=3,y'=1), 由于x是递减的, 所以必然有 x'+y'<x+y, 没用!
        2] 若 y'>y, 我们需要入栈. 进一步考虑:
            对于 (x'=2,y'=3, x'+y'=5) 它有更大的y可以满足更宽松的条件, 直接入栈;
            对于 (x'=3,y'=3, x'+y'=6), 它有更大的y的同时x+y也更大, 因此原本的 (x=4,y=2, x+y=6) 就没用了, 弹出;
            总结来说, 我们可以维护栈内 y 递增, x+y 递减的单调栈.
        代码上, stack只需要维护后两个元素即可~
思路2: #线段树 我们可以记录所有的 (y,x+y) 二元组, 然后在 >=y 的部分中找到最大的 x+y, 因此可以用线段树维护最大值.
    见 灵神 https://www.bilibili.com/video/BV15V4y1m7Sb
[灵神](https://leetcode.cn/problems/maximum-sum-queries/solution/pai-xu-dan-diao-zhan-shang-er-fen-by-end-of9h/)
关联 [KG-Tree](https://zhuanlan.zhihu.com/p/112246942)
    """
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        pairs = sorted(zip(nums1, nums2), key=lambda x: x[0], reverse=False)
        i = len(pairs)-1
        ans = [-1] * len(queries)
        st = []
        for qidx, (x,y) in sorted(enumerate(queries), key=lambda x: x[1][0], reverse=True):
            # 动态更新 st
            while i>=0 and pairs[i][0]>=x:
                a,b = pairs[i][1],pairs[i][0]+pairs[i][1]
                i -= 1
                # 1] 
                if st and st[-1][0]>=a: continue
                # 2] 
                while st and st[-1][1]<=b: st.pop()
                st.append((a, b))
            # 查询
            idx = bisect.bisect_left(st, (y,))
            if idx<len(st): ans[qidx] = st[idx][1]
        return ans


sol = Solution()
result = [
    # sol.smallestString(s = "cbabc"),
    # sol.smallestString('leetcode'),
    # sol.minCost(nums = [20,1,15], x = 5),
    # sol.minCost(nums = [1,2,3], x = 4),
    sol.maximumSumQueries(nums1 = [4,3,1,2], nums2 = [2,4,9,5], queries = [[4,1],[1,3],[2,5]]),
    sol.maximumSumQueries(nums1 = [3,2,5], nums2 = [2,3,4], queries = [[4,4],[3,2],[1,1]]),
    sol.maximumSumQueries(nums1 = [2,1], nums2 = [2,3], queries = [[3,3]]),
]
for r in result:
    print(r)
