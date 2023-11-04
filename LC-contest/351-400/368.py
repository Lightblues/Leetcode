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
https://leetcode.cn/contest/weekly-contest-368
https://leetcode.cn/circle/discuss/haZ1d7/

Easonsi @2023 """

""" 预处理 1....MX 这些数字的因子, 筛法
可以用到 T4中优化 
"""
factors = [[] for _ in range(201)]
for i in range(1, 201):
    for j in range(i * 2, 201, i):
        factors[j].append(i)



class Solution:
    """ 2909. 元素和最小的山形三元组 II #medium
    
    """
    def minimumSum(self, nums: List[int]) -> int:
        n = len(nums)
        pre = [inf] * (n)
        for i in range(n-1):
            pre[i+1] = min(pre[i], nums[i])
        suf = [inf] * (n)
        for i in range(n-1,0,-1):
            suf[i-1] = min(suf[i], nums[i])
        mn = inf
        for x,p,s in zip(nums, pre, suf):
            if x>p and x>s:
                mn = min(mn, x+p+s)
        return mn if mn!=inf else -1
    
    """ 2910. 合法分组的最少组数 #medium #题型 转为题目, 本质就是对于一组数字 vals, 可否将每个数字都拆成 k/k+1 的小组. 要求组数最少 (最大的k)
限制: n = sum(vals) 1e5
思路1: 平凡的做法, 关键是 #复杂度分析
    一开始的时候, 不敢 #暴力 去尝试. 但分析一下复杂度, 发现完成是feasible的!
    对于一个大小为 l=len(vals) 的数组和给定的k, 我们可以在 O(l) 的时间内验证是否可行. 而对于k, 它的取值范围必然在 [1...min(vals)] 中! 
        因此, 整体复杂度就是 O(len(vals)) * O(min(vals)), 因此是 O(sum(val)) 级别的! 完全可接受
    """
    def minGroupsForValidAssignment(self, nums: List[int]) -> int:
        vals = Counter(nums).values()
        mn = min(vals)
        def test(k, vals=vals):
            """ 将vals分成大小为 k/k+1 组 """
            ans = 0
            for val in vals:
                a,r = divmod(val, k+1)
                if r==0: ans += a
                else:
                    # 注意 r<=k
                    if r+a >= k: ans += a+1
                    else: return -1
            return ans
        for k in range(mn, 0, -1):
            ans = test(k)
            if ans != -1: return ans
        return -1
    
    
    """ 2911. 得到 K 个半回文串的最少修改次数 #hard
限制: n 200
思路1: #DP 
    记 f[i,k] 表示将前i个字符串分割成k组的最少修改次数
        假设已知 g[i,j] 表示将 s[i...j] 变为半回文的代价.
        则有递推 f[i,k] = min(f[ii,k-1]+g[ii+1,i]) for ii in [0...i-1]
        边界: f[0,0] = 0; 目标: f[n,k]
        复杂度: O(n^3)
    子问题 g[i,j]
        对于「得到回文串的最小修改次数」, 可以在O(n)得到; 现在「半回文串」, 暴力枚举可能的长度 (总长度的因子), 数量级在 O(logn), 因此整体复杂度为 O(nlogn)
        整体复杂度: 需要枚举 i,j, 因此是 O(n^3 logn)
[灵神](https://leetcode.cn/problems/minimum-changes-to-make-k-semi-palindromes/solutions/2493147/yu-chu-li-ji-yi-hua-sou-suo-by-endlessch-qp47/)
相关题单
分成（恰好/至多）k 个连续区间
    410. 分割数组的最大值
    813. 最大平均值和的分组 1937
    1278. 分割回文串 III 1979
    1335. 工作计划的最低难度 2035
    2478. 完美分割的方案数 2344
最小化分割出的区间个数 / 元素总和等
    132. 分割回文串 II
    2707. 字符串中的额外字符 1736
    2767. 将字符串分割为最少的美丽子字符串 1865
    1105. 填充书架 2014
"""
    def minimumChanges(self, s: str, k: int) -> int:
        def getP(s):
            """ 得到回文串的最小修改次数 """
            n = len(s)
            ans = 0
            for i in range(n//2):
                ans += s[i]!=s[n-1-i]
            return ans
        def getSemiP(s):
            """ 得到半回文串的最小修改次数 """
            n = len(s)
            # 注意, 单个字符不算!
            if n==1: return inf
            ans = inf
            for i in range(1,n):
                if n%i==0:
                    ans = min(ans, sum(
                        getP(s[j::i]) for j in range(i)
                    ))
            return ans
        n = len(s)
        g = [[inf] * n for _ in range(n)]
        for i,j in product(range(n), repeat=2):
            if i>j: continue
            g[i][j] = getSemiP(s[i:j+1])
        # print(g)
        f = g[0][:]
        for _ in range(k-1):
            # 分割成 _+1 组, 实际上前面的几个没有意义
            # f = [min(f[ii]+g[ii+1][i] for ii in range(i)) for i in range(n)]
            f =[inf] + [min(f[ii]+g[ii+1][i] for ii in range(i)) for i in range(1,n)]
        return f[-1]
    
sol = Solution()
result = [
    # sol.minimumSum(nums = [8,6,1,5,3]),
    # sol.minimumSum(nums = [5,4,8,7,10,2]),
    # sol.minimumSum(nums = [6,5,4,3,4,5]),
    # sol.minGroupsForValidAssignment(nums = [3,2,3,2,3]),
    # sol.minGroupsForValidAssignment(nums = [10,10,10,3,1,1]),
    sol.minimumChanges(s = "abcac", k = 2),
    sol.minimumChanges(s = "abcdef", k = 2),
    sol.minimumChanges(s = "aabbaa", k = 3),
    sol.minimumChanges("acba", 2), 
]
for r in result:
    print(r)
