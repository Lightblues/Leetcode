from typing import *


""" 
https://leetcode.cn/contest/weekly-contest-436

T2 调和级数枚举

Easonsi @2025 """
class Solution:
    """ 3446. 按对角线进行矩阵排序 #medium 对于上三角, 按照对角线方向排序; 对于下三角逆序.
参考: [ling](https://leetcode.cn/problems/sort-matrix-by-diagonals/solutions/3068709/mo-ban-mei-ju-dui-jiao-xian-pythonjavacg-pjxp/)
 """
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        # upper triangle
        for j in range(1,n):  # 包括主对角线
            line = []
            for i in range(n-j):
                line.append(grid[i][j+i])
            line.sort()
            for i in range(n-j):
                grid[i][j+i] = line[i]
        # lower triangle
        for i in range(n):
            line = []
            for j in range(n-i):
                line.append(grid[i+j][j])
            line.sort(reverse=True)
            for j in range(n-i):
                grid[i+j][j] = line[j]
        return grid
    
    """ 3447. 将元素分配给有约束条件的组 #medium 给定一组数字, 对于每个数字x, 找到elements里面最早出现的x的因子.
限制: n 1e5; K 1e5
思路1: #预处理 + #调和级数 枚举
    假设groups里面的数字最大为 mx, 考虑直接从左到右枚举elements
        用 target[j] 表示其第j个元素可以被整除的最左侧因子.
        枚举 x = elements[i], 我们直接将 y = x, 2x, ... 位置的target更新为 i.
    避免重复标记? 初始化 target=-1, 遇到 target[x] != -1 则跳过. (前面已经枚举或者其因子已经被枚举)
    复杂度: 核心是调和级数枚举, 复杂度为 O(n log mx), 其中n为elements的长度
     """
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        mx = max(groups)
        target = [-1]*(mx+1)
        for i,x in enumerate(elements):
            if x>mx or target[x]>=0: continue
            for y in range(x, mx+1, x):
                if target[y] == -1:
                    target[y] = i
        return [target[x] for x in groups]
    
    """ 3448. 统计可以被最后一个数位整除的子字符串数目 #hard 给定一个数字字符串, 问其子串中, 结尾不为0, 且其可以被最后一位整除的子串数量.
限制: n 1e5; 可以有前导0
思路1: #数学 #DP
    推导: 假设s的第i为数字为 si, 
 """
    def countSubstrings(self, s: str) -> int:

    
sol = Solution()
result = [
    # sol.sortMatrix(grid = [[1,7,3],[9,8,2],[4,5,6]]),
    sol.assignElements(groups = [8,4,3,2,4], elements = [4,2]),
]
for r in result:
    print(r)
