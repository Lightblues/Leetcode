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
https://leetcode.cn/contest/weekly-contest-362
https://leetcode.cn/circle/discuss/DihZU2/


Easonsi @2023 """
class Solution:
    """ 2848. 与车相交的点 """
    def numberOfPoints(self, nums: List[List[int]]) -> int:
        points = [0] * 102
        for s,e in nums:
            for i in range(s,e+1):
                points[i] = 1
        return sum(points)
    
    """ 2849. 判断能否在给定时间到达单元格 """
    def isReachableAtTime(self, sx: int, sy: int, fx: int, fy: int, t: int) -> bool:
        dx,dy = abs(sx-fx), abs(sy-fy)
        # NOTE: 一个边界
        if dx==dy==0: return t!=1
        mn = max(dx,dy)
        return t>=mn
    
    """ 2850. 将石头分散到网格图的最少移动次数 #medium #题型
对于 3*3 的网格里面有9个石子, 每次可以移动一个石子到邻居位置. 问得到均匀分布的最小操作次数. 
思路1: #DFS
    对每个状态, 枚举所有可能的移动, 然后递归.
        首先分析复杂度! 注意到, 对于「9个位置放置9个物品的方案数」, 等价于在17个位置中选出8个位置放置隔板, 即 C(17,8) = 24310. 然后每次转移4个方向. 可以!
    关键如何记录状态? 可以用tuple来表示
思路1.1: 反过来, 提前构建距离表
    也可以反过来, 从目标状态, 反过来搜索所有的状态及其代价.
    小羊 https://leetcode.cn/circle/discuss/DihZU2/view/CBMWts/
思路2: 枚举 #全排列
    从转移的角度来考虑, 有若干需要移动的石子, 和目标位置. 
    对于每一个位置pair, 移动有代价, 可以 #全排列 计算 最小代价.
    复杂度: 排列的最大长度为 8, 8! = 40320. 每次计算的代价为 O(n)
思路2.2: #最小费用最大流
    对于每个大于1的格子, 向等于0的格子连边, 容量为1, 费用为距离. 
    答案就是从超级源点到超级汇点的最小费用最大流.
见 [灵神](https://leetcode.cn/problems/minimum-moves-to-spread-stones-over-grid/solutions/2435313/tong-yong-zuo-fa-zui-xiao-fei-yong-zui-d-iuw8/)

关联: 「匹配」问题
*   [1947\. 最大兼容性评分和](https://leetcode.cn/problems/maximum-compatibility-score-sum/)
*   [1349\. 参加考试的最大学生数](https://leetcode.cn/problems/maximum-students-taking-exam/)
*   [LCP 04. 覆盖](https://leetcode.cn/problems/broken-board-dominoes/)
*   [1879\. 两个数组最小的异或值之和](https://leetcode.cn/problems/minimum-xor-sum-of-two-arrays/)
*   [2172\. 数组的最大与和](https://leetcode.cn/problems/maximum-and-sum-of-array/)
    """
    def minimumMoves(self, grid: List[List[int]]) -> int:
        # 用了简化的方法, 但是 TLE
        # 想要可以用 hash/hashlib 来进行去重, 但实际上用str即可! 
        # import hashlib
        # s[hashlib.md5(str(grid).encode()).hexdigest()] = 0
        # s[hash(str(grid))] = 0
        import copy
        s = set()
        s.add(str(grid))
        q = deque([grid])
        acc = 0
        while q:
            # check
            for _ in range(len(q)):
                g = q.popleft()
                if max(map(max, g)) == 1: return acc
                # move
                for x,y in itertools.product(range(3), range(3)):
                    if g[x][y] <= 1: continue
                    for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                        nx,ny = x+dx, y+dy
                        if not (0<=nx<3 and 0<=ny<3): continue
                        # move
                        ng = copy.deepcopy(g)
                        ng[x][y] -= 1
                        ng[nx][ny] += 1
                        # check
                        if str(ng) in s: continue
                        s.add(str(ng))
                        q.append(ng)
            acc += 1
    def minimumMoves(self, grid: List[List[int]]) -> int:
        # 更快的方法, from 小羊 https://leetcode.cn/circle/discuss/DihZU2/view/CBMWts/
        vals = []
        for x in grid:
            vals.extend(x)
        vals = tuple(vals)
        set_ = {vals}
        dq = deque([vals])
        cnt = 0
        while dq:
            for _ in range(len(dq)):
                u = dq.popleft()
                lst_u = list(u)
                # 提前判断最终状态
                if max(lst_u) == 1: return cnt
                for i in range(9):
                    if lst_u[i] > 1:
                        x, y = divmod(i, 3)
                        for dx, dy in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
                            new_x = x + dx
                            new_y = y + dy
                            if 0 <= new_x < 3 and 0 <= new_y < 3:
                                new_i = new_x * 3 + new_y
                                lst_u[i] -= 1
                                lst_u[new_i] += 1
                                tp = tuple(lst_u)
                                if tp not in set_:
                                    set_.add(tp)
                                    dq.append(tp)
                                lst_u[i] += 1
                                lst_u[new_i] -= 1
            cnt += 1
    def minimumMoves(self, grid: List[List[int]]) -> int:
        from_ = []
        to_ = []
        for i,row in enumerate(grid):
            for j,cnt in enumerate(row):
                if cnt>1:
                    from_.extend([(i,j)]*(cnt-1))
                elif cnt==0:
                    to_.append((i,j))
        ans = inf
        for perm in itertools.permutations(from_):
            acc = 0
            for (x1,y1),(x2,y2) in zip(perm, to_):
                acc += abs(x1-x2) + abs(y1-y2)
            ans = min(ans, acc)
        return ans
    
    """ 2851. 字符串转换 #hard #hardhard 给定两个长n的字符串 s,t. 每次操作将s的后缀数组删除并添加到前缀. 问「恰好k次操作变成t」的方案数.
限制: n 1e5, K 1e15. 对结果取模. 
思路1: 
    注意到, 每次操作不改变「循环同构」!
        因此, s和t一定是「循环同构字符串」
        对于s的循环同构字符串中有多少个t, 也即在 s+s 中找有多少个t, 可以用 #KMP 来得到. 记作 c
    我们记 f[i][0/1] 表示经过i次操作之后, 变为t/不变为t 的方案数. (答案就是 f[k][1])
    根据 #DP 思想, 我们有 
        f[i][0] = f[i-1][0] * (c-1) + f[i-1][1] * c
        f[i][1] = f[i-1][0] * (n-c) + f[i-1][1] * (n-c-1)
    我们可以写成矩阵形式. 然后用到 #快速幂. 
见 [灵神](https://leetcode.cn/problems/string-transformation/solutions/2435348/kmp-ju-zhen-kuai-su-mi-you-hua-dp-by-end-vypf/)
关于KMP, 见 [zhihu](https://www.zhihu.com/question/21923021/answer/37475572)

矩阵快速幂
• 70. 爬楼梯
• 509. 斐波那契数
• 1137. 第 N 个泰波那契数
• 1220. 统计元音字母序列的数目
• 552. 学生出勤记录 II
• 790. 多米诺和托米诺平铺
    """
    def numberOfWays(self, s, t, k):
        n = len(s)
        c = self.kmp_search(s + s[:-1], t)
        m = [
            [c - 1, c],
            [n - c, n - 1 - c]
        ]
        m = self.pow(m, k)
        return m[0][s != t]

    # KMP 模板
    def calc_max_match(self, s: str) -> List[int]:
        match = [0] * len(s)
        c = 0
        for i in range(1, len(s)):
            v = s[i]
            while c and s[c] != v:
                c = match[c - 1]
            if s[c] == v:
                c += 1
            match[i] = c
        return match

    # KMP 模板
    # 返回 text 中出现了多少次 pattern（允许 pattern 重叠）
    def kmp_search(self, text: str, pattern: str) -> int:
        match = self.calc_max_match(pattern)
        match_cnt = c = 0
        for i, v in enumerate(text):
            v = text[i]
            while c and pattern[c] != v:
                c = match[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                match_cnt += 1
                c = match[c - 1]
        return match_cnt

    # 矩阵乘法
    def multiply(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        c = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                c[i][j] = (a[i][0] * b[0][j] + a[i][1] * b[1][j]) % (10 ** 9 + 7)
        return c

    # 矩阵快速幂
    def pow(self, a: List[List[int]], n: int) -> List[List[int]]:
        res = [[1, 0], [0, 1]]
        while n:
            if n % 2:
                res = self.multiply(res, a)
            a = self.multiply(a, a)
            n //= 2
        return res

sol = Solution()
result = [
    # sol.numberOfPoints(nums = [[3,6],[1,5],[4,7]]),
    # sol.isReachableAtTime(1,2,1,2,1),
    
    sol.minimumMoves(grid = [[1,1,0],[1,1,1],[1,2,1]]),
    sol.minimumMoves(grid = [[1,3,0],[1,0,0],[1,0,3]]),
]
for r in result:
    print(r)
