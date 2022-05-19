from typing import List, Optional, Tuple
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 
"""



class RangeModule:
    """ 0715. Range 模块 #hard #题型
要求实现对于 [) 形式的区间的 增删查操作.
思路1: 关联 6066, 用两个数组分别记录左右边界. 在添加记录的时候, 注意进行区间的合并.
思路2: [官方](https://leetcode.cn/problems/range-module/solution/range-mo-kuai-by-leetcode/) 答案中 #区间求交 #二分
实现了一个通用的函数, 计算查询区间 [l,r) 与所存储的区间有交集, 实现更为方便的 add, remove.
#技巧: 通过 (100, 10, 1) 这种形式的步长衰减来替代bisect

输入
["RangeModule", "addRange", "removeRange", "queryRange", "queryRange", "queryRange"]
[[], [10, 20], [14, 16], [10, 14], [13, 15], [16, 17]]
输出
[null, null, null, true, false, true]

解释
RangeModule rangeModule = new RangeModule();
rangeModule.addRange(10, 20);
rangeModule.removeRange(14, 16);
rangeModule.queryRange(10, 14); 返回 true （区间 [10, 14) 中的每个数都正在被跟踪）
rangeModule.queryRange(13, 15); 返回 false（未跟踪区间 [13, 15) 中像 14, 14.03, 14.17 这样的数字）
rangeModule.queryRange(16, 17); 返回 true （尽管执行了删除操作，区间 [16, 17) 中的数字 16 仍然会被跟踪）

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/range-module
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
    def __init__(self):
        self.left = []
        self.right = []

    def addRange(self, left: int, right: int) -> None:
        """ 增加区间.
        注意, 如果已经有 [1,2), [3,4) 区间, 然后插入一个新区间 [2,3), 需要将其与相连的合并起来."""
        if len(self.left)==0:
            self.left.append(left)
            self.right.append(right)
            return
        # 注意为了查找数组交叉关系, 需要用 right 查找维护的左区间, 用 left 查找维护的右区间
        # 为了将相邻的数组合并 例如 [1,2) 和 [2,3), 需要分别 bisect_left, bisect_right
        idxL = bisect.bisect_left(self.right, left)
        idxR = bisect.bisect_right(self.left, right)
        if idxL == idxR:
            # 注意有 idxL<= idxR
            # idxL == idxR 说明: 没有与其他区间的交叉, 插入
            # 因此这里已经避免了 idxL==idxR == len() / 0 的边界情况, 下面的 idxL 和 idxR-1 可以不用判断越界
            valL, valR = left, right
        else:
            # 因为有了上面的判断, 可以避免数组越界
            valL = min(self.left[idxL], left)
            valR = max(self.right[idxR-1], right)
        # 用 slice 更新数组, 效率较高
        self.left[idxL:idxR] = [valL]
        self.right[idxL:idxR] = [valR]

    def queryRange(self, left: int, right: int) -> bool:
        """ 查询 [left, right) 区间是否被包含
        例子: 已有区间 [16,20), 则对于查询 [16,17), [17,18), [16,20) 均返回 True
        注意边界情况
        !! 智障!! 由于必然是包含关系, 只需要bisect一个index即可!
        """
        # 剪枝, 可以避免数组越界
        if len(self.left)==0: return False
        idxL = bisect.bisect_left(self.left, left)
        idxR = bisect.bisect_left(self.right, right)
        # 完全被包含的情况
        if idxL > idxR:
            return True
        # 这里用了 bisect_left, 说明超出了最大范围
        # 主要是为了避免数组越界
        if idxL>=len(self.left):
            return False
        return idxL==idxR and self.right[idxR]>=right and self.left[idxL]<=left

    def removeRange(self, left: int, right: int) -> None:
        """ 删除区间 """
        if len(self.left)==0: return
        idxL = bisect.bisect_left(self.right, left)
        # 注意删除不需要 bisect_right
        idxR = bisect.bisect_left(self.left, right)
        if idxL==idxR: return
        # 
        l, r = [], []
        if self.left[idxL] < left:
            l.append(self.left[idxL])
            r.append(left)
        if self.right[idxR-1]>right:
            l.append(right)
            r.append(self.right[idxR-1])
        self.right[idxL:idxR] = r
        self.left[idxL:idxR] = l

class RangeModule(object):
    def __init__(self):
        self.ranges = []

    def _bounds(self, left, right):
        """ 计算与 [left, right) 存在交集的区间有哪些
        #技巧: 通过 (100, 10, 1) 这种形式的步长衰减来替代bisect """
        i, j = 0, len(self.ranges) - 1
        for d in (100, 10, 1):
            while i + d - 1 < len(self.ranges) and self.ranges[i+d-1][1] < left:
                i += d
            while j >= d - 1 and self.ranges[j-d+1][0] > right:
                j -= d
        return i, j

    def addRange(self, left, right):
        i, j = self._bounds(left, right)
        if i <= j:
            left = min(left, self.ranges[i][0])
            right = max(right, self.ranges[j][1])
        self.ranges[i:j+1] = [(left, right)]

    def queryRange(self, left, right):
        i = bisect.bisect_left(self.ranges, (left, float('inf')))
        if i: i -= 1
        return (bool(self.ranges) and
                self.ranges[i][0] <= left and
                right <= self.ranges[i][1])

    def removeRange(self, left, right):
        i, j = self._bounds(left, right)
        merge = []
        for k in range(i, j+1):
            if self.ranges[k][0] < left:
                merge.append((self.ranges[k][0], left))
            if right < self.ranges[k][1]:
                merge.append((right, self.ranges[k][1]))
        self.ranges[i:j+1] = merge



class Solution:
    """ 0913. 猫和老鼠 #hard
给定一张图, 老鼠和猫分别从 1和2 出发, 老鼠到的目标 0 则获胜 (猫不能到达0). 给定初始状态, 求在双方都是最优解的情况下, 哪一方获胜.
注意, 可能出现平均的情况! 分别用 1/2/0 表示老鼠/猫获胜/平均.
复杂度: 图的节点数最大 50.
[here](https://leetcode.cn/problems/cat-and-mouse/solution/mao-he-lao-shu-by-leetcode-solution-444x/)
思路0: 自顶向下 DP
状态: `dp[mouse][cat][turns]` 表示猫和老鼠所在的节点以及当前轮次.
终止条件: 1) 老鼠到达终点或被抓到; 2) 关键是如何判断平局? 注意到有时必须遍历所有的相邻节点才能得到答案, 那么两个相邻节点之间就可能发生死锁! 
注意到, 这里的所有节点状态为 2n(n-1), 猫和老鼠可以到达的点乘积 * 该轮轮到老鼠/猫移动. 在每个 agent 都是理性的情况下, 若出现重复访问节点则说明平局.
然而, 复杂度相当高! DP数组的复杂度为 $n^4$, 而对每一个状态计算状态值 `getNextResult` 的复杂度为 n, 因此总体复杂度为 $n^5$, 即使 $n=50$ 也是超时.
思路1: #拓扑排序
上一种思路中, 判断平局需要迭代到 $n^2$ 复杂度. 为了避免重复访问节点, 相较于「自顶向下」我们可以「自底向上」进行遍历 (实际上就是拓扑排序!).
具体而言, 这里一共只有 n^2 个节点, 我们通过枚举所有的终止状态, 然后从该状态反推. 对于上一个节点: 
    可以判断胜利的条件: 对于当前行动体 a 的获胜条件: 当前为a的回合并且可以走到一个a的必胜节点
    否则: 无法判断, 继续往下查找. 为了避免重复访问, 我们记录每一个节点的度数, 每遇到这种情况就 -1.
        若一直到度数=0还不行, 则说明, a无论选择所有行动都无法获胜, a必败 (注意不是平局); 
        对于最后剩余无法判断的节点, 平局 (因此初始化所有节点为平局).
在主循环中, 我们维护一个 **queue**, 存放所有确定结局的节点. 遍历过程中, 1) 对于一个确定结局的节点, 将其加入 queue; 2) 否则, 度数 -1.
分析上述流程, 其实就是 #拓扑排序.


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
和 0913 类似的设定. 不过图换成了更为现实的带有墙的grid, 以及猫和老鼠每一次都可以选择走 1~limit 步.
另外给出限制: 如果老鼠不能在 1000 次操作以内到达食物，那么猫获胜.
因此, 这题的返回就是 T/F 表示是否为老鼠获胜.
复杂度: 网格长宽 8*8, 1 <= catJump, mouseJump <= 8. 

思路: 还是按照之前的思路, 反向搜索, #拓扑排序
这里定义了状态结构 `namedtuple('State', ['mouse', 'cat', 'turn'])` 前两个 (x,y) 表示两类agent的位置, 0/1 的turn 表示当前是谁的行动回合.
相较于 0913 这里需要构造节点之间的转移关系 (图).
另外, 反向拓扑排序的时候需要注意, 记录的节点度数为出度; 对应了在反向搜索的过程中, 如果不满足条件则 degree额-1.

技巧: 监视某些值, 在 debug状态打断点观察. 例如, 关心一个字典中某一个 key 的值变化, 可以把这个数值存到一个变量中, 打一个断点. 如, `if prevNode in x` 行判断是否需要监视, 下一行 `print(x[prevNode])` 上加断点.
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


    """ 调用ACM格式输入 """
    def test_class(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res

    """ 0547. 省份数量 #medium
给定一个矩阵形式的图结构, 计算其中的联通分量的个数.
思路1: 并查集. 每次遇到一条边, 将两个集合 union.
"""
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        # 初始化所有节点的 farther 为自己
        parents = list(range(n))
        
        def find(x):
            path = []
            while parents[x] != x:
                path.append(x)
                x = parents[x]
            for i in path:
                parents[i] = x
            return x
        
        def union(x,y):
            rootx, rooty = find(x), find(y)
            parents[rootx] = rooty
            
        for i in range(n):
            for j in range(i+1, n):
                if isConnected[i][j]:
                    union(i,j)
        # 所有 root 元素的数量
        return sum(1 for i in range(n) if parents[i]==i)
    
    """ 399. 除法求值 #medium #并查集 #题型
思路1: 采用并查集. 注意到, 这里需要维护集合之间的相对大小关系. 那么, 的时候, 如何记录这一关系?
注意到, 在查询的时候, 只有root相同(在同一集合内)的两个数才能比较, 因此 **只需要记录节点与根节点的大小关系**, 在查询时不需要考虑不同集合的倍率.
因此, 问题转为, 如何在合并时记录两集合的大小关系? 只需要记录在跟节点上, 在 find 的时候更新子节点即可!
具体而言, 对于比例关系 a = v*b, 构建的时候我们令 b为根节点, 然后 `value[b]=1, value[a]=v`. 这样, 我们在同一颗树上, 跟节点的值为1, 并且有 value[a] = a/roota (后两者为真实值)
这样, 在union过程中, 若有 x = v * y 在两个集合中; 我们求出两者的根节点, 然后令 `father[rootx] = rooty`. (根节点rooty的值仍为1)
如何更新 rootx 的值? (注意, 这里我们仅关心 rootx 的值, x的值会在find的时候进行更新) 此时, 我们有两个参考系, 目标是将 rootx 转到y的参考系.
下面用 value 表示参考系y, value' 表示参考系x. 则我们需要求 value[rootx].
在y参考系下, 有 value[x] = v * value[y]
另有 value[x] = value'[x] * value[rootx], 这是因为在不同参考系下, x/rootx 的比例关系是固定的.
因此有, `value[rootx] = v * value[y] / value'[x]`
"""
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # https://leetcode.cn/problems/evaluate-division/solution/pythonbing-cha-ji-fu-mo-ban-by-milomusia-kfsu/
        class UnionFind:
            def __init__(self):
                """
                记录每个节点的父节点
                记录每个节点到根节点的权重
                """
                self.father = {}
                self.value = {}
            
            def find(self,x):
                """
                查找根节点
                路径压缩
                更新权重
                """
                root = x
                # 节点更新权重的时候要放大的倍数
                base = 1
                while self.father[root] != None:
                    root = self.father[root]
                    base *= self.value[root]
                
                while x != root:
                    original_father = self.father[x]
                    ##### 离根节点越远，放大的倍数越高
                    self.value[x] *= base
                    base /= self.value[original_father]
                    #####
                    self.father[x] = root
                    x = original_father
                
                return root
            
            def merge(self,x,y,val):
                """
                合并两个节点
                """
                root_x,root_y = self.find(x),self.find(y)
                
                if root_x != root_y:
                    self.father[root_x] = root_y
                    ##### 四边形法则更新根节点的权重
                    self.value[root_x] = val * self.value[y] / self.value[x]

            def is_connected(self,x,y):
                """
                两节点是否相连
                """
                return x in self.value and y in self.value and self.find(x) == self.find(y)
            
            def add(self,x):
                """
                添加新节点，初始化权重为1.0
                """
                if x not in self.father:
                    self.father[x] = None
                    self.value[x] = 1.0


        uf = UnionFind()
        for (a,b),val in zip(equations,values):
            uf.add(a)
            uf.add(b)
            uf.merge(a,b,val)
    
        res = [-1.0] * len(queries)

        for i,(a,b) in enumerate(queries):
            if uf.is_connected(a,b):
                res[i] = uf.value[a] / uf.value[b]
        return res
    
    """ 0316. 去除重复字母 #medium #题型 #单调栈 #stack
要求得到一个字符串的子串, 1) 由原本字符串中的所有元素组成; 2) 所有字符不重复; 3) 字典序最小.
思路: 单调栈
去除限制条件, 我们如何得到一个尽可能小的字符串? 基本思路是 **维护一个单调栈**, 当遇到一个新的字符时, 如果栈顶元素小于当前字符, 则递归弹出栈顶元素, 然后再把这个字符入栈; 否则直接把当前字符压入栈 (注意当前字符总会入栈).
这里要求 1) 保留原字符串中的所有元素, 因此用一个 counter 记录剩余的数量, 当剩余数量为0时, 我们不能将该元素弹出栈; 3) 字符不重复, 因此在入栈的时候判断该字符是否已经在栈内.
[here](https://leetcode.cn/problems/remove-duplicate-letters/solution/qu-chu-zhong-fu-zi-mu-by-leetcode-soluti-vuso/)
"""
    def removeDuplicateLetters(self, s: str) -> str:
        stack = []
        # counter 记录字母剩余的数量
        counter = collections.Counter(s)
        for ch in s:
            counter[ch] -= 1
            # 字符已经用过了, 去重
            if ch in stack: continue
            while stack and ch < stack[-1]:
                # 注意这里是 while, 例如 "bcabc" 需要将栈中的 bc 都弹出.
                # 剩余字符还有, 可以弹出
                if counter[stack[-1]] > 0: stack.pop()
                else: break
            # ch 在 ch < stack[-1] 与否两种情况下都会入栈
            stack.append(ch)
        return "".join(stack)


sol = Solution()
result = [
    # sol.catMouseGame(graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]),
    # sol.catMouseGame(graph = [[1,3],[0],[3],[0,2]]),
    
    # sol.canMouseWin(grid = ["M.C...F"], catJump = 1, mouseJump = 4),
    # sol.canMouseWin(grid = ["####F","#C...","M...."], catJump = 1, mouseJump = 2),

#     sol.test_class("""["RangeModule","addRange","queryRange","removeRange","removeRange","addRange","queryRange","addRange","queryRange","removeRange"]
# [[],[5,8],[3,4],[5,6],[3,6],[1,3],[2,3],[4,8],[2,3],[4,9]]"""),
#     sol.test_class("""["RangeModule","addRange","addRange","addRange","queryRange","queryRange","queryRange","removeRange","queryRange"]
# [[],[10,180],[150,200],[250,500],[50,100],[180,300],[600,1000],[50,150],[50,100]]"""),
#     sol.test_class("""["RangeModule", "addRange", "removeRange", "queryRange", "queryRange", "queryRange"]
# [[], [10, 20], [14, 16], [10, 14], [13, 15], [16, 17]]"""),
#     sol.test_class("""["RangeModule","addRange","addRange","addRange","queryRange","queryRange","queryRange","removeRange","queryRange"]
# [[],[10,180],[150,200],[250,500],[50,100],[180,300],[600,1000],[50,150],[50,100]]"""),

    # sol.findCircleNum(isConnected = [[1,1,0],[1,1,0],[0,0,1]]),
    # sol.findCircleNum(isConnected = [[1,0,0],[0,1,0],[0,0,1]]),
    
    # sol.calcEquation([["a","b"],["e","f"],["b","e"]],[3.4,1.4,2.3],[["b","a"],["a","f"],["f","f"],["e","e"],["c","c"],["a","c"],["f","e"]]),
    # sol.calcEquation(equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]),
    # sol.calcEquation([["a","b"],["c","d"]],[1.0,1.0],[["a","c"],["b","d"],["b","a"],["d","c"]]),
    
    # sol.removeDuplicateLetters(s = "bcabc"),
    # sol.removeDuplicateLetters(s = "cbacdcbc"),
    

]
for r in result:
    print(r)
