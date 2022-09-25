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

https://leetcode.cn/circle/discuss/XP89Tp/

@2022 """

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    """ 1. 气温变化趋势 LCP 61. 气温变化趋 #easy 一段时间的气温变化可表示为 -1/0/1 序列. 给定两个城市, 问「气温变化趋势相同的最大连续天数」 势 """
    def temperatureTrend(self, temperatureA: List[int], temperatureB: List[int]) -> int:
        ta, tb = [], []
        def f(x,y):
            if x>y: return 1
            if x<y: return -1
            return 0
        for i in range(len(temperatureA)-1):
            ta.append(f(temperatureA[i], temperatureA[i+1]))
            tb.append(f(temperatureB[i], temperatureB[i+1]))
        ans = s = 0
        for i in range(len(ta)):
            if ta[i] == tb[i]: s += 1
            else: s = 0
            ans = max(ans, s)
        return ans
    
    """ 2. 交通枢纽 LCP 62. 交通枢纽 给定一张有向图, 找到其中「其他所有点都连向x, 但x不连向其他点」的点x. """
    def transportationHub(self, path: List[List[int]]) -> int:
        din = [0] * 1001
        dout = [0] * 1001
        s = set()
        for u,v in path:
            din[v] += 1
            dout[u] += 1
            s.add(u); s.add(v)
        for i in range(1001):
            if din[i]==len(s)-1 and dout[i]==0:
                return i
        return -1
    
    """ 3. 弹珠游戏
给定一个grid表示弹珠. 从四条边 (不包含角) 出发向内发射弹珠, 最大距离 num. 弹珠按照下面的规则前进, 直到进洞/出边界/达到距离限制. 要求找到所有可行的发射位置.
"W" 表示逆时针转向器; "E" 表示顺时针转向器; "O" 表示弹珠洞. 限制: 网格大小 n 1e3; 距离限制 num 1e6
思路0: #反向 #模拟. 从洞出发, 检测是否能到达边界.
    结果 #TLE 因此复杂度比较高? 注意到弹珠洞可能有 n^2 个, 这样整体复杂度最多 `O(n^2 * num)`!
思路1: 正向 #模拟. 从所有可能的位置模拟发射弹珠.
    这样的复杂度应该是 O(n * num).
    细节: 注意, 根据本题设置, 从任意点出发的光线是不可能重复的! 所有不需要 #记忆化 

"""
    def ballGame(self, num: int, plate: List[str]) -> List[List[int]]:
        # 思路0: #反向 #模拟. 从洞出发, 检测是否能到达边界. #TLE
        m,n = len(plate), len(plate[0])
        code2dir = {
            1: (0,1), 2: (0,-1), 3: (1,0), 4: (-1,0)
        }
        Ecode = {1:4, 2:3, 3:1, 4:2}
        Wcode = {1:3, 2:4, 3:2, 4:1}
        def isCorner(x,y):
            return (x==0 or x==m-1) and (y==0 or y==n-1)
        def isMargin(x,y):
            return x==0 or x==m-1 or y==0 or y==n-1
        def testSuccess(x,y,c):
            if plate[x][y] != '.': return False
            if isCorner(x,y): return False
            if x==0 and c==4: return True
            elif x==m-1 and c==3: return True
            elif y==0 and c==2: return True
            elif y==n-1 and c==1: return True
            return False
        def testIn(x,y):
            return 0<=x<m and 0<=y<n
        def step(x,y,code):
            dx,dy = code2dir[code]
            return x+dx, y+dy
        @lru_cache(None)
        def test(x,y, c, remain):
            # 检测逆向可否到达边界.
            if not testIn(x,y): return False, []
            # if isCorner(x,y): return False, []
            if isMargin(x,y):
                if testSuccess(x,y,c): return True, [x,y]
                # else:
                #     if plate[x][y] == 'O' and remain==num: pass
                #     else: return False, []
            b = plate[x][y]
            # if b=='.' and testSuccess(x,y,c): return True, [x,y]
            if remain==0: return False, []
            if b=='.' or (b=='O' and remain==num):
                x,y = step(x,y,c)
                return test(x,y,c,remain-1)
            elif b=='W': 
                x,y = step(x,y,Wcode[c])
                return test(x,y, Wcode[c], remain-1)
            elif b=='E': 
                x,y = step(x,y,Ecode[c])
                return test(x,y, Ecode[c], remain-1)
            # elif b=='O': return False, []
            return False, []
        
        ans = []
        for x,y in product(range(m), range(n)):
            if plate[x][y] == 'O':
                for c in range(1,5):
                    f, r = test(x,y,c, num)
                    if f: 
                        ans.append(r)
        return ans

    def ballGame(self, num: int, plate: List[str]) -> List[List[int]]:
        # 思路1: 正向 #模拟. 从所有可能的位置模拟发射弹珠.
        DIRS = ((0,1), (1,0), (0,-1), (-1,0))       # 右下左上（顺时针）
        m, n = len(plate), len(plate[0])
        def check(x, y, d) -> bool:
            # 判断从 (X,Y) 方向 d, 出发在限制 num 内能否进洞.
            left = num
            while plate[x][y] != 'O':
                if left==0: return False
                if plate[x][y]=='W': d = (d+3)%4    # 逆时针; Python 中可以直接 (d-1)%4
                elif plate[x][y]=='E': d = (d+1)%4  # 顺时针
                x += DIRS[d][0]; y += DIRS[d][1]
                if not (0<=x<m and 0<=y<n): return False
                left -= 1
            return True
        
        ans = []
        # 模拟上下边
        for j in range(1, n-1):
            if plate[0][j] == '.' and check(0,j,1): ans.append([0,j])
            if plate[m-1][j] == '.' and check(m-1,j,3): ans.append([m-1,j])
        # 模拟左右边
        for i in range(1, m-1):
            if plate[i][0] == '.' and check(i,0,0): ans.append([i,0])
            if plate[i][n-1] == '.' and check(i,n-1,2): ans.append([i,n-1])
        return ans

    """ 4. 二叉树灯饰 
给一个二叉树, 上面有一些灯. 每个节点可以 1) 切换单节点; 2) 切换它和左右孩子; 3) 切换它所定义的整颗子树. 问最少操作多少次, 可以熄灭所有灯. 限制: 节点 n 1e5
思路1: 
    对于每个节点, 递归返回 [a,aa,b,bb], 分别表示 原结构, root发生了反转, 整体反转, 整体反转+root反转 的情况下, 最小次数.
    假设两子树分别返回 [la,laa, lb,lbb], [ra,raa, rb,rbb]. 节点状态为 n,nn (若节点为1, 则用操作1需要1次).
        以结果a的结算为例: `a = min(la+ra+n, laa+raa+nn+1, lb+rb+nn+1, lbb+rbb+n+2)`, 对应了四种情况
            1) 对root仅使用操作1; 2) 对root使用操作1+2; 3) 对root使用操作1+3; 4) 对root使用操作1+2+3.
    结果 #WA

https://leetcode.cn/contest/season/2022-fall/problems/U7WvvU/
# 7
[1,0,0,0,1,0,1,null,1,1,null,null,null,null,null,1,1,1,1,null,null,1,1,null,1,null,null,1,null,null,null,null,null,1,0,1,1,0,1,null,null,0,null,null,null,null,1]
"""
    def closeLampInTree(self, root: TreeNode) -> int:
        def dfs(node: TreeNode):
            # return: [a,aa, b,bb]
            if node is None: return [0,0,0,0]
            if node.left is None and node.right is None:
                n = node.val # 0/1
                nn = 1-n 
                return [n,nn,nn,n]
            la,laa, lb,lbb = dfs(node.left)
            ra,raa, rb,rbb = dfs(node.right)
            n = node.val # 0/1
            nn = 1-n
            a = min(la+ra+n, laa+raa+nn+1, lb+rb+nn+1, lbb+rbb+n+2)
            aa = min(la+ra+nn, laa+raa+n+1, lb+rb+n+1, lbb+rbb+nn+2)
            b = min(laa+raa+nn, la+ra+n+1, lbb+rbb+n+1, lb+rb+nn+2)
            bb = min(laa+raa+n, la+ra+nn+1, lbb+rbb+nn+1, lb+rb+n+2)
            return [a,aa, b,bb]
        a,aa,b,bb = dfs(root)
        return a


    """ 5. 舒适的湿度
题目等价于: 给定一个数组, 可以对其每个元素设置正负号. 要求, 赋值的数组, 其「任意连续子数组的和的绝对值」的最大值最小化. 求这个值.
"""
root = TreeNode(1)
root.left = TreeNode(1)
root.right = TreeNode(0)
p = root.right
p.right = TreeNode(1)

# root = TreeNode(1)
# p = root
# p.left = TreeNode(1)
# p.right = TreeNode(1)
# p.left.left = TreeNode(1)
# p.right.right = TreeNode(1)
        
sol = Solution()
result = [
    # sol.temperatureTrend(temperatureA = [5,10,16,-6,15,11,3], temperatureB = [16,22,23,23,25,3,-16]),
    # sol.temperatureTrend(temperatureA = [21,18,18,18,31], temperatureB = [34,32,16,16,17]),
    # sol.transportationHub(path = [[0,1],[0,3],[1,3],[2,0],[2,3]]),
    # sol.transportationHub(path = [[0,3],[1,0],[1,3],[2,0],[3,0],[3,2]]),
    sol.ballGame(num = 4, plate = ["..E.",".EOW","..W."]),
    sol.ballGame(num = 5, plate = [".....","..E..",".WO..","....."]),
    sol.ballGame(num = 3, plate = [".....","....O","....O","....."]),
    sol.ballGame(6, ["....",".EE.","O.E.","...."]),     # [[3, 1]]
    sol.ballGame(69, ["W.W.WE..",".WWWEW..","EWW.WE.E","E.W.E.E.",".OEOO.EO","WE.WOE.W","WW...E..",".WEWO..O","E....E..",".OWE...."]),
    # [[1, 7], [4, 0], [0, 6], [9, 6], [6, 7], [0, 3], [9, 4]]
    # sol.closeLampInTree(root),
]
for r in result:
    print(r)
