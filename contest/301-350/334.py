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
https://leetcode.cn/contest/weekly-contest-334
讨论: https://leetcode.cn/circle/discuss/ldt5CI/
Easonsi @2023 """
class Solution:
    """ 6369. 左右元素和的差值 """
    def leftRigthDifference(self, nums: List[int]) -> List[int]:
        left = list(accumulate(nums, initial=0))[:-1]
        right = list(accumulate(nums[::-1], initial=0))[:-1][::-1]
        return [abs(l-r) for l,r in zip(left,right)]
    
    """ 6368. 找出字符串的可整除数组 """
    def divisibilityArray(self, word: str, m: int) -> List[int]:
        n = len(word)
        ans = [0] * n
        x = 0
        for idx,i in enumerate(word):
            x = x*10 + int(i)
            x %= m
            if x==0: ans[idx] = 1
        return ans
    
    """ 6367. 求出最多标记下标 #medium #题型 对于数组中 2[i]<-[j] 的两个元素进行标记, 问最多可以标记的数字数量 
思路1: 排序之后, 前半部分和后半部分 #贪心 匹配
    复杂度: O(n logn) 边界在排序上
思路2: 还可以 #二分
    检查是否可以完成 k对, 可以「看最小的 k 个数和最大的 k 个数能否匹配」
"""
    def maxNumOfMarkedIndices(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        # l = 0
        ans = 0
        m = r = ceil(n/2)
        for i in range(m):
            while r<n and nums[r] < 2*nums[i]:
                r += 1
            if r==n: break
            if nums[r] >= 2*nums[i]:
                ans += 2
                r += 1
        return ans
    
    """ 6366. 在网格图中访问一个格子的最少时间 #hard 从左上到右下. 每个格子都有可以被访问的最早时间, 问到达右下角的最早时间. 限制: 格子数量 1e5; 每个格子的时间 1e5
思路1: 根据当前的最小代价进行 #BFS 记录每一个节点的最短时间 #Dijkstra
    边界: (1,0),(0,1) 两个位置如果都 >1 那么无法到达. 否则, 总是有解的
    假设到达当前位置(i,j)的最小代价为 v, 相邻节点的值为x. 那么递推该节点的代价为
        若 x<=v+1, 则可以直接到达 v+1
        否则, 走其他地方回到(i,j)步数为偶数, 再到达邻居时间需要 x + (1 if (x-v)%2==0 else 0)
    复杂度: 每个节点至多拓展一次, 所以时间复杂度为 O(mn log(mn))
思路2: 还可以 #二分
    关联: 「0778. 水位上升的泳池中游泳」
[灵神](https://leetcode.cn/problems/minimum-time-to-visit-a-cell-in-a-grid/solution/er-fen-da-an-bfspythonjavacgo-by-endless-j10w/)
"""
    def minimumTime(self, grid: List[List[int]]) -> int:
        if grid[0][1]>1 and grid[1][0]>1: return -1
        m,n = len(grid), len(grid[0])
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        ans = [[inf]*n for _ in range(m)]   # 当前的最小代价
        q = [(0,0,0)]   # (v, x,y)
        while q:
            v, x,y = heappop(q)
            # 实际上, 在这里可以直接检查退出! 不需要下面的 return
            # if x == n - 1 and y == m - 1: return v
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not (0<=nx<m and 0<=ny<n): continue
                if grid[nx][ny] <= v+1:
                    nv = v+1
                else:
                    nv = grid[nx][ny] + (1 if (grid[nx][ny]-v)%2==0 else 0)
                if nv < ans[nx][ny]:
                    heappush(q, (nv, nx,ny))
                    ans[nx][ny] = nv
        return ans[-1][-1]
    
sol = Solution()
result = [
    # sol.leftRigthDifference(nums = [10,4,8,3]),
    # sol.divisibilityArray(word = "998244353", m = 3),
    # sol.divisibilityArray(word = "1010", m = 10),
    # sol.maxNumOfMarkedIndices(nums = [3,5,2,4]),
    # sol.maxNumOfMarkedIndices(nums = [9,2,5,4]),
    # sol.maxNumOfMarkedIndices(nums = [7,6,8]),
    sol.minimumTime(grid = [[0,1,3,2],[5,1,2,5],[4,3,8,6]]),
    sol.minimumTime(grid = [[0,2,4],[3,2,1],[1,0,4]]),
]
for r in result:
    print(r)
