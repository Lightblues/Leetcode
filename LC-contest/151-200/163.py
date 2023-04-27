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
https://leetcode.cn/contest/weekly-contest-163

本期质量较高! 
T1比较经典. T2的二叉树类似「堆」, 值得思考. T3也是经典的问题. T4 的推箱子也过分复杂了...

@2022 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    """ 1260. 二维网格迁移 #easy 循环移动grid 共 k步. 
 """
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m,n = len(grid),len(grid[0])
        ans = [[0]*n for _ in range(m)]
        k = k % (m*n)
        for x in range(m):
            for y in range(n):
                idx = (n*x+y + k) % (m*n)
                nx,ny = divmod(idx, n)
                ans[nx][ny] = grid[x][y]
        return ans
    
    """ 1262. 可被三整除的最大和 #medium 给定一个数组, 要求选择最大的子集, 其和能够被3整除. 
思路1: 要求和能够被3整除, (假设数组和余数为x) 等价于选出和最小的子数组, 满足余数为 x.
"""
    def maxSumDivThree(self, nums: List[int]) -> int:
        s = sum(nums)
        r = s % 3
        if r==0: return s
        div1, div2 = [], []
        for x in nums:
            if x % 3 == 1: div1.append(x)
            elif x % 3 == 2: div2.append(x)
        div1.sort(); div2.sort()
        mn = inf
        if r==1:
            if len(div1)>=1: mn = min(mn, div1[0])
            if len(div2)>=2: mn = min(mn, div2[0]+div2[1])
        else:
            if len(div2)>=1: mn = min(mn, div2[0])
            if len(div1)>=2: mn = min(mn, div1[0]+div1[1])
        return s - mn
    
    
    """ 1263. 推箱子 #hard #题型 #模拟 模拟能够推到目标. 最小的推动步骤. 限制: m,n 20 
思路1: #暴力 #BFS 搜索. 
    最短路径问题, 一般可以采用 #BFS + #队列 解决.
    这里, 针对 箱子进行BFS, 同时还需要考虑人的位置. 两者合起来, 进行 #记忆化 搜索. 
    状态表示: d, state={(bx,by), (px,py)} 表示: d步, 箱子位置, 人的位置.
    状态更新: up(state, dir), 返回是否合法, 已经新的状态.
    复杂度: 搜索空间为 O(mn*mn), 每个状态的更新复杂度为 O(1), 总复杂度为 O(m^2n^2). 实际上还是sl的排序复杂度...
    下面用了sl来简化队列的逻辑, 实际上可以一次遍历推动步数d的每一层, 参见 zero
    [zero 的官答](https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/solution/ti-jie-1263-tui-xiang-zi-by-zerotrac/)
进阶解法: [人tarjan+箱A*](https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/solution/1263-tui-xiang-zi-po-su-de-bfsbfsjiu-ke-yi-tong-gu/)
"""
    from sortedcontainers import SortedList
    def minPushBox(self, grid: List[List[str]]) -> int:
        m,n = len(grid), len(grid[0])
        diretions = [(0,1),(0,-1),(1,0),(-1,0)]
        def move(bx,by, px,py):
            # 检查当前状态的合法性, 并且返回新的可转移状态.
            # 返回: 是否推动了箱子, newState
            if not (0<=bx<m and 0<=by<n and 0<=px<m and 0<=py<n): return []
            if grid[bx][by]=='#' or grid[px][py]=='#': return []
            ans = []
            for dx,dy in diretions:
                nx,ny = px+dx, py+dy
                if not (0<=nx<m and 0<=ny<n): continue
                if grid[nx][ny]=='#': continue
                if nx==bx and ny==by: 
                    nbx,nby = bx+dx, by+dy
                    if not (0<=nbx<m and 0<=nby<n): continue
                    if grid[nbx][nby]=='#': continue
                    ans.append((1,nbx,nby, nx,ny))
                else: ans.append((0,bx,by, nx,ny))
            return ans
        # 初始化
        posB = posP = posT = None
        for x,y in product(range(m), range(n)):
            ch = grid[x][y]
            if ch=='S': posP = (x,y)
            elif ch=='T': posT = (x,y)
            elif ch=='B': posB = (x,y)
        # 记忆化搜索
        seen = set()
        sl = SortedList()   # 利用sl来代替队列. 
        sl.add((0, posB[0],posB[1], posP[0],posP[1]))
        while sl:
            d, bx,by, px,py = sl.pop(0)
            if (bx,by)==posT: return d
            if (bx,by,px,py) in seen: continue
            seen.add((bx,by,px,py))
            for moved, nbx,nby, npx,npy in move(bx,by, px,py):
                nd = d + moved
                sl.add((nd, nbx,nby, npx,npy))
        return -1
    
    """ 1261. 在受污染的二叉树中查找元素 #medium 规范的二叉树定义了每个节点 left, right 的值分别为 2*v+1, 2*v+2, 根节点值0 (可以画出来). 
要求根据树结构还原值, 并提供 find 接口. 
思路1: 直接DFS重建; 利用全局的集合记录出现的数字
思路2: 能否不用全局存储? 可以对于所有数字都 +1, 根据二进制发现规律.
    见 [here](https://leetcode.cn/problems/find-elements-in-a-contaminated-binary-tree/solution/bu-yong-setde-findfang-fa-by-cyanflxy/)
"""
class FindElements:
    def __init__(self, root: Optional[TreeNode]):
        self.vals = set()
        def f(node: TreeNode, v: int):
            if node is None: return
            self.vals.add(v)
            f(node.left, 2*v+1)
            f(node.right, 2*v+2)
        f(root, 0)

    def find(self, target: int) -> bool:
        return target in self.vals
    
    

    
sol = Solution()
result = [
    # sol.shiftGrid(grid = [[1,2,3],[4,5,6],[7,8,9]], k = 1),
    # sol.maxSumDivThree(nums = [3,6,5,1,8]),
    sol.minPushBox(grid = [["#","#","#","#","#","#"],
             ["#","T","#","#","#","#"],
            ["#",".",".","B",".","#"],
            ["#",".","#","#",".","#"],
            ["#",".",".",".","S","#"],
            ["#","#","#","#","#","#"]]),
]
for r in result:
    print(r)
