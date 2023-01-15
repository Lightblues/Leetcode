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
https://oi-wiki.org/basic/prefix-sum/
[子矩阵元素加 1](https://leetcode.cn/problems/increment-submatrices-by-one/solution/er-wei-chai-fen-by-endlesscheng-mh0h/)


=== 二维
子矩阵元素加 1
0304. 二维区域和检索 - 矩阵不可变 #medium 对于一个不可变的矩阵, 求任意矩形区域的和.
2132. 用邮票贴满网格图 #hard #题型 
    给定一个矩阵, 部分的点无法贴上邮票, 你需要用 (h,w) 的邮票覆盖, 规则是可以重叠 但是不能贴到禁止格上, 也不能超过边界! 判断能否贴满
    利用前缀和矩阵判断是否有禁止格
    利用差分矩阵记录邮票贴的情况


Easonsi @2023 """
class Solution:
    """ 6292. 子矩阵元素加 1 #medium 二维 #查分 矩阵. 每次给定一个矩形区域, 对其内的元素加1, 问每次操作后的矩阵. 限制: n 500, 操作次数 K 1e5
见 [灵神](https://leetcode.cn/problems/increment-submatrices-by-one/solution/er-wei-chai-fen-by-endlesscheng-mh0h/)
思路1: 一维 #差分. 对于每一行求前缀和. 
    复杂度: O(kn + n^2)
思路2: #二维差分
    先理解一下二维 #前缀和. 求二维前缀和的方法: acc[i,j] = acc[i,j-1] + acc[i-1,j] - acc[i-1,j-1] + a[i,j]
    这样容易得到二维差分数组的操作: 需要两个 + 和两个 - (显然相加应该为0)
    复杂度 O(k + n^2)
"""
    def rangeAddQueries(self, n: int, queries: List[List[int]]) -> List[List[int]]:
        # 思路2: #二维差分
        # 二维差分
        diff = [[0]*(n+1) for _ in range(n+1)]
        for r1,c1,r2,c2 in queries:
            diff[r1][c1]+=1
            diff[r1][c2+1]-=1
            diff[r2+1][c1]-=1
            diff[r2+1][c2+1]+=1
        # 用二维前缀和复原
        ret = [[0]*(n) for _ in range(n)]
        ret[0][0] = diff[0][0]
        for i in range(1,n):
            ret[i][0] = ret[i-1][0]+diff[i][0]
            ret[0][i] = ret[0][i-1]+diff[0][i]
        for i in range(1,n):
            for j in range(1,n):
                ret[i][j] = ret[i-1][j]+ret[i][j-1] - ret[i-1][j-1] + diff[i][j]
        return ret
    def rangeAddQueries(self, n: int, queries: List[List[int]]) -> List[List[int]]:
        # 一维差分
        a = [[0]*n for _ in range(n)]
        for r1,c1,r2,c2 in queries:
            for i in range(r1,r2+1):
                a[i][c1]+=1
                if c2+1<n: 
                    a[i][c2+1]-=1
        for i in range(n):
            for j in range(1,n):
                a[i][j] += a[i][j-1]
        return a
    

    """ 2132. 用邮票贴满网格图 #hard #题型 
给定一个矩阵, 部分的点无法贴上邮票, 你需要用 (h,w) 的邮票覆盖, 规则是可以重叠 但是不能贴到禁止格上, 也不能超过边界! 判断能否贴满
思路1: #二维差分
    尝试在 (i,j) 贴邮票, 如何判断给定范围能够贴? 判断范围内是否有禁止点 —— 对于所给的grid计算 #二维前缀和
    然后, 判断是否贴满? 将邮票的贴法用二维差分矩阵记录, 然后还原到原始矩阵, 判断是否有空的位置
"""
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        m,n = len(grid),len(grid[0])
        # 计算二维前缀和: 判断区间内是否有禁止点
        acc = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                acc[i+1][j+1] = acc[i][j+1]+acc[i+1][j]-acc[i][j]+grid[i][j]
        # 尝试在每个空的位置贴邮票
        diff = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                # if grid[i][j]==1: continue
                # 这里 (i2,j2) 直接用了下一个位置
                # i2,j2 = i+stampHeight-1,j+stampWidth-1
                i2 = i+stampHeight
                j2 = j+stampWidth
                # 邮票也不能超过边界
                if i2>m or j2>n: continue
                cnt = acc[i2][j2] -acc[i2][j]-acc[i][j2] +acc[i][j]
                if cnt>0:continue
                diff[i][j]+=1; diff[i2][j]-=1; diff[i][j2]-=1; diff[i2][j2]+=1
        # 还原贴邮票的情况
        stamps = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                stamps[i+1][j+1] = stamps[i][j+1]+stamps[i+1][j]-stamps[i][j]+diff[i][j]
                if grid[i][j]==0 and stamps[i+1][j+1]==0: return False
        return True
    """ from 评论区, hhh 用卷积来做 —— 虽然超时了 """
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        import numpy as np
        from scipy.signal import convolve2d

        h,w=stampHeight,stampWidth
        g=np.array(grid)
        b=np.ones((h,w))
        # x统计以这个点为左上角的矩形能覆盖多少个1，如果为0的位置说明这个矩形能铺上
        x=convolve2d(g,b,fillvalue=1)
        # y统计能覆盖到这个位置的矩形有多少个是铺不下去的，如果为h*w说明这个点没有任何矩形能覆盖得到
        y=convolve2d(x>0,b,mode='valid')
        return not (y==(h*w))[g==0].any()
    
    
    
    
    
""" 0304. 二维区域和检索 - 矩阵不可变 #medium 对于一个不可变的矩阵, 求任意矩形区域的和. 限制: n 20, 查询次数 q 1e5
思路1: #二维前缀和
"""
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m,n = len(matrix),len(matrix[0])
        # 计算前缀和, 带哨兵
        acc = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                acc[i+1][j+1] = acc[i][j+1]+acc[i+1][j]-acc[i][j]+matrix[i][j]
        self.acc = acc

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        acc = self.acc
        return acc[row2+1][col2+1]-acc[row2+1][col1]-acc[row1][col2+1]+acc[row1][col1]


        
sol = Solution()
result = [
#     testClass("""["NumMatrix","sumRegion","sumRegion","sumRegion"]
# [[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],[2,1,4,3],[1,1,2,2],[1,2,2,4]]"""),

    # sol.maxOutput(n = 3, edges = [[0,1],[1,2]], price = [1,1,1]),
    # sol.maxOutput(n = 6, edges = [[0,1],[1,2],[1,3],[3,4],[3,5]], price = [9,8,7,6,10,5]),
    sol.possibleToStamp(grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], stampHeight = 4, stampWidth = 3),
    sol.possibleToStamp(grid = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], stampHeight = 2, stampWidth = 2),
    sol.possibleToStamp([[1,0],[0,0]],2,2),
]
for r in result:
    print(r)
