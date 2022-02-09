from cmath import rect
from operator import ne
from os import times
from turtle import st
from typing import List
import collections
import math
import bisect
import heapq
from unittest import result

class Solution:
    def longestNiceSubstring(self, s: str) -> str:
        """ 1763. 最长的美好子字符串 easy
当一个字符串 s 包含的每一种字母的大写和小写形式 同时 出现在 s 中，就称这个字符串 s 是 美好 字符串。
给你一个字符串 s ，请你返回 s 最长的 美好子字符串 。如果有多个答案，请你返回 最早 出现的一个。如果不存在美好子字符串，请你返回一个空字符串。

输入：s = "YazaAay"
输出："aAa"
解释："aAa" 是一个美好字符串，因为这个子串中仅含一种字母，其小写形式 'a' 和大写形式 'A' 也同时出现了。
"aAa" 是最长的美好子字符串。

1 <= s.length <= 100
暴力遍历
         """
        def check(s):
            lower = [ch for ch in s if ch.islower()]
            upper = [ch.lower() for ch in s if ch.isupper()]
            return set(lower) == set(upper)
        longest = ""
        for i in range(len(s)):
            for j in range(i+1,len(s)+1): # 注意这里的范围
                if check(s[i:j]) and j-i > len(longest):
                    longest = s[i:j]
        return longest

    """ 2000. 反转单词前缀 easy
输入：word = "abcdefd", ch = "d"
输出："dcbaefd"
解释："d" 第一次出现在下标 3 。 
反转从下标 0 到下标 3（含下标 3）的这段字符，结果字符串是 "dcbaefd" 。
 """
    def reversePrefix(self, word: str, ch: str) -> str:
        index = word.find(ch)
        if index != -1:
            return word[:index+1][::-1] + word[index+1:]
        else:
            return word

    """ 1414. 和为 K 的最少斐波那契数字数目 medium
给你数字 k ，请你返回和为 k 的斐波那契数字的最少数目，其中，每个斐波那契数字都可以被使用多次。

输入：k = 7
输出：2 
解释：斐波那契数字为：1，1，2，3，5，8，13，……
对于 k = 7 ，我们可以得到 2 + 5 = 7 。

显然贪心即可 """
    def findMinFibonacciNumbers(self, k: int) -> int:
        def getFibonacci(n):
            fib = [1,1]
            now = 2
            while now<=n:
                fib.append(now)
                now = fib[-1] + fib[-2]
            return fib
        fib = getFibonacci(k)
        result = 0
        while k != 0:
            a = bisect.bisect(fib, k)
            k -= fib[a-1]
            result += 1
        return result

    """ 1725. 可以形成最大正方形的矩形数目 easy
给一组矩阵, 每个矩阵最大可以切出一个正方形, 求所有矩阵能切出的最大正方形的个数.
输入：rectangles = [[5,8],[3,9],[5,12],[16,5]]
输出：3
解释：能从每个矩形中切出的最大正方形边长分别是 [5,3,5,5] 。
最大正方形的边长为 5 ，可以由 3 个矩形切分得到。
 """
    def countGoodRectangles(self, rectangles: List[List[int]]) -> int:
        result, maxL = 0, 0
        for a,b in rectangles:
            l = min(a,b)
            if l > maxL:
                result = 1
                maxL = l
            elif l == maxL:
                result += 1
        return result
                
    """ 1219. 黄金矿工 medium
找到矩阵中非零路径中累积和最大的

DFS 即可, Copilot 牛逼! 下面的DFS直接帮写好了
 """
    def getMaximumGold(self, grid: List[List[int]]) -> int:
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        m,n = len(grid), len(grid[0])
        def isValid(x,y):
            return 0<=x<m and 0<=y<n
        visited = [[False]*n for _ in range(m)]
        result = 0
        def dfs(x,y, cumsum):
            if not isValid(x,y):
                return
            if visited[x][y] or grid[x][y] == 0:
                return
            visited[x][y] = True
            nonlocal result
            result = max(result, cumsum+grid[x][y])
            for dx,dy in directions:
                dfs(x+dx, y+dy, cumsum+grid[x][y])
            visited[x][y] = False
        for i in range(m):
            for j in range(n):
                dfs(i,j,0)
        return result

    """ 1748. 唯一元素的和 """
    def sumOfUnique(self, nums: List[int]) -> int:
        counter = collections.Counter(nums)
        result = 0
        for num, c in counter.items():
            if c==1:
                result += num
        return result

    """ 1405. 最长快乐字符串
给定三个数字 a,b,c 分别是字符 abc 的数量, 构造最长字符串, 满足其中不包含三个连续的相同子字符串, 例如 aaa

输入：a = 1, b = 1, c = 7
输出："ccaccbcc"
解释："ccbccacc" 也是一种正确答案。
     """
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        def construct(s1, s2):
            """ 用 len(s1)<len(s2) 构造字符串
            策略: 尽可能多利用 s2, 直到 1. s1 用完, s2 在最后补充两个即可; 2. len(s2)==len(s1), 此时交错排列即可 """
            result = ""
            while len(s2)>len(s1) and s1:
                result += s2[:2] + s1[:1]
                s2, s1 = s2[2:], s1[1:]
            while s1:
                result += s2[0] + s1[0]
                s2, s1 = s2[1:], s1[1:]
            if s2:
                result += s2[:2]
            return result
        """ 策略:
        先对于三个数字排序, 假设排好序为 n1,n2,n3. 
        1. 当 n1+n2<n3 时, 把前两种字符当作一种即可;
        2. 当 n1+n2>n3 时, 注意此时必然可构造全长 (n1+n2+n3) 字符串, 先尽量基于前两种字符构造, 然后插入数量最多的那种字符. 
        注意到, 当 n2 > 2*n1 时, 利用前两种字符构造时次多字符会有剩余, 因此将剩余的次多字符放在前面 construct(c[1]*c[0], b[1]*(b[0]-countb)+sab)  """
        a,b,c = sorted([(a,'a'), (b,'b'), (c,'c')])
        if a[0]+b[0] < c[0]:
            return construct(a[1]*a[0]+b[1]*b[0], c[1]*c[0])
        else:
            sab = construct(a[1]*a[0], b[1]*b[0])
            countb = sab.count(b[1])
            return construct(c[1]*c[0], b[1]*(b[0]-countb)+sab)

    """ 1001. 网格照明 hard
大小为 n x n 的网格 grid, lamps 给定了一组灯, lamps[i] = [rowi, coli] 可以照亮 行、列、两条对角线
再给一组查询坐标 queries[j] = [rowj, colj], 每次查询返回该点是否被照亮, 并且查询后关闭该点为中心的 3*3 九个坐标上的灯

输入：n = 5, lamps = [[0,0],[0,4]], queries = [[0,4],[0,1],[1,4]]
输出：[1,1,0]

思路: 用四个字典记录 行、列、两条对角线 上的亮灯情况
 """
    def gridIllumination(self, n: int, lamps: List[List[int]], queries: List[List[int]]) -> List[int]:
        lightX = collections.defaultdict(set)
        lightY = collections.defaultdict(set)
        lightD1 = collections.defaultdict(set)
        lightD2 = collections.defaultdict(set)
        def addLight(x,y):
            lightX[x].add(y)
            lightY[y].add(x)
            lightD1[x-y].add(x)
            lightD2[x+y].add(x)
        def checkLight(x,y):
            if lightX[x] or lightY[y] or lightD1[x-y] or lightD2[x+y]:
                return 1
            return 0
        def removeSingleLight(x,y):
            if y in lightX[x]:
                lightX[x].remove(y)
            if x in lightY[y]:
                lightY[y].remove(x)
            if x in lightD1[x-y]:
                lightD1[x-y].remove(x)
            if x in lightD2[x+y]:
                lightD2[x+y].remove(x)
        def removeLight(x,y):
            for xx in range(x-1,x+2):
                for yy in range(y-1,y+2):
                    if 0<=xx<n and 0<=yy<n:
                        removeSingleLight(xx,yy)
        for x,y in lamps:
            addLight(x,y)
        result = []
        for x,y in queries:
            result.append(checkLight(x,y))
            removeLight(x,y)
        return result

    """ 2006. 差的绝对值为 K 的数对数目 """
    def countKDifference(self, nums: List[int], k: int) -> int:
        result = 0
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if abs(nums[i]-nums[j]) == k:
                    result += 1
        return result


sol = Solution()
rels = [
    # sol.longestNiceSubstring(s = "dDzeE"),
    # sol.longestNiceSubstring("Bb"),
    # sol.findMinFibonacciNumbers(19),
    # sol.getMaximumGold(grid = [[0,6,0],[5,8,7],[0,9,0]]),
    # sol.longestDiverseString(a = 1, b = 1, c = 7),
    # sol.longestDiverseString(a = 2, b = 2, c = 1),
    sol.gridIllumination(n = 5, lamps = [[0,0],[0,4]], queries = [[0,4],[0,1],[1,4]]),
]
for r in rels:
    print(r)


