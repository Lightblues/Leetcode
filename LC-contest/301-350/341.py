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
https://leetcode.cn/contest/weekly-contest-341

难度较低, T4 树形DP有些意思
Easonsi @2023 """
class Solution:
    """ 6376. 一最多的行 """
    def rowAndMaximumOnes(self, mat: List[List[int]]) -> List[int]:
        mx,rid = -1,-1
        for i,row in enumerate(mat):
            t = sum(row)
            if t>mx:
                mx = t; rid = i
        return rid,mx
    
    """ 6350. 找出可整除性得分最大的整数 """
    def maxDivScore(self, nums: List[int], divisors: List[int]) -> int:
        mx, ans = -1,inf
        for d in divisors:
            acc = 0
            for x in nums:
                if x%d == 0: acc+=1
            if acc>mx or (acc==mx and d<ans):
                mx=acc; ans=d
        return ans
    
    """ 6375. 构造有效字符串的最少插入数 """
    def addMinimum(self, word: str) -> int:
        word = [ord(c)-ord('a') for c in word]
        cnt3 = 1; t = -1
        for c in word:
            if c<=t:
                cnt3 += 1
                t = c
            else: t = c
        return cnt3*3 - len(word)

    """ 6378. 最小化旅行的价格总和 #hard 树上每个节点有分数, 现在有一系列的旅行路径要进行 (每条路径话费为节点和); 可对不相邻节点分数减半, 求最小代价
限制: n 50
思路1: 
    根据所要经过的路径, 统计每个节点的cnt
    然后决定对哪些不相邻节点进行减半? 类似「0337. 打家劫舍 III」, dfs 返回「减半/不减半下的最小代价」
[灵神](https://leetcode.cn/problems/minimize-the-total-price-of-the-trips/solution/lei-si-da-jia-jie-she-iii-pythonjavacgo-4k3wq/)
    """
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v); g[v].append(u)
        # 
        cnt = [0] * n   # 每个节点要经过的次数
        for s,e in trips:
            def dfs(u,fa):
                """ 返回是否能到达e """
                if u==e:
                    cnt[u] += 1
                    return True
                for v in g[u]:
                    if v==fa: continue
                    if dfs(v,u):
                        cnt[u] += 1
                        return True
                return False
            dfs(s,-1)
        # 类似 0337. 打家劫舍 III https://leetcode.cn/problems/house-robber-iii
        def dfs(u, fa):
            """ 返回减半/不减半下的最小代价 """
            noHalf = price[u] * cnt[u]
            half = noHalf // 2
            for v in g[u]:
                if v==fa: continue
                h,nh = dfs(v,u)
                half += nh
                noHalf += min(h,nh)
            return half, noHalf
        return min(dfs(0,-1))

    
sol = Solution()
result = [
    sol.minimumTotalPrice(n = 4, edges = [[0,1],[1,2],[1,3]], price = [2,2,10,6], trips = [[0,3],[2,1],[2,3]]),
]
for r in result:
    print(r)
