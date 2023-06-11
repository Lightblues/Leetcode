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
https://leetcode.cn/contest/weekly-contest-344
https://leetcode.cn/circle/discuss/FDkyPg/

三道 medium, T4
Easonsi @2023 """
class Solution:
    """ 2670. 找出不同元素数目差数组 """
    def distinctDifferenceArray(self, nums: List[int]) -> List[int]:
        ans = []
        for i in range(len(nums)):
            ans.append(
                len(set(nums[:i+1])) - len(set(nums[i+1:]))
            )
        return ans
    
    """ 2672. 有相同颜色的相邻元素数目 #medium """
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        ans = []
        arr = [0] * (n+2)
        acc = 0
        for i,c in queries:
            diff = 0
            if arr[i+1]!=0:
                if arr[i+1]==arr[i]: diff -= 1
                if arr[i+1]==arr[i+2]: diff -= 1
            if c==arr[i]: diff += 1
            if c==arr[i+2]: diff += 1
            arr[i+1] = c
            acc += diff
            ans.append(acc)
        return ans
    
    """ 2673. 使二叉树所有路径值相等的最小代价 #medium 给定一颗二叉树, 可以对节点 +1, 使得所有root到leaf的路径相同的最小代价
思路0: 求出路径最大值, 尽量把加的值放到更高的节点上
    两次DFS
思路2: #贪心
    相邻的两个叶子结点值一定相同! 从下往上遍历, 其左右子树的路径和要求相同!
    [灵神](https://leetcode.cn/problems/make-costs-of-paths-equal-in-a-binary-tree/solution/tan-xin-jian-ji-xie-fa-pythonjavacgo-by-5svh1/)
拓展: 如果还有 -1 操作呢? 
    所有路径的中位数?
    """
    def minIncrements(self, n: int, cost: List[int]) -> int:
        cost = [0] + cost
        mx = [0] * (n+1)
        def dfs(i):
            l,r = 2*i, 2*i+1
            if l>n: 
                mx[i] = cost[i]
                return cost[i]
            v = max(dfs(l), dfs(r)) + cost[i]
            mx[i] = v
            return v
        dfs(1)
        # 
        # target = mx[1]
        ans = 0
        def dfs_ud(i):
            nonlocal ans
            l,r = 2*i, 2*i+1
            if l>n: return 
            target = mx[i] - cost[i]
            for ii in [l,r]:
                ans += target - mx[ii]
                dfs_ud(ii)
        dfs_ud(1)
        return ans
    def minIncrements(self, n: int, cost: List[int]) -> int:
        """ 灵神的优雅写法 """
        ans = 0
        for i in range(n // 2, 0, -1):  # 从最后一个非叶节点开始算
            ans += abs(cost[i * 2 - 1] - cost[i * 2])  # 两个子节点变成一样的
            cost[i - 1] += max(cost[i * 2 - 1], cost[i * 2])  # 累加路径和
        return ans

""" 2671. 频率跟踪器 #medium """
class FrequencyTracker:
    def __init__(self):
        self.v2cnt = defaultdict(int)
        self.f2cnt = defaultdict(int)

    def add(self, number: int) -> None:
        f = self.v2cnt[number]
        if f>0: self.f2cnt[f] -= 1
        self.v2cnt[number] += 1
        self.f2cnt[f+1] += 1

    def deleteOne(self, number: int) -> None:
        f = self.v2cnt[number]
        if f>0: 
            self.f2cnt[f] -= 1
            self.v2cnt[number] -= 1
        if f>1: self.f2cnt[f-1] += 1

    def hasFrequency(self, frequency: int) -> bool:
        return self.f2cnt[frequency]>0
    
sol = Solution()
result = [
    # sol.colorTheArray(n = 4, queries = [[0,2],[1,2],[3,1],[1,1],[2,1]]),
    sol.minIncrements(n = 7, cost = [1,5,2,2,3,3,1]),
    sol.minIncrements(n = 3, cost = [5,3,3]),
]
for r in result:
    print(r)
