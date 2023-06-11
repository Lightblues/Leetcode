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
https://leetcode.cn/contest/weekly-contest-343


Easonsi @2023 """
class Solution:
    """ 6341. 保龄球游戏的获胜者 #easy 翻译垃圾! 注意是第i轮的前两轮中有10分的情况下, 该轮得分 *2 """
    def isWinner(self, player1: List[int], player2: List[int]) -> int:
        def getScore(arr):
            s = 0
            for i in range(len(arr)):
                if (i>0 and arr[i-1]==10) or (i>1 and arr[i-2]==10):
                    s += arr[i]
                s += arr[i]
            return s
        # s1 = sum(player1) + (sum(player1[2:]) if (10 in player1[:2]) else 0)
        # s2 = sum(player2) + (sum(player2[2:]) if (10 in player2[:2]) else 0)
        s1,s2 = getScore(player1), getScore(player2)
        return 1 if s1>s2 else 2 if s1<s2 else 0
    
    """ 6342. 找出叠涂元素 #medium 依次对于矩形每个位置涂色, 找到第一个位置idx, 使得该行/该列其他单元格斗涂上了颜色 """
    def firstCompleteIndex(self, arr: List[int], mat: List[List[int]]) -> int:
        m,n = len(mat), len(mat[0])
        v2idx = {}
        for i,row in enumerate(mat):
            for j,x in enumerate(row):
                v2idx[x] = (i,j)
        cntCol = [0] * n
        cntRow = [0] * m
        for i,v in enumerate(arr):
            x,y = v2idx[v]
            cntCol[y] += 1
            if cntCol[y] == m:
                return i
            cntRow[x] += 1
            if cntRow[x] == n:
                return i
    
    """ 6343. 前往目标的最小代价 #medium
要从 (sx,sy) -> (tx,ty), 从基本的路径走的代价为 曼哈顿距离 |x2 - x1| + |y2 - y1|
但地图上包含一些特殊路径 [x1i, y1i, x2i, y2i, costi], 问整体的最小代价? 
限制: x,y 1e5; 路径数量 200
思路1: 转化为图求最短路
    只考虑 s,t,和特殊路径上的端点! 可以抽象为一张图, 这些点之间的距离为曼哈顿距离,
    然后用 #Dijkstra 来求最短路. 
    下面灵神的实现中, 没有建图
[灵神](https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/solution/zhi-jie-qiu-zui-duan-lu-wu-xu-jian-tu-by-i8h7/)
    """
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        # from 0x3f
        t = tuple(target)
        dis = defaultdict(lambda: inf)
        dis[tuple(start)] = 0
        vis = set()
        while True:
            v = None
            for p, d in dis.items():
                if p not in vis and (v is None or d < dis[v]):
                    v = p
            if v == t:  # 到终点的最短路已确定
                return dis[v]
            vis.add(v)
            vx, vy = v
            dis[t] = min(dis[t], dis[v] + t[0] - vx + t[1] - vy)  # 更新到终点的最短路
            for x1, y1, x2, y2, cost in specialRoads:
                w = (x2, y2)
                # 要么直接到 (x,y)，要么走特殊路径到 (x,y)
                d = dis[v] + min(abs(x1 - vx) + abs(y1 - vy) + cost, abs(x2 - vx) + abs(y2 - vy))
                dis[w] = min(dis[w], d)

    """ 6344. 字典序最小的美丽字符串 #hard 要求比初始的s更大的, 由字母表前k个字母组成的, 并且没有长度 >=2 的回文串
限制: s的长度n 1e5
思路1: #贪心 #细节
    初始化为 s+1, 然后贪心从高位开始解决回文的问题
    注意在代码内部的逻辑! 
[灵神](https://leetcode.cn/problems/lexicographically-smallest-beautiful-string/solution/tan-xin-pythonjavacgo-by-endlesscheng-yix5/)
    """
def smallestBeautifulString(self, s: str, k: int) -> str:
        a = ord('a')
        k += a
        s = list(map(ord, s))
        n = len(s)
        i = n - 1
        s[i] += 1  # 从最后一个字母开始
        while 0 <= i < n:
            if s[i] == k:  # 超过范围
                if i == 0: return ""
                # 进位
                s[i] = a
                i -= 1
                s[i] += 1
            elif i and s[i] == s[i - 1] or i > 1 and s[i] == s[i - 2]:
                s[i] += 1  # 如果 s[i] 和前面的字符形成回文串，就继续增加 s[i]
            else:
                i += 1  # 检查 s[i] 是否和后面的字符形成回文串
        return ''.join(map(chr, s))

sol = Solution()
result = [
    # sol.isWinner(player1 = [3,5,7,6], player2 = [8,10,10,2]),
    # sol.isWinner([5,6,1,10], [5,1,10,5]),
    sol.firstCompleteIndex(arr = [1,3,4,2], mat = [[1,4],[2,3]]),
]
for r in result:
    print(r)
