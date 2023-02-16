from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71

一上来看错了顺序直接做第三题超时, 差点崩了, 还好相较于 1723 没有卡复杂度直接暴力+剪枝通过 (子集枚举前两天还写的Orz). 第四题真的想不到.
还是第一次遇到第2,3题都是五分的.
@2022 """
class Solution:
    """ 5259. 计算应缴税款总额 """
    def calculateTax(self, brackets: List[List[int]], income: int) -> float:
        ans = 0
        for i,(upper, rate) in enumerate(brackets):
            if upper <= income:
                lower = 0 if i==0 else brackets[i-1][0]
                ans += (upper - lower) * rate
            if upper > income:
                lower = 0 if i==0 else brackets[i-1][0]
                ans += (income - lower) * rate
                break
            
        return ans / 100
    
    """ 5270. 网格中的最小路径代价 """
    def minPathCost(self, grid: List[List[int]], moveCost: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        minCost = defaultdict(lambda: inf)
        for c in grid[0]:
            minCost[c] = c
        for layer in range(m-1):
            for u in grid[layer]:
                for idx, cost in enumerate(moveCost[u]):
                    v = grid[layer+1][idx]
                    minCost[v] = min(minCost[v], minCost[u] + cost + v)
        return min(minCost[i] for i in grid[-1])
    
    
    """ 5289. 公平分发饼干 #medium 同 1723. 完成所有工作的最短时间
有一组饼干数组 cookies, 要分给k个孩子, 定义分配的不公平程度为所分配数的最大值. 要求所有分配方式中, 不公平程度最小化.
约束: 数组长度 n<=8; 分配数 k<=m
思路1: 暴力 #dfs + #剪枝
    直接暴力搜索的复杂度为 k**m
    然而因为采用DFS, 若当前分配数大于此前的最小不公平程度时, 可以进行剪枝.
    但不会带来复杂度上的下降. 在 1723题中长度 n==12 无法过.
思路2: #状态压缩 #DP #子集遍历
    我们定义 `f[i][mask]` 表示分配完前i个孩子, 当前分配的饼干集合为mask, 时的最小不公平程度.
    我们遍历分配给第i个孩子的集合sub, 这样有 `f[i][mask] = min{ max{ f[i-1][mask\sub], sum[sub] } }` 这里的sub是mask的所有子集, sum[sub] 表示sub集合中的元素之和.
    因此, 需要两层遍历, 第一层遍历i, 第二层遍历mask (还要遍历mask的所有子集). 注意到, 若我们对于mask从大到小遍历, 则可以省略dp的第一个维度.
    遍历子集采用经典的 `sub = (sub - 1) & mask` 方式.
    复杂度: 对于mask从1遍历到 1<<n, 每次遍历mask所有的子集, 其复杂度为 `O(3^n)` (恰好是排列公式). 因此总复杂度为 O(k * 3^n).
    from [灵神](https://leetcode.cn/problems/fair-distribution-of-cookies/solution/by-endlesscheng-80ao/)
    
"""
    def distributeCookies(self, cookies: List[int], k: int) -> int:
        counts = [0] * k
        ans = inf
        n = len(cookies)
        def dfs(i):
            nonlocal ans
            if i == n:
                ans = min(ans, max(counts))
                return 
            c = cookies[i]
            for ii in range(k):
                if counts[ii] + c >= ans: continue
                counts[ii] += c
                dfs(i+1)
                counts[ii] -= c
        dfs(0)
        return ans
    
    def minimumTimeRequired(self, jobs: List[int], k: int) -> int:
        """ 思路2: [灵神](https://leetcode.cn/problems/fair-distribution-of-cookies/solution/by-endlesscheng-80ao/) """
        n = len(jobs)
        # 预计算每一个mask所代表的工作集合之和
        sub2cost = [0] * (1<<n)
        for mask in range(1<<n):
            cost = 0
            for i,c in enumerate(jobs):
                if mask>>i & 1:
                    cost += c
            sub2cost[mask] = cost
        # f[i][mask] 表示给前i工人分配工作, 所有已分配的工作为为mask时的最短时间.
        # f = [[0] * (2<<n) for _ in range(k)]
        last = sub2cost[:]
        for i in range(1, k):
            new = [inf] * (1<<n)
            for mask in range(1, 1<<n):
                sub = mask
                while sub:
                    new[mask] = min(new[mask], max(last[mask^sub], sub2cost[sub]))
                    sub = (sub - 1) & mask
            last = new
        return last[-1]

    """ 2306. 公司命名 #hard #题型 #互补
有一组数量为n的单词, 从中选择 a,b 两个出来作为公司的名字: 选择方式为, 交换 a,b 的首字母, 若交换后生成的单词不再原数组中, 则用这两个单词作为公司名. 问所有不同的有效公司名的个数.
约束: n<=10^5
思路0: 根据尾序列分组. 但之后没想出来怎么缩减两两匹配的复杂度
    根据示例, 容易想到将结尾序列相同的单词分到一组 group/set 中.
    什么情况下单词组合是合法的? 假设后缀1的首字母集合为 {c,t}, 后缀2的是 {t,a}, 则两者可以搭配的组合之后 (a,c).
        因此: 条件是 交换的首字母不能出现在另一个group中.
    因此, 问题转化为: 有一组集合, 每个集合包括了一些字母. 要求从中计算所有的二元组 (ch1,ch2) 使得它们在两个不同的集合 set1,set2 中, 满足 ch1不在set2中, ch2不在set1中.
        但可能的集合数量达 2^26, 还需要两两组合复杂度不够.
思路1: 利用 #互补 的思想 #计数 #分类讨论
    再来看约束目标: 两个首字母 c1,c2 需要满足, 分别单独出现在两个集合中, 也即, 一个集合包含c1不包含c2, 另一个对称.
    因此, 我们用 `cnt[i][j]` 表示 **字母i不在集合, 而字母j在集合中的数量**.
    答案是什么? 在得到cnt计数中. 我们遍历每一个group, 我们遍历每一个组合 `(i,j) in pair(group, allCh\group)`, 将其与 `cnt[i][j]` 匹配; 将结果相加即可.
    注意, 这里是得到了整个cnt计数之后累计的, 因此 (i,j) (j,i) 都会加入到结果中.
        而原本是在遍历过程中, 直接累加进答案. 因此只考虑了一个方向; 因此需要将结果 *2.
[灵神](https://leetcode.cn/problems/naming-a-company/solution/by-endlesscheng-ruz8/)
总结: 1) 这里 #互补 的思想很有意思. 2) **在需要两两组合但复杂度明显不够的时候, 应该考虑计数, 问题是如何找到一种好的统计方式**.
"""
    def distinctNames(self, ideas: List[str]) -> int:
        """ 互补思想 from 灵神 """
        # 尾部相同的单词为一组, 统计每组中出现的首字母有哪些
        pattern2first = defaultdict(list)
        for idea in ideas:
            pattern2first[idea[1:]].append(ord(idea[0]) - ord('a'))
        ans = 0
        # 辅助数组 cnt[i][j] 记录在遍历过程中, i不在组中而j在组中的个数
        cnt = [[0] * 26 for _ in range(26)]
        for firsts in pattern2first.values():
            for i in range(26):
                # i不在组中
                if i not in firsts:
                    for j in range(26):
                        if j in firsts:
                            cnt[i][j] += 1
                # i在组中. 此时, 对于同组的所有j进行匹配: 匹配其他的有i但没有j的数量.
                else:
                    for j in range(26):
                        if j not in firsts:
                            ans += cnt[i][j]
        return ans * 2


    def distinctNames(self, ideas: List[str]) -> int:
        # 得到整个cnt之后再累积, 不需要 *2
        pattern2first = defaultdict(list)
        for idea in ideas:
            pattern2first[idea[1:]].append(ord(idea[0]) - ord('a'))
        ans = 0
        cnt = [[0] * 26 for _ in range(26)]
        allCh = set(range(26))
        for firsts in pattern2first.values():
            for i in allCh.difference(firsts):
                for j in firsts:
                    cnt[i][j] += 1
        for firsts in pattern2first.values():
            for i in firsts:
                for j in allCh.difference(firsts):
                    ans += cnt[i][j]
        return ans

    
sol = Solution()
result = [
    # sol.distributeCookies(cookies = [8,15,10,20,8], k = 2),
    # sol.distributeCookies([76265,7826,16834,63341,68901,58882,50651,75609], 8),
    
    # sol.calculateTax(brackets = [[3,50],[7,10],[12,25]], income = 10),
    # sol.calculateTax(brackets = [[1,0],[4,25],[5,50]], income = 2),
    # sol.calculateTax(brackets = [[2,50]], income = 0),
    
    # sol.minPathCost(grid = [[5,3],[4,0],[2,1]], moveCost = [[9,8],[1,5],[10,12],[18,6],[2,4],[14,3]]),
    # sol.minPathCost(grid = [[5,1,2],[4,0,3]], moveCost = [[12,10,15],[20,23,8],[21,7,1],[8,1,13],[9,10,25],[5,3,2]]),
    
    # sol.minimumTimeRequired(jobs = [1,2,4,7,8], k = 2),
    
    sol.distinctNames(ideas = ["coffee","donuts","time","toffee"]),
    sol.distinctNames(ideas = ["lack","back"]),
]
for r in result:
    print(r)
