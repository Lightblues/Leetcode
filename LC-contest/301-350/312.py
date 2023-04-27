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
https://leetcode.cn/contest/weekly-contest-312


@2022 """
class Solution:
    """ 2418. 按身高排序 """
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        persons = list(zip(heights, names))
        return [i[1] for i in sorted(persons, reverse=True)]
    
    """ 2419. 按位与最大的最长子数组 """
    def longestSubarray(self, nums: List[int]) -> int:
        mx = max(nums)
        ans = c = 0
        for i in nums:
            if i!=mx: c = 0
            else: c += 1; ans = max(ans, c)
        return ans
    
    """ 2420. 找到所有好下标 #medium 「好下标」的定义是, 对于idx, 其左侧k长序列是非递增的, 右侧k长序列是非递减的. 找到长n数组中所有的好下标
思路1: #预处理 得到数组前向的非递增最大长度, 和后向的非递增最大长度. 则要求等价于, `l[i-1]>=k and r[i+1]>=k`.
"""
    def goodIndices(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        
        l = [1] * n
        for i in range(1, n):
            if nums[i]<=nums[i-1]: l[i] += l[i-1]
        r = [1] * n
        for i in range(n-2, -1, -1):
            if nums[i]<=nums[i+1]: r[i] += r[i+1]
        ans = []
        # for i, (a, b) in enumerate(zip(l, r)):
        #     if a>=k+1 and b>=k+1: ans.append(i)
        for i in range(k, n-k):
            if l[i-1]>=k and r[i+1]>=k: ans.append(i)
        return ans
    
    """ 2421. 好路径的数目 #hard #题型 #review. 在n个节点的一棵树上, 统计符合要求的路径数量: 要求首尾的val相同, 并且经过节点的值要 <= val. 限制: n 3e4; 
https://leetcode.cn/problems/number-of-good-paths/
思路1: #DFS, 递归过程中返回当前子树下可能匹配的合法起点/终点. 卡在时间边界上.
    问题是, 如何汇总信息? 例如, 节点的两个孩子分别返回 {2:2}, {2:3}, 节点本身的 val=2. 则所有的匹配数量有 2+3+3*2. 
    当孩子较多的时候呢? 注意 **可以直接累加计数**. 因为前序节点内部已经进行了匹配, 只需要考虑新加入节点和前序节点的匹配. (注意是乘法!)
    复杂度: 大概是 O(n^2) ? 还是说是 O(n log^2(n)). see [here](https://leetcode.cn/problems/number-of-good-paths/solution/by-tsreaper-f91w/)
思路2: #并查集. 从小到大的顺序添加节点连边 (该数字作为起点的合法路径范围), 若所连的区间内也包含该数字, 则可以构成合法路径.
    具体参见 [灵神代码](https://leetcode.cn/problems/number-of-good-paths/solution/bing-cha-ji-by-endlesscheng-tbz8/)
    复杂度: O(n logn + a n). 前者为排序, 后者为并查集
"""
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        # 思路1: #DFS
        n = len(vals)
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)
        ans = 0
        seen = set()
        def dfs(u):
            # 返回一个字典, {val: cnt} 表示值为 val 的合法节点的数量.
            nonlocal ans
            ans += 1        # 节点自己也构成合法路径.
            seen.add(u)
            val = vals[u]
            ret = {val: 1}
            for v in g[u]:
                if v in seen: continue
                r = dfs(v)
                for k,v in r.items():
                    if k<val: continue
                    if k in ret: 
                        ans += ret[k] * v   # 注意需要乘上 v
                        ret[k] += v
                    else: ret[k] = v
            return ret
        dfs(0)
        return ans
    
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        # 思路2: #并查集.
        n = len(vals)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图

        # 并查集模板
        fa = list(range(n))
        # size[x] 表示节点值等于 vals[x] 的节点个数，如果按照节点值从小到大合并，size[x] 也是连通块内的等于最大节点值的节点个数
        size = [1] * n
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        ans = n
        for vx, x in sorted(zip(vals, range(n))):
            fx = find(x)
            for y in g[x]:
                y = find(y)
                if y == fx or vals[y] > vx: continue  # 只考虑最大节点值比 vx 小的连通块
                if vals[y] == vx:  # 可以构成好路径. 注意由于是从小到大遍历的, 这里相等就是最大值.
                    ans += size[fx] * size[y]  # 乘法原理
                    size[fx] += size[y]  # 统计连通块内节点值等于 vx 的节点个数
                fa[y] = fx  # 把小的节点值合并到大的节点值上
        return ans

    
sol = Solution()
result = [
    # sol.longestSubarray(nums = [1,2,3,3,2,2]),
    # sol.longestSubarray(nums = [1,2,3,4]),
    # sol.goodIndices(nums = [2,1,1,1,3,4,1], k = 2),
    # sol.goodIndices(nums = [2,1,1,2], k = 2),
    # sol.goodIndices([878724,201541,179099,98437,35765,327555,475851,598885,849470,943442], 4)
    sol.numberOfGoodPaths(vals = [1,3,2,1,3], edges = [[0,1],[0,2],[2,3],[2,4]]),
    sol.numberOfGoodPaths(vals = [1,1,2,2,3], edges = [[0,1],[1,2],[2,3],[2,4]]),
    sol.numberOfGoodPaths(vals = [1], edges = []),
    sol.numberOfGoodPaths([2,5,5,1,5,2,3,5,1,5], [[0,1],[2,1],[3,2],[3,4],[3,5],[5,6],[1,7],[8,4],[9,7]])
]
for r in result:
    print(r)
