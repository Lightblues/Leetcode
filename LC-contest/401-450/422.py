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
https://leetcode.cn/contest/weekly-contest-422
T2/3 Dijkstra
T4 排列 #题型
Easonsi @2024 """
class Solution:
    """ 3340. 检查平衡字符串 """
    def isBalanced(self, num: str) -> bool:
        odd = sum(map(int, num[::2]))
        even = sum(map(int, num[1::2]))
        return odd == even
    
    """ 3341. 到达最后一个房间的最少时间 I #medium 要从 (0,0) 到达 (n-1,m-1), 移动一步的时间需要1, 同时每个位置有最早可以到达的时间限制 """
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        n,m = len(moveTime), len(moveTime[0])
        dist = {}
        h = [(0,0,0)] # (d, x,y)
        while h:
            d, x,y = heapq.heappop(h)
            if (x,y) in dist: continue
            dist[(x,y)] = d
            for dx ,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx,ny = x+dx, y+dy
                if not (0<=nx<n and 0<=ny<m): continue
                if (nx,ny) in dist: continue
                nd = max(d+1, moveTime[nx][ny]+1)   # 每个位置有最早可以到达的时间限制
                heapq.heappush(h, (nd, nx,ny))
        return dist[(n-1,m-1)]
    
    """ 3342. 到达最后一个房间的最少时间 II #medium 相较于上一题, 每次移动的时间为 1,2, 1,2, ...
限制: n 750
优化: 可以用 i+j 的奇偶性简化判断, 见 ling
[ling](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-ii/solutions/2975554/dijkstra-zui-duan-lu-pythonjavacgo-by-en-alms/)
     """
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        n,m = len(moveTime), len(moveTime[0])
        dist = {}
        h = [(0,0,0,0)] # (d, if_double, x,y)
        while h:
            d, f, x,y = heapq.heappop(h)
            if (x,y) in dist: continue
            dist[(x,y)] = d
            for dx ,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx,ny = x+dx, y+dy
                if not (0<=nx<n and 0<=ny<m): continue
                if (nx,ny) in dist: continue
                nd = max(d+f+1, moveTime[nx][ny]+f+1)   # 每个位置有最早可以到达的时间限制
                heapq.heappush(h, (nd, 1-f, nx,ny))
        return dist[(n-1,m-1)]
    
    """ 3343. 统计平衡排列的数目 #hard 对于一个数字字符串, "平衡" 的定义是奇数和偶数位置数字之和相同. 问一个字符串的所有排列中, 平衡排列的个数. 
限制: n 80; 对结果取模
思路1: 考虑相同数字填的位置! #记忆化搜索 #题型
    对于所有数字计数为 cnt
    记 f(i, k, m,n) 表示当前填数字 i (0~9), 奇偶位置的剩余 m/n 个, 它们之和差为 k 时候的平衡排列数量
        考虑 i 从9填到0, 则答案应该是 f(9, 0, m, n). 
        转移方程: 考虑在m中选择q (0~cnt[i]) 填充, 剩余的 cnt[i]-q 填到n个空位, 因此有
            sum_q { C(m,q) * C(n, cnt[i]-q]) * f(i-1, k + i*(q-cnt[i]+q), m-q, n-cnt[i]+q) }
    边界: f(-1, 0, 0, 0) = 1
    from [](https://leetcode.cn/problems/count-number-of-balanced-permutations/solutions/2975518/ji-yi-hua-sou-suo-zu-he-ji-shu-by-ddddok-iy4k/)
思路2: 多重集排列数 + 计数 DP
    定义 f(i, left1, leftS) 表示从9开始, 当前要填i, 第一个多重集还有 left1个空位, 第一个多重集的和还剩余 leftS 时的平衡排列个数
    参见灵神, 深入讲了基于排列的思路. 做了排列数的优化 (不考虑性能的话不用管)
[ling](https://leetcode.cn/problems/count-number-of-balanced-permutations/solutions/1/duo-zhong-ji-pai-lie-shu-ji-shu-dppython-42ky/)
    拓展: 动态规划题单中的「§7.5 多维 DP」和数学题单中的「§2.2 组合计数」
    """
    def countBalancedPermutations(self, num: str) -> int:
        MOD = 10**9 + 7
        n = len(num)
        cnt = Counter(map(int, num))
        @lru_cache(None)
        def f(i, k, m,n):
            if i == -1: return int(k==0 and m==n==0)
            if m<0 or n<0: return 0  # 提前终止
            res = 0
            for q in range(cnt[i]+1):
                res += math.comb(m, q) * math.comb(n, cnt[i]-q) * f(i-1, k + i*(q-cnt[i]+q), m-q, n-cnt[i]+q)
                res %= MOD
            return res
        return f(9, 0, n//2, n-n//2)

sol = Solution()
result = [
    # sol.isBalanced(num = "24123"),
    # sol.minTimeToReach(moveTime = [[0,4],[4,4]]),
    # sol.minTimeToReach(moveTime = [[0,0,0],[0,0,0]]),

    # sol.minTimeToReach(moveTime = [[0,4],[4,4]]),
    # sol.minTimeToReach(moveTime = [[0,0,0,0],[0,0,0,0]]),
    # sol.minTimeToReach([[0,58],[27,69]]),
    sol.countBalancedPermutations(num = "123"),
    sol.countBalancedPermutations(num = "112"),
    sol.countBalancedPermutations(num = "12345"),
]
for r in result:
    print(r)
