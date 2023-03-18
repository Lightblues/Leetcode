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
https://leetcode-cn.com/contest/biweekly-contest-91
灵神: https://www.bilibili.com/video/BV1gd4y1b7qj/

群里说是比较难的一次双周赛, T2就是DP; T3代码量比较大, 但还是比较直观的. T4比较琐碎, 但也没啥思维量, 考代码能力. 
@2022 """
class Solution:
    """ 2465. 不同的平均值数目 """
    
    """ 2466. 统计构造好字符串的方案数 #medium 基本DP
关联: 0070. 爬楼梯
"""
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        mod = 10**9 + 7
        f = [0] * (high+1)
        f[0] = 1
        for i in range(high+1):
            if i+zero<=high: f[i+zero] = (f[i+zero]+f[i]) %mod
            if i+one<=high: f[i+one] = (f[i+one]+f[i]) %mod
        return sum(f[low:high+1]) %mod
    
    """ 2467. 树上最大得分和路径 #medium #题型 有一个树, 每个节点有分数. A从root到叶子, B从某一节点到root. 分数按照先后到达来得到. 问A能够得到的最大分数.
思路1: 先找到B的路径, 计算距离; 然后模拟A从root往叶子的搜索.
    细节: 如何处理树结构? 可以直接看成图, dfs的时候通过一个 #parent 防止重复访问即可
[灵神](https://leetcode.cn/problems/most-profitable-path-in-a-tree/solution/liang-bian-dfs-by-endlesscheng-da7j/) 也是一样的
"""
    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        n = len(edges)+1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v); g[v].append(u)
        # 计算从B到root的距离
        disToBob = [-1]*n
        def dfsBob(u, p, d=0) -> int:
            flag = u==0
            for v in g[u]:
                if v==p: continue
                f = dfsBob(v, u, d+1)
                if f: flag = True
            if flag: disToBob[u] = d
            return flag
        dfsBob(bob, -1)
        # 根据先后到达顺序计算分数
        def getScore(u, da):
            if disToBob[u]<0: return amount[u]
            db = disToBob[u]
            if da<db: return amount[u]
            elif da==db: return amount[u]//2
            else: return 0
        # 对于A进行搜索
        def dfsAlice(u, p, d=0, score=0) -> int:
            score += getScore(u, d)
            if len(g[u])==1 and g[u][0]==p: return score
            mx = -inf
            for v in g[u]:
                if v==p: continue
                mx = max(mx, dfsAlice(v, u, d+1, score))
            return mx
        return dfsAlice(0, -1)

    """ 2468. 根据限制分割消息 #hard #模拟 需要将字符串message进行分割, 要求分割后除了最后一个的长度都相同 =limit. 想要最短的分割方案. 
输出形式: `"thi<1/14>","s i<2/14>","s r<3/14>","eal<4/14>",...` 这样, 每个子串, 后缀是 <i/n>, 表示第i个子串, 总共n个子串
    注意: 这里的不同n能够容纳的message长度不是线性的, 因此不能用二分来搜索!! (考虑 n=9,10 的变化) 
from [灵神](https://leetcode.cn/problems/split-message-based-on-limit/solution/mei-ju-by-endlesscheng-gt7c/), 参见视频. 
"""
    def splitMessage(self, message: str, limit: int) -> List[str]:
        i = cap = 0
        while True:
            i += 1
            if i < 10:
                tail_len = 5  # 结尾的长度
            elif i < 100:
                if i == 10: cap -= 9  # 前面的结尾的长度都 +1，那么容量就要减小
                tail_len = 7
            elif i < 1000:
                if i == 100: cap -= 99
                tail_len = 9
            else:
                if i == 1000: cap -= 999
                tail_len = 11
            if tail_len >= limit: return []  # cap 无法增大，寄
            cap += limit - tail_len
            if cap < len(message): continue  # 容量没有达到，继续枚举

            ans, k = [], 0
            for j in range(1, i + 1):
                tail = f"<{j}/{i}>"
                if j == i:
                    ans.append(message[k:] + tail)
                else:
                    m = limit - len(tail)
                    ans.append(message[k: k + m] + tail)
                    k += m
            return ans

    
sol = Solution()
result = [
    # sol.countGoodStrings(low = 3, high = 3, zero = 1, one = 1),
    # sol.mostProfitablePath(edges = [[0,1],[1,2],[1,3],[3,4]], bob = 3, amount = [-2,4,2,-4,6]),
    # sol.mostProfitablePath([[0,1],[1,2],[2,3]], 3, [-5644,-6018,1188,-8502]), 
    sol.splitMessage(message = "this is really a very awesome message", limit = 9), 
]
for r in result:
    print(r)
