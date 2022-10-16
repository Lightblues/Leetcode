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
https://leetcode.cn/contest/weekly-contest-314

感觉这一期挺精彩, 四道题都有一定的思维, AK花了50min. T3做的时间更长一些, 或许有更为简洁的思路; T4的DP也比较巧妙, 自己看k=3的情况误打误撞推出来了.

@2022 """
class Solution:
    """ 2432. 处理用时最长的那个任务的员工 """
    def hardestWorker(self, n: int, logs: List[List[int]]) -> int:
        time = 0
        longest = 0
        ret = 0
        for u,t in logs:
            tt = t - time; time = t
            if tt>longest or tt==longest and u<ret:
                longest = tt
                ret = u
        return ret
    
    """ 2433. 找出前缀异或的原始数组 #medium 给定顺序 #异或 的结果, 求原始数组 """
    def findArray(self, pref: List[int]) -> List[int]:
        ret = [pref[0]]
        for i in range(1, len(pref)):
            ret.append(pref[i]^pref[i-1])
        return ret
    
    """ 2434. 使用机器人打印字典序最小的字符串 #medium #题型 给定一个字符串s, 在顺序处理s 的过程中 (输出, 或者存入栈), 可以使用一种辅助的栈t (存入字符之后只能倒序输出). 
问能够输出的最小字典序的字符串. 限制: n 1e5
思路0: 原本尝试用栈, 发现没有那么简单.
注意: 例如 abac, acab 其输出的结果都是 aabc.
思路1: #模拟 每次从剩余字符中取出所有最小字符. 灵神总结是 #贪心+ #栈
    这样, 放入栈中的字符的出栈顺序就固定了, 但剩余字符还可以执行的操作除了输出还可以入栈.
    因此, 每次从剩余的s中找到其中的最小字符 mn, 根据其 ridx 分割, 左边将其他字符压入栈, 右边是保留的字符串.
        注意, 次小字符也可能出现在栈顶, 需要将这些符合要求的字符先pop出来.
    具体见下代码.
[灵神](https://leetcode.cn/problems/using-a-robot-to-print-the-lexicographically-smallest-string/solution/tan-xin-zhan-by-endlesscheng-ldds/) 的思路一样, 但简洁许多
"""
    def robotWithString(self, s: str) -> str:
        t = ""
        ret = ""
        while s:
            # 找到剩余字符串 s 中的所有最小 char
            mn = min(s)
            idx = s.rindex(mn)
            # 栈 t 中可能存在比 mn 小的字符, 需要先pop出来
            while t and t[-1]<=mn:
                ret += t[-1]; t = t[:-1]
            # 根据 idx 分割, 左边的字符入栈, 右边的字符保留
            ret += s.count(mn) * mn
            t += "".join([c for c in s[:idx] if c!=mn])
            s = s[idx+1:]
        ret += t[::-1]
        return ''.join(ret)
    def robotWithString(self, s: str) -> str:
        # from 灵神
        ans = []
        cnt = Counter(s)
        min = 0  # 剩余最小字母
        st = []
        for c in s:
            cnt[c] -= 1
            while min < 25 and cnt[ascii_lowercase[min]] == 0:
                min += 1
            st.append(c)
            while st and st[-1] <= ascii_lowercase[min]:
                ans.append(st.pop())
        return ''.join(ans)

    
    """ 2435. 矩阵中和能被 K 整除的路径 #hard #DP 给定一个grid, 求从左上角到右下角的路径数, 使得路径上的和能被 K 整除. 限制: m*n 5e4, k 50. 对结果取mod 1e9+7
思路1: #取模+ #DP
    如何记录路径和? 由于我们需要考虑的仅仅是能否被k整除, 因此只需要记录取模结果即可.
    因此, DP形式可以是 `f[i,j] = [...]` 长为k的数组, 表示到达 (i,j) 时, 路径和取模后的数量.
    转移: 假设 `grid[i,j]==0`, 则有 `f[i,j,g] = f[i-1,j,g] + f[i,j-1,g]`. 
        加上 grid[i,j] 的影响呢? 实际上就是在上面的数组上加了一个偏移量. 
        例如, 假设 k=3 时不考虑 grid[i,j] 时, 值为0,1,2的路径数量分别 [a,b,c], 若 grid[i,j]=2, 则加上之后路径数分别为 [c,a,b].
    复杂度: O(m*n*k)
    参见 [灵神优雅的代码](https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/solution/dong-tai-gui-hua-pythonjavacgo-by-endles-94wq/)
"""
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        mod = 10**9+7       # 注意取模
        m,n = len(grid), len(grid[0])
        # 先对 grid 进行预处理, 将所有的值都转换为取模后的值
        grid = [[i%k for i in row] for row in grid]
        f = [[[0] * k for _ in range(n)] for _ in range(m)]
        # 初始化
        acc = 0
        for i in range(m):
            acc = (acc+grid[i][0]) % k
            f[i][0][acc] = 1
        acc = 0
        for j in range(n):
            acc = (acc+grid[0][j]) % k
            f[0][j][acc] = 1
        # 转移
        for i in range(1,m):
            for j in range(1,n):
                cnt = [f[i-1][j][kk]+f[i][j-1][kk] for kk in range(k)]
                # 加上 grid[i][j] 的偏移量
                bias = grid[i][j]
                new_cnt = [0] * k
                for kk in range(k):
                    new_cnt[(kk+bias)%k] = cnt[kk] % mod
                f[i][j] = new_cnt
        return f[-1][-1][0]
        
        
sol = Solution()
result = [
    # sol.hardestWorker(n = 10, logs = [[0,3],[2,5],[0,9],[1,15]]),
    # sol.findArray(pref = [5,2,0,3,1]),
    sol.numberOfPaths(grid = [[5,2,4],[3,0,5],[0,7,2]], k = 3),
    sol.numberOfPaths(grid = [[0,0]], k = 5),
    sol.numberOfPaths(grid = [[7,3,4,9],[2,3,6,2],[2,3,7,0]], k = 1),
    # sol.robotWithString("zza"),
    # sol.robotWithString("bac"),
    # sol.robotWithString("bdda"),
]
for r in result:
    print(r)
