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
https://leetcode.cn/contest/weekly-contest-340
Easonsi @2023 """
class Solution:
    """ 6361. 对角线上的质数 两个对角线都要 """
    def diagonalPrime(self, nums: List[List[int]]) -> int:
        n = len(nums)
        def isPrime(n):
            if n<2: return False
            for i in range(2, int(n**0.5)+1):
                if n%i==0: return False
            return True
        ans = 0
        for i in range(n):
            x = nums[i][i]
            if x>ans and isPrime(x): ans = x
            x = nums[i][n-i-1]
            if x>ans and isPrime(x): ans = x
        return ans
    
    """ 6360. 等值距离和
假设相同数字分别出现在位置 [1,3,4]; 对于位置1来说, 它的距离和是5; 转移到位置3, 减去了两个2, 加上了一个2, 所以距离和是3; 转移到位置4, 减去一个1, 加上两个1, 距离和是4
也即, 转移到第i个位置, 距离和的变化为 [-(n-i)+i] * dist(i-1,i)
     """
    def distance(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [0] * n
        num2idxs = defaultdict(list)
        for i,x in enumerate(nums):
            num2idxs[x].append(i)
        for x,idxs in num2idxs.items():
            idxs.sort()
            m = len(idxs)
            dist = sum(idxs[j]-idxs[0] for j in range(1,m))
            ans[idxs[0]] = dist
            for i in range(1,m):
                dist += (2*i-m) * (idxs[i]-idxs[i-1])
                ans[idxs[i]] = dist
        return ans
    
    """ 6359. 最小化数对的最大差值 #medium 要从数组中找到p个下标对, 使得对应元素差值的最大值最小. 限制: n 1e5 
思路1: 排序后 #二分
    这个差值的范围 [0, max(nums)-min(nums)]
    排序后, 可以在 O(n) 时间内检查差值x是否可以
    """
    def minimizeMax(self, nums: List[int], p: int) -> int:
        nums.sort()
        n = len(nums)
        def check(x):
            acc = 0
            pre = -1
            for i,a in enumerate(nums):
                if pre!=i-1 and a-nums[i-1]<=x: 
                    pre = i
                    acc += 1
                if acc>=p: return True
            return False
        l,r = 0, nums[-1]-nums[0]
        ans = r
        while l<=r:
            m = (l+r)//2
            if check(m):
                ans = m
                r = m-1
            else:
                l = m+1
        return ans
    
    """ 6353. 网格图中最少访问的格子数 #hard 要从左上走到右下, 每次可以往下/右移动最多grid[i,j]步, 问最少跳转次数. 
限制: mn 1e5
思路1: #UCS 注意记录已访问
     """
    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]
        q = [(1,0,0)]   # (dist, x,y)
        visited[0][0] = True
        while q:
            dist, x, y = heapq.heappop(q)
            if x==m-1 and y==n-1: return dist
            # if visited[x][y]: continue
            visited[x][y] = True
            for dx,dy in [(0,1),(1,0)]:
                for i in range(1, grid[x][y]+1):
                    nx, ny = x+dx*i, y+dy*i
                    if not (0<=nx<m and 0<=ny<n): break
                    if nx==m-1 and ny==n-1: return dist+1
                    if visited[nx][ny]: continue
                    visited[nx][ny] = True
                    heapq.heappush(q, (dist+1, nx, ny))
        return -1


sol = Solution()
result = [
    # sol.diagonalPrime(nums = [[1,2,3],[5,17,7],[9,11,10]]),
    # sol.distance(nums = [1,3,1,1,2]),
    # sol.minimizeMax(nums = [10,1,2,7,1,3], p = 2),
    sol.minimumVisitedCells(grid = [[3,4,2,1],[4,2,3,1],[2,1,0,0],[2,4,0,0]]),
    sol.minimumVisitedCells(grid = [[3,4,2,1],[4,2,1,1],[2,1,1,0],[3,4,1,0]]),
]
for r in result:
    print(r)
