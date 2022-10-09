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
https://leetcode.cn/contest/weekly-contest-181


@2022 """
class Solution:
    """ 1389. 按既定顺序创建目标数组 """
    def createTargetArray(self, nums: List[int], index: List[int]) -> List[int]:
        ret = []
        for i,num in zip(index, nums):
            ret.insert(i, num)
        return ret
    
    """ 1390. 四因数 """
    def sumFourDivisors(self, nums: List[int]) -> int:
        def get_divisors(n):
            ret = []
            for i in range(1, int(n**0.5)+1):
                if n % i == 0:
                    ret.append(i)
                    if i != n // i:
                        ret.append(n // i)
            return ret
        ret = 0
        for n in nums:
            divisors = get_divisors(n)
            if len(divisors) == 4:
                ret += sum(divisors)
        return ret
    
    """ 1391. 检查网格中是否存在有效路径 #medium #细节 有两种砖块, 分别连接上下左右四个方向. 给定一个 grid, 问能否根据路径的指向, 从左上角走到右下角
思路0: #模拟 #DFS. 会写得爆炸...
思路1: 根据道路连接关系「建图」! 
    如何描述联通关系? 一种简单的方式是用 #并查集
    复杂度: O(a mn), 其中a为并查集操作.
参见 [官答](https://leetcode.cn/problems/check-if-there-is-a-valid-path-in-a-grid/solution/jian-cha-wang-ge-zhong-shi-fou-cun-zai-you-xiao-lu/)
"""
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        # 定义 从上开始, 顺时针方向分别为 0, 1, 2, 3 (走动的方向)
        directions = [(-1,0), (0,1), (1,0), (0,-1)]
        type2dirs = dict(zip(range(1,7), [(3,1), (0,2), (3,2), (1,2), (0,3), (0,1)]))
        def getNext(type, dir):
            # 类型为 type 的砖块, 从 i 方向出发, 可以走到哪个方向
            if type==1:
                if dir==1: return 1
                elif dir==3: return 3
                else: return -1
            elif type==2:
                if dir==0: return 0
                elif dir==2: return 2
                else: return -1
            elif type==3:
                if dir==1: return 2
                elif dir==0: return 3
                else: return -1
            elif type==4:
                if dir==3: return 2
                elif dir==0: return 1
                else: return -1
            elif type==5:
                if dir==1: return 0
                elif dir==2: return 3
                else: return -1
            elif type==6:
                if dir==3: return 0
                elif dir==2: return 1
                else: return -1
        m,n = len(grid), len(grid[0])
        # 边界
        if m==n==1: return True
        # 可能有环! 加一个cache
        cache = set()
        def dfs(i,j, dir):
            nonlocal cache
            if (i,j,dir) in cache: return False
            cache.add((i,j,dir))
            if i<0 or i>=m or j<0 or j>=n: return False
            dir = getNext(grid[i][j], dir)
            if dir==-1: 
                return False
            if i==m-1 and j==n-1: return True
            dx,dy = directions[dir]
            nx,ny = i+dx, j+dy
            # if nx<0 or nx>=m or ny<0 or ny>=n: return False
            return dfs(nx,ny, dir)
        for dir in type2dirs[grid[0][0]]:
            dx,dy = directions[dir]
            if dfs(dx,dy, dir): return True
        return False

    def hasValidPath(self, grid: List[List[int]]) -> bool:
        # 思路1: 根据道路连接关系「建图」! 
        m, n = len(grid), len(grid[0])
        ds = Solution.DisjointSet(m * n)

        def getId(x, y):
            return x * n + y
        
        def detectL(x, y):
            if y - 1 >= 0 and grid[x][y - 1] in [1, 4, 6]:
                ds.merge(getId(x, y), getId(x, y - 1))
        
        def detectR(x, y):
            if y + 1 < n and grid[x][y + 1] in [1, 3, 5]:
                ds.merge(getId(x, y), getId(x, y + 1))
        
        def detectU(x, y):
            if x - 1 >= 0 and grid[x - 1][y] in [2, 3, 4]:
                ds.merge(getId(x, y), getId(x - 1, y))
        
        def detectD(x, y):
            if x + 1 < m and grid[x + 1][y] in [2, 5, 6]:
                ds.merge(getId(x, y), getId(x + 1, y))

        def handler(x, y):
            if grid[x][y] == 1:
                detectL(x, y)
                detectR(x, y)
            elif grid[x][y] == 2:
                detectU(x, y)
                detectD(x, y)
            elif grid[x][y] == 3:
                detectL(x, y)
                detectD(x, y)
            elif grid[x][y] == 4:
                detectR(x, y)
                detectD(x, y)
            elif grid[x][y] == 5:
                detectL(x, y)
                detectU(x, y)
            else:
                detectR(x, y)
                detectU(x, y)
        
        for i in range(m):
            for j in range(n):
                handler(i, j)
        
        return ds.find(getId(0, 0)) == ds.find(getId(m - 1, n - 1))

    class DisjointSet:
        # 并查集模版
        def __init__(self, n):
            self.f = list(range(n))
        
        def find(self, x):
            if x == self.f[x]:
                return x
            self.f[x] = self.find(self.f[x])
            return self.f[x]
        
        def merge(self, x, y):
            self.f[self.find(x)] = self.find(y)







    """ 1392. 最长快乐前缀 #hard #KMP 或者用字符串hash. 见 [KMP] """
    

    
sol = Solution()
result = [
    # sol.createTargetArray(nums = [1,2,3,4,0], index = [0,1,2,3,0]),
    # sol.sumFourDivisors(nums = [21,21]),
    # sol.hasValidPath(grid = [[1,2,1],[1,2,1]]),
    # sol.hasValidPath(grid = [[1,1,1,1,1,1,3]]),
    # sol.hasValidPath(grid = [[1,1,2]]),
    # sol.hasValidPath(grid = [[2],[2],[2],[2],[2],[2],[6]]),
    # sol.hasValidPath([[4,1],[6,1]]),
    sol.hasValidPath([[4,3,3],[6,5,2]])
]
for r in result:
    print(r)
