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
https://leetcode.cn/contest/weekly-contest-156
T3是一个经典题型, 官答给出了很多种的解法, 值得阅读. 
T4被搞了, 题目理解错了... 当然题目本身的代码也比较有意思. 

@2022 """
class Solution:
    """ 1207. 独一无二的出现次数 """
    
    """ 1208. 尽可能使字符串相等 """
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        diff = [abs(ord(s[i]) - ord(t[i])) for i in range(len(s))]
        ans = 0
        l = 0
        acc = 0
        for r,d in enumerate(diff):
            acc += d
            while l<len(diff) and acc>maxCost: acc-=diff[l]; l+=1
            ans = max(ans, r-l+1)
        return ans
                
    """ 1209. 删除字符串中的所有相邻重复项 II #题型 #medium 给定一个字符串重复操作: 删除相邻的连续的k个字符. 返回最后剩下的结果. 限制: n 1e5; k 1e4
思路1: 利用 #栈 记录字符的重复次数. 
    栈内所存的数据格式 (ch, cnt)
见 [官答](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string-ii/solution/shan-chu-zi-fu-chuan-zhong-de-suo-you-xiang-lin--4/) 讨论了很多种的题解~
"""
    def removeDuplicates(self, s: str, k: int) -> str:
        st = []
        for ch in s:
            if st and st[-1][0]==ch:
                st[-1][1] += 1
                if st[-1][1]==k: st.pop()
            else:
                st.append([ch, 1])
        return ''.join([ch*cnt for ch,cnt in st])

    
    
    """ 1210. 穿过迷宫的最少移动次数 #hard #细节 #review 需要从左上角走到右下角, 但是现在是一个 1*2 的蛇. 限制: n 100
行走规则: 只有在四个格子只都是空格的情况下才能「旋转」, 否则只能保持水平/竖直移动. 注意是只能向右下移动!
思路0: 注意理解题意, 一开始理解为可以随便旋转移动, 但实际只能右下移动. 导致WA了一次...
思路1: 构建「超图」, 在其上搜索. #超图
    对于两个连续的空格当作一个新的节点. 蛇头蛇尾在相邻的两个点 (x1,y1, x2,y2) 作为一个超节点.
    细节: 如何判断边界? 一种简单的方式, 是下面先枚举所有可能的超节点, 然后判断是否合法即可.
    如何找到「最短路径」? 直接 #BFS 即可
    参见 [here](https://leetcode.cn/problems/minimum-moves-to-reach-target-with-rotations/solution/golang-bfs-by-resara-2/)
"""
    def minimumMoves(self, grid: List[List[int]]) -> int:
        # 
        n = len(grid)
        # def toId(x1,y1,x2,y2): return x1*n+y1, x2*n+y2
        # 得到所有的超节点
        nodes = set()
        for x,y in itertools.product(range(n),range(n)):
            if grid[x][y]==1: continue
            for dx,dy in [(0,1),(1,0)]:
                if x+dx<n and y+dy<n and grid[x+dx][y+dy]==0:
                    nodes.add((x,y,x+dx,y+dy))
                    # nodes.add((x+dx,y+dy,x,y))
        g = defaultdict(list)
        # for x1,y1,x2,y2 in nodes:
        #     if x1==x2: 
        #         # 向前
        #         if (x2,y2,x2,y2+1) in nodes: g[(x1,y1,x2,y2)].append((x2,y2,x2,y2+1))
        #         # 向后
        #         if (x2,y2,x2,y2-1) in nodes: g[(x1,y1,x2,y2)].append((x2,y2,x2,y2-1))
        #         if (x1-1,y1,x2-1,y2) in nodes: 
        #             g[(x1,y1,x2,y2)].append((x1-1,y1,x2-1,y2))  # 平移
        #             g[(x1,y1,x2,y2)].append((x1,y1,x1-1,y1))    # 旋转
        #         if (x1+1,y1,x2+1,y2) in nodes: 
        #             g[(x1,y1,x2,y2)].append((x1+1,y1,x2+1,y2))
        #             g[(x1,y1,x2,y2)].append((x1,y1,x1+1,y1))
        #     # y1==y2
        #     else:
        #         # 向上
        #         if (x2,y2,x2-1,y2) in nodes: g[(x1,y1,x2,y2)].append((x2,y2,x2-1,y2))
        #         # 向下
        #         if (x2,y2,x2+1,y2) in nodes: g[(x1,y1,x2,y2)].append((x2,y2,x2+1,y2))
        #         if (x1,y1-1,x2,y2-1) in nodes:
        #             g[(x1,y1,x2,y2)].append((x1,y1-1,x2,y2-1))  # 平移
        #             g[(x1,y1,x2,y2)].append((x1,y1,x1,y1-1))    # 旋转
        #         if (x1,y1+1,x2,y2+1) in nodes: 
        #             g[(x1,y1,x2,y2)].append((x1,y1+1,x2,y2+1))
        #             g[(x1,y1,x2,y2)].append((x1,y1,x1,y1+1))
        # 构建超图上的边关系
        for node in nodes:
            x1,y1,x2,y2 = node
            if x1==x2:
                # (x2,y2) = (x1,y1+1)
                if (x2,y2,x2,y2+1) in nodes: g[node].append((x2,y2,x2,y2+1))
                if (x1+1,y1,x2+1,y2) in nodes:
                    g[node].append((x1+1,y1,x2+1,y2))
                    g[node].append((x1,y1,x1+1,y1))
            else:
                if (x2,y2,x2+1,y2) in nodes: g[node].append((x2,y2,x2+1,y2))
                if (x1,y1+1,x2,y2+1) in nodes:
                    g[node].append((x1,y1+1,x2,y2+1))
                    g[node].append((x1,y1,x1,y1+1))
        # 基本BFS框架
        def bfs(s,e):
            q = deque([(s,0)])
            visited = set()
            while q:
                node,step = q.popleft()
                if node==e: return step
                if node in visited: continue
                visited.add(node)
                for nei in g[node]:
                    q.append((nei,step+1))
            return -1
        return bfs((0,0,0,1),(n-1,n-2,n-1,n-1))

    
sol = Solution()
result = [
    # sol.equalSubstring(s = "abcd", t = "bcdf", maxCost = 3),
    # sol.minimumMoves(grid = [[0,0,0,0,0,1],[1,1,0,0,1,0],[0,0,0,0,1,1],[0,0,1,0,1,0],[0,1,1,0,0,0],[0,1,1,0,0,0]]),
    # sol.minimumMoves([[0,0,0,0,0,0,0,0,0,1],[0,1,0,0,0,0,0,1,0,1],[1,0,0,1,0,0,1,0,1,0],[0,0,0,1,0,1,0,1,0,0],[0,0,0,0,1,0,0,0,0,1],[0,0,1,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0]]),
    sol.removeDuplicates(s = "deeedbbcccbdaa", k = 3),
]
for r in result:
    print(r)
