from typing import *
from math import gcd, prod, inf
from itertools import pairwise

"""
https://leetcode.cn/contest/weekly-contest-452
Easonsi @2026 """


class Solution:
    """ 3566. 等积子集的划分方案 #medium 判断一个数组是否可划分为两个乘积为 target 的数组
限制: n 12; target 1e15; 元素互不相同
思路 1: #枚举 因为数量较少, 直接暴力枚举 (2**12 = 4096)
    复杂度: O(2^n); 空间 O(n) 栈空间
思路 2: #二进制枚举
    优化: 考虑对称性, 最后一个元素 (最高位) 可以默认放到 s2 里面 (也即二进制最高位设置为 0 即可) -- 只需要枚举到 1<<(n-1)-1
    复杂度: O(n 2^n); 空间 O(1)
思路 3: #折半枚举 将数组均匀二分, 考虑子问题!
    考虑前半中, 分成的两组积为 a1, b2; 则要求 a1*a2 = b1*b2; 也即 a1/b1 = a2/b2 --> 检查前半数组划分所能构成的最简分数, 看和后半部分是否有交集!
    前置条件: prod(nums) == target^2
    细节: 可以通过保留 #最简分数 的形式来记录集合 (不建议用浮点数存储因为有误差) -- 这样带来 gcd 操作的代价
    复杂度: O(2^(n/2) * log target), 其中 log 操作是 gcd
https://leetcode.cn/problems/partition-array-into-two-equal-product-subsets/solutions/3690735/er-jin-zhi-mei-ju-pythonjavacgo-by-endle-w78j/
    """
    def checkEqualPartitions(self, nums: List[int], target: int) -> bool:
        n = len(nums)
        def dfs(i: int, s1: int, s2: int) -> bool:
            if i == n: return s1 == s2 == target
            return dfs(i+1, s1*nums[i], s2) or dfs(i+1, s1, s2*nums[i])
        return dfs(0, 1, 1)

    def checkEqualPartitions(self, nums: List[int], target: int) -> bool:
        # 二进制枚举
        n = len(nums)
        for s in range(1, 1<<(n-1)):  # 优化: 考虑对称性
            s1, s2 = 1, 1
            for i, x in enumerate(nums):
                if s >> i  & 1:
                    s1 *= x
                else: s2 *= x
            if s1 == s2 == target: return True
        return False

    def checkEqualPartitions(self, nums: List[int], target: int) -> bool:
        # 折半枚举
        def calc(nums: list[int], target: int) -> set[tuple[int, int]]:
            st = set()
            def dfs(i: int, a: int, b: int) -> None:
                if a > target or b > target: return  # prune
                if i == len(nums):
                    g = gcd(a, b)
                    st.add((a//g, b//g))
                    return
                dfs(i+1, a*nums[i], b)
                dfs(i+1, a, b*nums[i])
            dfs(0,1,1)
            return st
        # fist check
        if prod(nums) != nums**2: return False
        m = len(nums) // 2
        st1 = calc(nums[:m], target)
        st2 = calc(nums[m:], target)
        return len(st1 & st2) > 0

    """ 3567. 子矩阵的最小绝对差. 
对于一个 m*n 的矩阵, 对于所有 k*k 子矩阵, 计算 "最小绝对差" -- 任意不相同元素之差的 abs
限制: n 30; v 1e5
思路 1: #暴力枚举
    复杂度: O((n-k)(m-k)k^2 log(k))
思路 2: 考虑用 定长滑动窗口 + 有序集合 + 懒删除堆，用有序集合维护窗口（子矩阵）元素，用懒删除堆维护相邻不同元素之差。添加删除的时候更新相邻不同元素之差。
    复杂度: O((m-k)nk logk), 但常熟比较大
https://leetcode.cn/problems/minimum-absolute-difference-in-sliding-submatrix/solutions/3690788/bao-li-mei-ju-pythonjavacgo-by-endlessch-ecsp/
    """
    def minAbsDiff(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m,n = len(grid),len(grid[0])
        ans = [[0] * (n-k+1) for _ in range(m-k+1)]
        for i in range(m-k+1):
            for j in range(n-k+1):
                arr = []
                for l in range(k):
                    arr += grid[i+l][j:j+k]
                # arr.sort()
                # res = inf
                # for a,b in pairwise(arr):
                #     if a<b: # 要求元素不相等
                #         res = min(res, b-a)
                # if res != inf: ans[i][j] = res
                # op2: 测下来速度差不多!
                arr = sorted(set(arr))
                if len(arr) > 1:
                    ans[i][j] = min(b-a for a,b in pairwise(arr))
        return ans

    """ 3568. 清理教室的最少移动 
给定一个网格, 从 S 出发要收集所有 L 点, X 是障碍; 初始能量 energy, 到达 R 点恢复所有; 移动一格消耗 1, 到 0 则无法移动. 问最小步数
限制: n 20; energy 50; 最多 10 个L. 无法则返回 -1
思路 1: #BFS 计算 #最短路
    状态: (x,y,e,mask), 其中 e 为当前剩余能量, mask 为当前收集的垃圾状态 (二进制)
    终点: 任意 x/y/e, mask=U 收集完毕
    复杂度: O(n^2 e U), 其中 U=2^L; 状态转移为常数
优化: 记录 (x,y,mask) 状态的最大能量, 若新状态能量更低, 则不加入 q
    -- 避免左右反复移动的无意义探索
    理论复杂度同; 但 7s -> 1.4s
https://leetcode.cn/problems/minimum-moves-to-clean-the-classroom/solutions/3690747/bfs-by-endlesscheng-rpk6/
    """
    def minMoves(self, classroom: List[str], energy: int) -> int:
        m,n = len(classroom),len(classroom[0])
        idx = [[0]*n for _ in range(m)]
        cnt_l = sx = sy = 0
        for i, row in enumerate(classroom):
            for j, ch in enumerate(row):
                if ch == 'L':
                    idx[i][j] = 1<<cnt_l  # 给所有 L 标号 (二进制)
                    cnt_l += 1
                elif ch == "S":
                    sx,sy = i,j
        if cnt_l == 0: return 0
        # 
        mask_full = (1<<cnt_l) - 1
        DIRS = [(0,-1),(0,1),(-1,0),(1,0)]
        vis = [[[[False] * (1<<cnt_l) for _ in range(energy+1)] for _ in range(n)] for _ in range(m)]
        # 双列表（队列）计算 BFS
        ans = 0
        q = [(sx, sy, energy, 0)]
        while q:
            nq = []
            for x,y,e,mask in q:
                # 采用后判断
                if mask == mask_full: return ans
                if e == 0: continue
                for dx,dy in DIRS:
                    nx,ny = x+dx,y+dy
                    if nx<0 or nx>=m or ny<0 or ny>=n or classroom[nx][ny]=="X": continue
                    ne = energy if classroom[nx][ny]=="R" else e-1
                    nmask = mask | idx[nx][ny]
                    if not vis[nx][ny][ne][nmask]:
                        vis[nx][ny][ne][nmask] = True
                        nq.append((nx,ny,ne,nmask))
            ans += 1
            q = nq
        return -1

    def minMoves(self, classroom: List[str], energy: int) -> int:
        m,n = len(classroom),len(classroom[0])
        idx = [[0]*n for _ in range(m)]
        cnt_l = sx = sy = 0
        for i, row in enumerate(classroom):
            for j, ch in enumerate(row):
                if ch == 'L':
                    idx[i][j] = 1<<cnt_l  # 给所有 L 标号 (二进制)
                    cnt_l += 1
                elif ch == "S":
                    sx,sy = i,j
        if cnt_l == 0: return 0
        # 
        mask_full = (1<<cnt_l) - 1
        DIRS = [(0,-1),(0,1),(-1,0),(1,0)]
        maxEnergy = [[[-1] * (1<<cnt_l) for _ in range(n)] for _ in range(m)]
        q = [(sx,sy,energy,0)]
        ans = 0
        while q:
            nq = []
            for x,y,e,mask in q:
                if mask == mask_full: return ans
                if e==0: continue
                for dx,dy in DIRS:
                    nx,ny = x+dx,y+dy
                    if nx<0 or nx>=m or ny<0 or ny>=n or classroom[nx][ny]=="X": continue
                    ne = energy if classroom[nx][ny]=="R" else e-1
                    nmask = mask | idx[nx][ny]
                    if ne > maxEnergy[nx][ny][nmask]:
                        maxEnergy[nx][ny][nmask] = ne
                        nq.append((nx,ny,ne,nmask))
            ans += 1
            q = nq
        return -1


sol = Solution()
result = [
    # sol.checkEqualPartitions(nums = [3,1,6,8,4], target = 24),
    # sol.checkEqualPartitions(nums = [2,5,3,7], target = 15),
    # sol.minAbsDiff(grid = [[1,8],[3,-2]], k = 2),
    # sol.minAbsDiff(grid = [[3,-1]], k = 1),
    # sol.minMoves(classroom = ["S.", "XL"], energy = 2),
    # sol.minMoves(classroom = ["LS", "RL"], energy = 4),
    sol.minMoves(classroom = ["L.S", "RXL"], energy = 3),
]
for r in result:
    print(r)