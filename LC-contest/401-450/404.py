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
https://leetcode.cn/contest/weekly-contest-404
https://leetcode.cn/circle/discuss/wOaR6K/

T3 经典 #题型: "寻找一个最长的子序列，满足子序列奇数项都相同，偶数项都相同"
T4 关于树的直径, 也比较经典 #题型
Easonsi @2023 """
class Solution:
    """ 3200. 三角形的最大高度 
实际上可以优化到 O(1), 见 [ling](https://leetcode.cn/problems/maximum-height-of-a-triangle/solutions/2826643/o1-shu-xue-gong-shi-pythonjavacgo-by-end-t2ht/)
"""
    def maxHeightOfTriangle(self, red: int, blue: int) -> int:
        def f(x):
            a = -1; now = 1
            xx = x
            while xx >= now:
                xx -= now
                a = now
                now += 2
            b = 0; now = 2
            xx = x
            while xx >= now:
                xx -= now
                b = now
                now += 2
            return a, b
        a1, b1 = f(red)
        a2, b2 = f(blue)
        ans = max(
            min(a1,b2) + 1,
            min(a2,b1) + 1
        )
        return ans
        
    """ 3201. 找出有效子序列的最大长度 I #medium 找到最长的子序列, 满足相邻元素之和 %2 都相等
(sub[0] + sub[1]) % 2 == (sub[1] + sub[2]) % 2 == ... == (sub[x - 2] + sub[x - 1]) % 2
限制: n 2e5
    """
    def maximumLength(self, nums: List[int]) -> int:
        n = len(nums)
        nums = [i%2 for i in nums]
        ans = max(nums.count(0), nums.count(1))
        flag = nums[0]; cnt = 1
        for i in range(1, n):
            if nums[i] + flag == 1:
                cnt += 1
                flag = 1 - flag
        return max(ans, cnt)
    
    """ 3202. 找出有效子序列的最大长度 II #medium 找到最长的子序列, 满足相邻元素之和 %k 都相等
也即, (sub[0] + sub[1]) % k == (sub[1] + sub[2]) % k == ... == (sub[x - 2] + sub[x - 1]) % k
限制: n 1e3 k 1e3
思路1: 对每个元素 %k, 则子序列一定是 [i,j,i,j,...] 形式的! 
    考虑每一个可能的x, 考虑它和另一个元素的匹配: x出现的位置在 idx_1, idx_2, ...idx_k, 考虑它们中间夹的最多的元素! 
        实际上, 需要增加边界 [0, idx_1, idx_2, ...idx_k, n]
    如何统计 "最多的元素"? 可以用一个count, 对于每个间隔 (s,e) 之间的元素计数! 
        注意需要处理边界情况, 见注释
思路2: #DP
    问题定义: "寻找一个最长的子序列，满足子序列奇数项都相同，偶数项都相同"
    我们用 f[x,y] 记录最后两项分别为 x,y 的子序列的最大长度! 
    从左到右遍历数组, 有递推: 
        f[x,y] = f[y,x] + 1
    初始化: 全0即可! 
    答案就是矩阵最大值! 
[ling](https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-ii/solutions/2826591/deng-jie-zhuan-huan-dong-tai-gui-hua-pyt-z2fs/)
"""
    def maximumLength(self, nums: List[int], k: int) -> int:
        nums = [i%k for i in nums]
        n = len(nums)
        ans = max(Counter(nums).values())
        if ans == n: return ans
        # 预处理边界位置
        ridx, lidx = {}, {}
        for i,x in enumerate(nums):
            if x not in lidx: lidx[x] = i
            ridx[x] = i
        def f(nums, x):
            idxs = [i for i in range(n) if nums[i] == x]
            cnt = Counter()
            for s,e in zip([-1]+idxs, idxs+[n]):
                ss = set(nums[s+1:e])
                for i in ss: cnt[i] += 1
            mx = max(cnt.values())
            # 边界的处理! 注意到可能出现多个重复出现mx次的元素, 根据它和x的边界情况, 最长子序列可能是 [2*mx-1 ~ 2*mx+1]
            ans_ = 2*mx-1
            if 2*mx + 1 <= ans: return 0
            for a,c in cnt.items():
                if c!=mx: continue
                add = (lidx[x]<lidx[a]) + (ridx[x]>ridx[a]) - 1  # [-1, 0, 1]
                if add == 1: return 2*mx + 1    # early stop
                ans_ = max(ans_, 2*mx + add)
            return ans_
        for x in range(k):
            if x not in lidx: continue
            ans = max(ans, f(nums, x))
        return ans
    
    """ 3203. 合并两棵树后的最小直径 #hard 给定两棵树, 可以连一条边, 问得到的数的最小直径
限制: n,m 1e5 
思路1: #分类讨论 + 直觉
    注意到, 可能出现的情况有两种! 假设两棵树的直径分别为 d1, d2
    第一, 某一棵树的直径特别大, 那么拼起来之后还是不变!
    否则, 选择一个root使得 "这棵树的高度最小", 显然选直径中点! 
        然后, 将两棵树拼接 root, 则经过这个新的边的最大长度为 ceil(d1/2) + ceil(d2/2) + 1
    综合上述分类即可
see [ling](https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/solutions/2826587/lian-jie-zhi-jing-zhong-dian-pythonjavac-0e1c/)
    """
    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        def get_diameter(edges):
            n = len(edges) + 1
            g = [[] for _ in range(n)]
            for u,v in edges:
                g[u].append(v)
                g[v].append(u)
            
            diameter = 0        # NOTE: global variable!!
            def dfs(u, fa) -> int:
                # 返回从u出发的不经过fa的链路最大长度
                nonlocal diameter
                max_link_len = 0
                for v in g[u]:
                    if v == fa: continue
                    sub_link_len = dfs(v, u) + 1
                    diameter = max(diameter, sub_link_len + max_link_len)
                    max_link_len = max(max_link_len, sub_link_len)
                return max_link_len
            dfs(0, -1)
            return diameter
            
        d1 = get_diameter(edges1)
        d2 = get_diameter(edges2)
        return max(d1, d2, ceil(d1/2) + ceil(d2/2) + 1)
        
sol = Solution()
result = [
    # sol.maxHeightOfTriangle( red = 10, blue = 1),
    # sol.maximumLength( nums = [1,2,1,1,2,1,2]),
    
    # sol.maximumLength(nums = [1,2,3,4,5], k = 2),
    # sol.maximumLength(nums = [1,4,2,3,1,4], k = 3),
    # sol.maximumLength([2,8], 1),
    sol.minimumDiameterAfterMerge(edges1 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]], edges2 = [[0,1],[0,2],[0,3],[2,4],[2,5],[3,6],[2,7]]),
]
for r in result:
    print(r)
