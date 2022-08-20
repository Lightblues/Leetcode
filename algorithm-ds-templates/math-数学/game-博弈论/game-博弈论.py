import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

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

== hardhard
0913. 猫和老鼠 #hard
    给定一张图, 老鼠和猫分别从节点 1和2 出发, 老鼠到目标是到达洞0, 猫的目标是抓住老鼠. 给定初始状态, 求在双方都是最优解的情况下, 哪一方获胜/平局.
1728. 猫和老鼠 II #hard
    和 0913 类似的设定. 不过图换成了更为现实的带有墙的grid, 以及猫和老鼠每一次都可以选择走 1~limit 步.
@2022 """
class Solution:
    """ 0913. 猫和老鼠 #hard
- 给定一张图, 老鼠和猫分别从节点 1和2 出发, 老鼠到的目标 0 则获胜 (猫不能到达0). 给定初始状态, 求在双方都是最优解的情况下, 哪一方获胜.
    - 注意, 可能出现平局的情况! 分别用 1/2/0 表示老鼠/猫获胜/平均.
    - 复杂度: 图的节点数最大 50.
- [here](https://leetcode.cn/problems/cat-and-mouse/solution/mao-he-lao-shu-by-leetcode-solution-444x/)
- 思路0: 自顶向下 DP
    - 状态: `dp[mouse][cat][turns]` 表示猫和老鼠所在的节点以及当前轮次.
    - 终止条件: 1) 老鼠到达终点或被抓到; 2) 关键是如何判断平局? 注意到有时必须遍历所有的相邻节点才能得到答案, 那么两个相邻节点之间就可能发生死锁!
    - 注意到, 这里的所有节点状态为 2n(n-1), 猫和老鼠可以到达的点乘积 * 该轮轮到老鼠/猫移动. 在每个 agent 都是理性的情况下, 若出现重复访问节点则说明平局.
    - 然而, 复杂度相当高! DP数组的复杂度为 $n^4$, 而对每一个状态计算状态值 `getNextResult` 的复杂度为 n, 因此总体复杂度为 $n^5$, 即使 $n=50$ 也是超时.
- 思路1: #拓扑排序
    - 上一种思路中, 判断平局需要迭代到 $n^2$ 复杂度. 为了避免重复访问节点, 相较于「自顶向下」我们可以「自底向上」进行遍历 (实际上就是拓扑排序!).
    - 具体而言, 这里一共只有 n^2 个节点, 我们通过枚举所有的终止状态, 然后从该状态反推. 对于上一个节点:
        - 可以判断胜利的条件: 对于当前行动体 a 的获胜条件: 当前为a的回合并且可以走到一个a的必胜节点
        - 否则: 无法判断, 继续往下查找. 为了避免重复访问, 我们记录每一个节点的度数, 每遇到这种情况就 -1.
            - 若一直到度数=0还不行, 则说明, a无论选择所有行动都无法获胜, a必败 (注意不是平局);
            - 对于最后剩余无法判断的节点, 平局 (因此初始化所有节点为平局).
    - 在主函数中, 我们维护一个 **queue**, 存放所有确定结局的节点. 遍历过程中, 1) 对于一个确定结局的节点, 将其加入 queue; 2) 否则, 度数 -1.
    - 分析上述流程, 其实就是 #拓扑排序.
    - 总有 n^2 个节点, 每个节点最多访问 n 次, 因此是 O(n^3)

https://leetcode.cn/problems/cat-and-mouse/
输入：graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]
输出：0
"""
    def catMouseGame_0(self, graph: List[List[int]]) -> int:
        DRAW = 0
        MOUSE_WIN = 1
        CAT_WIN = 2
        
        n = len(graph)
        dp = [[[-1] * (2 * n * (n - 1)) for _ in range(n)] for _ in range(n)]

        def getResult(mouse: int, cat: int, turns: int) -> int:
            # 终止条件: 迭代轮次超过了状态数量, 还有胜负, 说明平局
            if turns == 2 * n * (n - 1):
                return DRAW
            
            # 判断是否重复访问节点
            res = dp[mouse][cat][turns]
            if res != -1:
                return res
            
            # 对当前节点的胜负进行判断
            if mouse == 0:
                res = MOUSE_WIN
            elif cat == mouse:
                res = CAT_WIN
            else:
                res = getNextResult(mouse, cat, turns)
            
            # 更新 DP (所有节点) 值
            dp[mouse][cat][turns] = res
            return res

        def getNextResult(mouse: int, cat: int, turns: int) -> int:
            """ 遍历该节点的所有相邻节点, 判断胜负 """
            curMove = mouse if turns % 2 == 0 else cat
            # 1) 若无法达成平均或获胜, 说明必败
            defaultRes = MOUSE_WIN if curMove != mouse else CAT_WIN
            res = defaultRes
            for next in graph[curMove]:
                """ 遍历所有可能的点 """
                if curMove == cat and next == 0:
                    # 猫不能到 0
                    continue
                nextMouse = next if curMove == mouse else mouse
                nextCat = next if curMove == cat else cat
                # 递归
                nextRes = getResult(nextMouse, nextCat, turns + 1)
                if nextRes != defaultRes:
                    res = nextRes
                    # 2) 若达成和局, 则继续遍历下一个; 若行动方获胜, 则可知必胜
                    if res != DRAW:
                        break
            return res

        return getResult(1, 2, 0)


    def catMouseGame(self, graph: List[List[int]]) -> int:
        MOUSE_TURN = 0
        CAT_TURN = 1

        DRAW = 0
        MOUSE_WIN = 1
        CAT_WIN = 2

        n = len(graph)
        # 一个节点由 (idx_mouse, idx_cat, turn) 组成, 其中 turn=0/1 分别表示老鼠/猫的回合
        degrees = [[[0, 0] for _ in range(n)] for _ in range(n)]    # 记录每个节点的度数, 两个数字分别表示老鼠和猫
        results = [[[0, 0] for _ in range(n)] for _ in range(n)]    # 记录每个节点的结果. 注意这里初始化为 0, 恰好为 DRAW, 但其实意味着「状态不确定」
        # 初始化节点度数
        for i in range(n):
            for j in range(1, n):
                degrees[i][j][MOUSE_TURN] = len(graph[i])
                degrees[i][j][CAT_TURN] = len(graph[j])
        # 因为猫不能到0点, 相邻节点的度数 -1
        for y in graph[0]:
            for i in range(n):
                degrees[i][y][CAT_TURN] -= 1

        # 初始化结果: 「自底向上」搜索
        q = collections.deque()
        for j in range(1, n):
            results[0][j][MOUSE_TURN] = MOUSE_WIN
            results[0][j][CAT_TURN] = MOUSE_WIN
            q.append((0, j, MOUSE_TURN))
            q.append((0, j, CAT_TURN))
        for i in range(1, n):
            results[i][i][MOUSE_TURN] = CAT_WIN
            results[i][i][CAT_TURN] = CAT_WIN
            q.append((i, i, MOUSE_TURN))
            q.append((i, i, CAT_TURN))

        while q:
            mouse, cat, turn = q.popleft()
            # 注意到, q 中节点都是已知结局的了!
            result = results[mouse][cat][turn]
            if turn == MOUSE_TURN:
                prevStates = [(mouse, prev, CAT_TURN) for prev in graph[cat]]
            else:
                prevStates = [(prev, cat, MOUSE_TURN) for prev in graph[mouse]]
            for prevMouse, prevCat, prevTurn in prevStates:
                if prevCat == 0:
                    continue
                # 若节点状态 != 0, 说明已经可以知道结果了
                if results[prevMouse][prevCat][prevTurn] == DRAW:
                    # 1) 对于 a 的获胜条件:  当前为a的回合并且可以走到一个a的必胜节点;
                    canWin = result == MOUSE_WIN and prevTurn == MOUSE_TURN or result == CAT_WIN and prevTurn == CAT_TURN
                    if canWin:
                        results[prevMouse][prevCat][prevTurn] = result
                        q.append((prevMouse, prevCat, prevTurn))
                    else:
                        # 对于不能判断是否可获胜的节点, 记录访问的次数
                        degrees[prevMouse][prevCat][prevTurn] -= 1
                        # 2) 对于 a 而言, 若其所有自节点都无法确保获胜, 则该节点是 b 的必胜节点
                        if degrees[prevMouse][prevCat][prevTurn] == 0:
                            results[prevMouse][prevCat][prevTurn] = CAT_WIN if prevTurn == MOUSE_TURN else MOUSE_WIN
                            q.append((prevMouse, prevCat, prevTurn))
                        # 3) 注意, 没有访问到的节点才可能是平局
        return results[1][2][MOUSE_TURN]


    """ 1728. 猫和老鼠 II #hard
- 和 0913 类似的设定. 不过图换成了更为现实的带有墙的grid, 以及猫和老鼠每一次都可以选择走 1~limit 步.
    - 另外给出限制: 如果老鼠不能在 1000 次操作以内到达食物，那么猫获胜. (实际上不用也没问题, 因为状态空间比较小不会出现 (平局情况下) 经过这么多步不还没到达稳态的情况.)
    - 因此, 这题的返回就是 T/F 表示是否为老鼠获胜.
    - 复杂度: 网格长宽 8*8, 1 <= catJump, mouseJump <= 8.
- 思路: 还是按照之前的思路, 反向搜索, #拓扑排序
    - 这里定义了状态结构 `namedtuple('State', ['mouse', 'cat', 'turn'])` 前两个 (x,y) 表示两类agent的位置, 0/1 的turn 表示当前是谁的行动回合.
    - 相较于 0913 这里需要构造节点之间的转移关系 (图).
    - 另外, 反向拓扑排序的时候需要注意, 记录的节点度数为出度; 对应了在反向搜索的过程中, 如果不满足条件则 degree额-1.
- 技巧: 监视某些值, 在 debug状态打断点观察. 例如, 关心一个字典中某一个 key 的值变化, 可以把这个数值存到一个变量中, 打一个断点. 如, `if prevNode in x` 行判断是否需要监视, 下一行 `print(x[prevNode])` 上加断点.
"""
    def canMouseWin(self, grid: List[str], catJump: int, mouseJump: int) -> bool:
        """  """
        MOUSE_TURN, CAT_TURN = 0, 1
        State = collections.namedtuple('State', ['mouse', 'cat', 'turn'])
        m,n = len(grid), len(grid[0])
        
        def getPositions():
            res = [None] * 3
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 'C':
                        res[1] = (i, j)
                    elif grid[i][j] == 'M':
                        res[0] = (i, j)
                    elif grid[i][j] == 'F':
                        res[2] = (i, j)
            return res
        
        PosMouse, PosCat, PosFood = getPositions()
        
        def getPossiblePos(pos, turn):
            # x,y = pos
            limit = mouseJump if turn == MOUSE_TURN else catJump
            res = set((pos,)) # 注意可能重复
            for dx,dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                x,y = pos
                count = 0
                while 0 <= x+dx < m and 0 <= y+dy < n and grid[x+dx][y+dy] != '#' and count < limit:
                    x,y  = x+dx, y+dy
                    count += 1
                    res.add((x,y))
            return res
        
        def getNeighbors(state: State) -> List[State]:
            posMouse, posCat = state.mouse, state.cat
            ans = []
            if state.turn == MOUSE_TURN:
                for pos in getPossiblePos(posMouse, MOUSE_TURN):
                    ans.append(State(pos, posCat, 1-state.turn))
            else:
                for pos in getPossiblePos(posCat, CAT_TURN):
                    ans.append(State(posMouse, pos, 1-state.turn))
            return ans
        
        # states = {}
        degrees = collections.defaultdict(int)
        graph = {}
        # buildGraph
        for pos1 in itertools.product(range(m), range(n)):
            if grid[pos1[0]][pos1[1]] == '#': continue
            for pos2 in itertools.product(range(m), range(n)):
                if grid[pos2[0]][pos2[1]] == '#': continue
                # states[State(pos1, pos2, MOUSE_TURN)] = []
                # 猫/老鼠不动, 两个状态互为邻居
                degrees[State(pos1, pos2, MOUSE_TURN)] = 1
                degrees[State(pos1, pos2, CAT_TURN)] = 1
                for t in [MOUSE_TURN, CAT_TURN]:
                    state = State(pos1, pos2, t)
                    neighbors = getNeighbors(state)
                    # degrees[state] = len(neighbors)
                    graph[state] = neighbors
        degrees = {s: len(n) for s,n in graph.items()}
        nG = collections.defaultdict(list)
        for state in graph:
            for neighbor in graph[state]:
                nG[neighbor].append(state)
        
        # 
        q = collections.deque()
        ans = collections.defaultdict(lambda: -1)
        # 终止条件
        """ 在 debug 的时候担心这里节点是否会重复等问题; 但实际上, 因为有 ans 的检查, 无所谓 """
        for state in nG:
            posMouse, posCat, turn = state.mouse, state.cat, state.turn
            if posCat==PosFood or posCat==posMouse:
                ans[state] = False
                q.append(state)
            elif posMouse==PosFood:
                ans[state] = True
                q.append(state)
        # for pos in itertools.product(range(m), range(n)):
        #     if grid[pos[0]][pos[1]] == '#': continue
        #     for t in [MOUSE_TURN, CAT_TURN]:
        #         s = State(pos, pos, t)
        #         ans[s] = False
        #         q.append(s)
        # for pos in itertools.product(range(m), range(n)):
        #     if grid[pos[0]][pos[1]] == '#' or pos==PosFood: continue
        #     for t in [MOUSE_TURN, CAT_TURN]:
        #         s = State(pos, PosFood, t)
        #         ans[s] = False
        #         q.append(s)
        #         s = State(PosFood, pos, t)
        #         ans[s] = True
        #         q.append(s)
        
        # x = [State((0,0), (0,2), 0), State((0,4), (0,2), 1)]
        while q:
            state = q.popleft()
            # turn = state.turn
            for prevNode in nG[state]:
                # 避免重复
                if prevNode in ans: continue
                canWin = (ans[state]==True and prevNode.turn==MOUSE_TURN) or ((ans[state]==False) and prevNode.turn==CAT_TURN)
                if canWin:
                    r = True if prevNode.turn==MOUSE_TURN else False
                    ans[prevNode] = r
                    q.append(prevNode)
                    # break
                else:
                    degrees[prevNode] -= 1
                    # 技巧: 监视某些值, 在 debug状态打断点观察.
                    # if prevNode in x:
                    #     print()
                    if degrees[prevNode] == 0:
                        """ 注意这里! 当前行动体a的所有子节点都无法获胜, 则说明该节点为必败节点
                        而非搜索终止, 猫获胜"""
                        # ans[prevNode] = False
                        r = False if prevNode.turn==MOUSE_TURN else True
                        ans[prevNode] = r
                        q.append(prevNode)
                        # break
        a = ans[State(PosMouse, PosCat, MOUSE_TURN)]
        a = False if a==-1 else a
        return a

    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.catMouseGame(graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]),
    # sol.catMouseGame(graph = [[1,3],[0],[3],[0,2]]),
    
    # sol.canMouseWin(grid = ["M.C...F"], catJump = 1, mouseJump = 4),
    # sol.canMouseWin(grid = ["####F","#C...","M...."], catJump = 1, mouseJump = 2),

]
for r in result:
    print(r)
