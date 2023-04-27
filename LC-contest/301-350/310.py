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
https://leetcode.cn/contest/weekly-contest-310

T3用了贪心+堆, 感觉挺有意思. 看到灵神的还可以用差分来做. 
T4 是带约束的「最长递增子序列」, 就无法采用 0300 题的 贪心+二分 的框架了; 需要用到线段树才实现「区间查询」.

@2022 """
class Solution:
    """ 2404. 出现最频繁的偶数元素 """
    
    """ 2405. 子字符串的最优划分 #medium #贪心 """
    
    """ 2406. 将区间分为最少组数 #medium #题型 有一组 [s,e] 区间, 要求划分成数量最少的组, 每一组区间之间不相交. 限制: n 1e5; 区域范围 1e6
思路1: 根据开始时间排序. 记录当前所划分的组; 遍历过程中, 每次在合法的组中添加即可 #贪心 思想.
    可以用一个 #堆 来判断是否合法.
思路2: 看成「上车下车问题」. 记录同时在车上的最多有多少人即可.
    如何统计区间人数? 用 #差分.
    优化: 本地的数字范围在 L=1e6. 这样复杂度 O(max{n, L}). 是否可以优化? 
        一种方式是用 #平衡树 来记录区间端点的值, 这样复杂度为 O(n logn)
参见 [灵神](https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/solutions/1816294/by-endlesscheng-ze3t/)
"""
    def minGroups(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        ends = []
        cnt = 0; avas = 0
        for s,e in intervals:
            while ends and ends[0] < s:
                heapq.heappop(ends)
                avas += 1
            if avas==0:
                cnt += 1
            else: avas -= 1
            heapq.heappush(ends, e)
        return cnt
    def minGroups(self, intervals: List[List[int]]) -> int:
        # 思路2: 看成「上车下车问题」. 记录同时在车上的最多有多少人即可. 采用 #差分
        mn, mx = min(i[0] for i in intervals), max(i[1] for i in intervals)
        diff = [0] * (mx-mn+2)
        for s,e in intervals:
            diff[s-mn] += 1
            diff[e-mn+1] -= 1
        for i in range(1, len(diff)):
            diff[i] += diff[i-1]
        return max(diff)

    """ 2407. 最长递增子序列 II #hard #题型 #review #hardhard 对于给定的数组, 找到其中最长的严格递增子序列, 要求相邻元素差值不超过 k.
限制: n 1e5; k 1e5
思路1: #DP + #线断树
    建立 {val: LIS} 的字典记录以val结尾的LIS 长度. 遍历过程中, 对于val, 在 [val-k,val] 范围内查询最大值.
    考虑到数据范围, 可以采用 #线段树.
    技巧: 由于我们线段树的定义从节点1开始, 下面注释部分要避免出现区间非法! 为此, 我们可以将数字整体shift一下.
拓展: 若本题的数据范围在 1e9, 则需要采用 #动态开点线段树. 
参见 [灵神](https://leetcode.cn/problems/longest-increasing-subsequence-ii/solution/zhi-yu-xian-duan-shu-pythonjavacgo-by-en-p1gz/)
"""
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        # 思路1: 线段树. 注意下面因为「线段树从1开始」导致的边界情况.
        # 线段树框架
        # u = max(nums)
        u = max(nums) + 1  # 对于num进行shift, 从而避免下面注释部分的判断.
        mx = [0] * (u*4)
        def modify(o,l,r,i,val):
            # 修改 a[i] = val
            if l==r: mx[o]=val; return
            m = (l+r)//2
            if i<=m: modify(o*2,l,m,i,val)
            else: modify(o*2+1,m+1,r,i,val)
            mx[o] = max(mx[o*2], mx[o*2+1])
        def query(o,l,r,L,R):
            # 查询 max(a[L:R+1])
            if L<=l and r<=R: return mx[o]
            res = 0
            m = (l+r)//2
            if L<=m: res = query(o*2,l,m,L,R)
            if R>m: res = max(res, query(o*2+1,m+1,r,L,R))
            return res
        
        # for x in nums:
        #     # 注意, 线段树从 1 开始!!!
        #     if x==1: 
        #         modify(1,1,u,1,1)       # 都是正数, 次数长度一定为1
        #     else: 
        #         res = 1 + query(1,1,u,max(1,x-k),x-1)     # 这里的 x-1 应该 >= 1
        #         modify(1,1,u,x,res)
        for x in nums:
            x += 1
            res = 1 + query(1,1,u,max(1,x-k),x-1)
            modify(1,1,u,x,res)
        return mx[1]        # 对于线段树, 最大值就是根节点.
    
sol = Solution()
result = [
    # sol.minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]]),
    # sol.minGroups([[1,3],[5,6],[8,10],[11,13]]),
    sol.lengthOfLIS(nums = [4,2,1,4,3,4,5,8,15], k = 3), 
],
for r in result:
    print(r)
