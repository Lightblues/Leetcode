from re import I
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
https://leetcode.cn/contest/weekly-contest-188

居然T1就是中等. T2T3 都是基本的问题建模, 值得写一写. T4也是很有意思的题型, DP还需要训练.
@2022 """
class Solution:
    """ 1441. 用栈操作构建数组 """
    def buildArray(self, target: List[int], n: int) -> List[str]:
        res = []
        ll = len(target); idx= 0
        for i in range(1, n+1):
            if idx >= ll: break
            if i == target[idx]:
                res.append("Push")
                idx += 1
            else:
                res.extend(["Push", "Pop"])
        return res
    
    """ 1442. 形成两个异或相等数组的三元组数目 #medium #题型 给定一个数组, 要求找到三元组 (i, j, k) 的数量, 使得 arr[i...j-1], arr[j...k] 的异或值相等
限制: 数组长度 300.
思路1: 注意这里要求两个相邻的子数组的异或和相等, 等价于「这些数字的异或和为0」.
    因此, 可以先求 #前缀 #异或和. 假设数组为 [1,1], 则前缀异或和为 [0,1,0]. 也即 arr[0...1] 的异或和为0. 该区间长度为2, 分割点有一个.
    细节: 注意前缀0.
这里的计数写得繁琐了, 参见[官答](https://leetcode.cn/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/solution/xing-cheng-liang-ge-yi-huo-xiang-deng-sh-jud0/)
"""
    def countTriplets(self, arr: List[int]) -> int:
        xors = [0]
        xx = 0
        for a in arr:
            xx ^= a; xors.append(xx)
        xor2idxs = defaultdict(list)
        for i,x in enumerate(xors): xor2idxs[x].append(i)
        ans = 0
        for x, idxs in xor2idxs.items():
            l = len(idxs)
            for i in range(l):
                for j in range(i+1,l):
                    ans += idxs[j] - idxs[i] - 1
        return ans
    
    """ 1443. 收集树上所有苹果的最少时间 #medium #题型 给定一个树结构, 在一些节点上有苹果. 求从根节点0出发到所有苹果节点, 并返回根节点的最短路径. 限制: n 1e5
思路1: #DFS, 记录是否需要访问该节点.
    提示: 本题就是要求出能够到达所有苹果的路径 (需要去除公共路径); 或者说, #最小生成树.
    在DFS的过程中, dfs(node) 返回一个bool值表示该子树是否包含苹果; 在遍历所有子节点的过程中, 记录所有需要访问的孩子数量, 每个孩子的访问成本为 2.
"""
    def minTime(self, n: int, edges: List[List[int]], hasApple: List[bool]) -> int:
        t = [[] for _ in range(n)]
        for u,v in edges: t[u].append(v); t[v].append(u)
        visited = [False] * n
        ans = 0
        def dfs(node) -> bool:
            # 探索根节点, 返回子树是否有苹果
            nonlocal ans
            visited[node] = True
            childsHasApple = 0  # 孩子节点中, 有苹果 (需要访问) 的节点数
            for child in t[node]:
                if visited[child]: continue
                childsHasApple += dfs(child)
            ans += 2 * childsHasApple
            return bool(childsHasApple) or hasApple[node]    # 返回 bool
        dfs(0)
        return ans
    
    """ 1444. 切披萨的方案数 #hard #题型 在一个grid表示的披萨上, 只有在部分点上才是有苹果的. 你需要切 k-1 刀分给 n个人. 
每次可以选择横/竖切, 上面/左边的部分会分给当前的人, 然后继续切. 问「切好的每块披萨上都有苹果」的方案数, 答案取mod. 限制: 长宽 50, k 10.
思路0: #暴力 解法. #记忆化 搜索
    模拟每一次切分的尝试. 用 dfs(row,col,remain) 来返回还剩余 pizza[row:, col:] 这一右下角, 需要分成remain块的方案数.
    在DFS过程中, 对于横向 row+1...n-1 和纵向的部分相应分割线分别尝试分割, 注意要保证切割的部分有苹果.
    复杂度: 状态空间 n^2*k, 每次转移需要考虑 n 种可能性, 在切割过程中还需要判断分割出去的部分是否包含苹果, 因此 `O(n^4*k)`
    注意: 直接用DFS会产生大量重复查询, 需要用记忆化搜索.
总结: 题目的形态一看就是 #DP, 但一开始想着直接写递推公式 (从右下往左上) 死活想不出来. 看到题解直接用 记忆化 搜索, 思路就比较清楚了!
[here](https://leetcode.cn/problems/number-of-ways-of-cutting-a-pizza/solution/ji-yi-hua-di-gui-bu-xu-yao-guan-dpci-xu-rong-yi-xi/)
"""
    def ways(self, pizza, k: int) -> int:
        import numpy as np
        
        module=int(1e9+7)
        rows,cols=len(pizza),len(pizza[0])
        G=np.array([np.array(['A'==ch for ch in s], dtype=bool) for s in pizza])
        # print(G)    #为了方便做子pizza切片，将pizza[]中的'A'True，'.'映射为False。用numpy库的array类非常方便
        # dfs: 以row行col列为左上角的矩形子pizza，切remain刀（按题目要求每一份都要有apple）的切法
        @lru_cache(None)
        def dfs(row,col,remain):
            if remain<=0:   #已经不用切了
                return 1 if True in G[row:,col:] else 0 # 当前子pizza含有apple时算1种。否则不符合题目所需，算0种！
            cnt=0   # 还要切remain刀。cnt记录最终切法数
            nr,nc=row,col
            while nr<rows and True not in G[nr,col:]: nr+=1   #跳过没有apple的行（切了不算数）
            while nr<rows-1:  #横着切
                nr+=1 #先+1，因为首次进入循环是pizza[nr][col:]恰好有apple，要切其下一行才对
                cnt=(cnt + dfs(nr,col,remain-1))%module     #分为 pizza[row:nr][col:]和pizza[nr:][col:] 两个子pizza
            while nc<cols and True not in G[row:,nc]: nc+=1   #跳过没有apple的列（切了不算数）
            while nc<cols-1:  #横着切
                nc+=1
                cnt=(cnt + dfs(row,nc,remain-1))%module
            # print(row,col,remain,cnt)
            return cnt
        return dfs(0,0,k-1)

    
    
sol = Solution()
result = [
    # sol.buildArray(target = [1,3], n = 3),
    # sol.countTriplets( [2,3,1,6,7]),
    # sol.countTriplets([1,1,1,1,1]),
    # sol.minTime(n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [False,False,True,False,True,True,False]),
    sol.ways(pizza = ["A..","AAA","..."], k = 3),
]
for r in result:
    print(r)
