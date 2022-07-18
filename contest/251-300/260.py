from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/weekly-contest-260
@20220313 补 """
class Solution:
    """ 2016. 增量元素之间的最大差值 """
    def maximumDifference(self, nums: List[int]) -> int:
        min_now = float('inf')
        res = -1
        for num in nums:
            if num > min_now:
                res = max(res, num - min_now)
            min_now = min(min_now, num)
        return res

    """ 2017. 网格游戏
给定一个 2 x n 的网格, 每个格子有一些分数; 两人只能向右或向下从左上角走到右下角. 第一个人的目标是让第二个人剩余可以吃到的分数最小, 求最小分数.

输入：grid = [[2,5,4],[1,5,1]]
输出：4
解释：第一个机器人的最佳路径如红色所示，第二个机器人的最佳路径如蓝色所示。
第一个机器人访问过的单元格将会重置为 0 。
第二个机器人将会收集到 0 + 0 + 4 + 0 = 4 个点。

分析边界
首先分别计算上下两行从右往左和从左往右的累计和, 在前后加两个哨兵简化判断. 因此 up,down 的长度为 n+1
然后, 假设第一个人从第i个位置往下走(从1开始), 则第二人可以得到的分数为 上半部分的 i+1,...,n, 或者下半部分的 1,...,i-1
对应到这里的两个累计和, 分别是 up[i+1], down[i]. 因此更新 `res = min(res, max(up[i+1], down[i]))`
显然遍历范围为 `range(0, n)`
 """
    def gridGame(self, grid: List[List[int]]) -> int:
        n = len(grid[0])
        grid[0][0] = 0
        grid[1][-1] = 0
        # 累计, 利用两个哨兵简化判断
        down, up = [0] * (n+1), [0] * (n+1)
        for i in range(n):
            down[i+1] = grid[1][i] + down[i]
            up[n-i-1] = grid[0][n-i-1] + up[n-i]
        # 需要判断对应情况
        """ 
        假设第一个人从第i个位置往下走(从1开始), 则第二人可以得到的分数为 上半部分的 i+1,...,n, 或者下半部分的 1,...,i-1
        对应到这里的两个累计和, 分别是 up[i+1], down[i]. 因此更新 `res = min(res, max(up[i+1], down[i]))`
        显然遍历范围为 `range(0, n)`
         """
        res = float('inf')
        for i in range(0, n):
            res = min(res, max(up[i+1], down[i]))
        return res


    """ 2018. 判断单词是否能放入填字游戏内
给定一个网格, 三种情况: ' ' 表示为空, '#' 表示无法仿制, 还可能已经填入字母.
要求判断一个单词是否能放入填字游戏内. 条件: 1. 方向 上下左右都可(可以从右往左); 2. 边界上不能为空或其他字母, 也即只能是 '#' 或者网格的边界; 3. 字母匹配.

输入：board = [["#", " ", "#"], [" ", " ", "#"], ["#", "c", " "]], word = "abc"
输出：true
解释：单词 "abc" 可以如上图放置（从上往下）。

重点: 条件和边界判断
下面自己的实现比较乱, 定义了一系列的函数, 贵在比较清楚; 
然后又抄了 [here](https://leetcode-cn.com/problems/check-if-word-can-be-placed-in-crossword/solution/mei-ju-liang-ge-zhi-jian-de-zi-fu-by-end-pjq1/) 的解法, 思维难度上大了些.
"""
    def placeWordInCrossword0(self, board: List[List[str]], word: str) -> bool:
        d2direction = {
            0: [0, 1],
            1: [1, 0],
        }
        m,n = len(board), len(board[0])
        l = len(word)
        
        def test_str(s, word):
            for ch1, ch2 in zip(s, word):
                if ch1 == " " or ch1 == ch2:
                    continue
                else:
                    return False
            return True
        def test(i,j, direct):
            # 边界满足的情况下, 检查从(i,j)开始, 向direct方向是否可放置word
            # direct 0/1 表示两个方向
            direction = d2direction[direct]
            s = ""
            for k in range(l):
                s += board[i][j]
                i,j = i+direction[0], j+direction[1]
            if test_str(s, word) or test_str(s[::-1], word):
                return True
            return False
        
        def test_margin(i,j, direct):
            # 判断从 (i,j) 开始放, direct方向, 检查边界是否满足条件
            if direct==0:
                if j+l>n:
                    return False
                return j+l==n or board[i][j+l]=='#'
            else:
                if i+l>m:
                    return False
                return i+l==m or board[i+l][j]=='#'

        for i in range(0, m):
            for j in range(0, n):
                if i==0:
                    if test_margin(i,j, 1):
                        if test(i,j, 1):
                            return True
                if j==0:
                    if test_margin(i,j, 0):
                        if test(i,j, 0):
                            return True
                if board[i][j]=='#':
                    for direct in [0, 1]:
                        di,dj = d2direction[direct]
                        ni,nj = i+di, j+dj
                        if test_margin(ni,nj, direct):
                            if test(ni,nj, direct):
                                return True
        return False

    # https://leetcode-cn.com/problems/check-if-word-can-be-placed-in-crossword/solution/mei-ju-liang-ge-zhi-jian-de-zi-fu-by-end-pjq1/
    def placeWordInCrossword(self, board: List[List[str]], word: str) -> bool:
        m,n, k = len(board), len(board[0]), len(word)
        for row in board:
            # 遍历行
            """ 注意, 在go中range下修改 j 的值是会影响循环变量的, 而Python中则不会!! 因此, 必须先定义变量 j """
            # for j in range(n):
            j = 0
            while j < n:
                # 遍历并匹配两个 # 之间的字符
                if row[j]=='#':
                    j+=1
                    continue
                j0, ok1, ok2 = j, True, True # j0 是开始尝试匹配的位置
                # 注意这里的 j 就是外层循环的 j，因此整体复杂度是线性的
                while j<n and row[j]!="#": # 这里遍历的 j 是下一个 # 或者边界位置
                    # 分别正向和反向判断
                    if j-j0>=k or row[j]!=" " and row[j]!=word[j-j0]:
                        ok1 = False
                    if j-j0>=k or row[j]!=" " and row[j]!=word[k-1-j+j0]:
                        ok2 = False
                    j += 1
                if (ok1 or ok2) and j-j0==k: # j-j0==k 说明长度是匹配的
                    return True
                # j += 1
        for j in range(n):
            i = 0
            while i<m:
            # for i in range(m):
                if board[i][j]=='#':
                    i+=1
                    continue
                i0, ok1, ok2 = i, True, True
                while i<m and board[i][j]!="#":
                    if i-i0>=k or board[i][j]!=" " and board[i][j]!=word[i-i0]:
                        ok1 = False
                    if i-i0>=k or board[i][j]!=" " and board[i][j]!=word[k-1-i+i0]:
                        ok2 = False
                    i += 1
                if (ok1 or ok2) and i-i0==k:
                    return True
                # i += 1
        return False


    """ 2019. 解出数学表达式的学生分数
给一个只有 +* 运算和 0~9 数字的表达式, 对于不同的答案赋予分数. 1. 正确为5, 2. 因为运算顺序导致的错误, 分数为2, 3. 其他0分.
因此, 核心问题是搜索所有运算顺序可能给出的结果.

输入：s = "7+3*1*2", answers = [20,13,42]
输出：7
解释：如上图所示，正确答案为 13 ，因此有一位学生得分为 5 分：[20,13,42] 。
一位学生可能通过错误的运算顺序得到结果 20 ：7+3=10，10*1=10，10*2=20 。所以这位学生得分为 2 分：[20,13,42] 。
所有学生得分分别为：[2,5,0] 。所有得分之和为 2+5+0=7 。

思路一: 暴力递归
结合 lru_cache 实现. 由于这里的所有数字和运算符都是一个字符的, 解析起来非常方便 (表达式长度一定为奇数).

注意, 题目中给出了限制: 以及0 <= answers[i] <= 1000 (正确答案在1000以下), 因此不在此范围内的数字可以忽略 —— 降低复杂度.
测试了一下, 在下面的遍历过程中, 对于表达式 "4+8*8+8+8*8+4*4+8*4+8*8+8*8+8" 若不进行过滤, 则不同答案的数量可以达到 `86301`, 过滤后最多只有 `141`
 """
    def scoreOfStudents(self, s: str, answers: List[int]) -> int:
        filter = False

        # 得到所有可能的答案
        from functools import lru_cache
        @lru_cache(None)
        def recc(s):
            if len(s) == 1:
                return set([int(s)])
            anss = set()
            for i in range(1, len(s), 2):
                s1, cal, s2 = s[:i], s[i], s[i+1:]
                if cal == '+':
                    for a in recc(s1):
                        for b in recc(s2):
                            if filter:
                            # 注意, 题目中给出了限制正确答案在100以下, 以及0 <= answers[i] <= 1000, 因此不在此范围内的数字可以忽略 —— 降低复杂度.
                                if a+b<=1000:
                                    anss.add(a+b)
                            else: 
                                anss.add(a+b)
                elif cal == '*':
                    for a in recc(s1):
                        for b in recc(s2):
                            if filter:
                                if a*b<=1000:
                                    anss.add(a*b)
                            else:
                                anss.add(a*b)
            print(s, len(anss))
            return anss
        poss_answers = recc(s)
        ans2score = collections.defaultdict(int)
        for a in poss_answers:
            ans2score[a] = 2
        ans2score[eval(s)] = 5

        return sum(ans2score[a] for a in answers)


sol = Solution()
result = [
    # sol.maximumDifference(nums = [9,4,3,2]),
    # sol.maximumDifference(nums = [3,6,10,1,2,20]),

    # sol.gridGame(grid = [[3,3,1],[8,5,2]]),
    # sol.gridGame([[2,5,4],[1,5,1]]),

    sol.placeWordInCrossword(board = [["#", " ", "#"], [" ", " ", "#"], ["#", "c", " "]], word = "abc"), # True
    sol.placeWordInCrossword([[" ","#","a"],[" ","#", "c"],[" ","#","a"]], "ac"), # False
    sol.placeWordInCrossword([["#"," ","#"],["#"," ","#"],["#"," ","c"]], "ca"), # True
    sol.placeWordInCrossword([["x","g","q","p","j"," ","e","l","i","v","u","x"," ","#","i"],["n","v","q"," "," ","c","q","l","w","v","b","m","p","a","y"],["q","x","z","y","d","s","#","v","w","y"," ","m","l","#","r"]], "xgqpjlelivuxt")

    # sol.scoreOfStudents(s = "6+0*1", answers = [12,9,6,4,8,6]), # 10
    # sol.scoreOfStudents("4+8*8+8+8*8+4*4+8*4+8*8+8*8+8", [812,324,843,924,496,940,856,324,624,668,588,372,928,324,146,684,324,608,436,187,708,])
]
for r in result:
    print(r)

""" 需要注意, go和Python 中, **在循环内部对于循环变量修改是不同的**, Python中修改不会影响结果! 而go中则是可以进行赋值的. """
def test_for():
    for i in range(10):
        print(i)
        i += 1