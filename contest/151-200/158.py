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
https://leetcode.cn/contest/weekly-contest-158

@2022 """
class Solution:
    """ 1221. 分割平衡字符串 """
    def balancedStringSplit(self, s: str) -> int:
        ans = 0
        cntL = cntR = 0
        for c in s:
            if c=='L': cntL+= 1
            else: cntR+= 1
            if cntL==cntR:
                ans += 1
                cntL=cntR=0
        return ans
    
    """ 1222. 可以攻击国王的皇后 """
    def queensAttacktheKing(self, queens: List[List[int]], king: List[int]) -> List[List[int]]:
        m = 8
        ans = []
        queens = set(map(tuple, queens))
        for dx,dy in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            x,y = king
            while 0<=x<m and 0<=y<m:
                x+= dx
                y+= dy
                if (x,y) in queens:
                    ans.append([x,y])
                    break
        return ans
    
    """ 1223. 掷骰子模拟 #hard 掷n个骰子, 形成一个序列 (共 6^n 种可能), 对于每个数字约束其在序列中不能连续出现 rollMax[i] 次, 问有多少种不同的序列? 限制: n 5e3, rollMax[i] 15, 对结果取模
记 `f[n,x,c]` 表示长n的序列, 以连续c个x结尾的数量. 则有转移
    若 c>1, 则 f[n,x,c] = f[n-1,x,c-1]
    若 c=1, 有 f[n,x,c] = sum(f[n-1,y!=x,rr]), 这里需要 rr是任意的值, 并且需要满足 rollMax限制.
    复杂度: 转移复杂度 O(6*15), 空间复杂度 O(6*15*n)
可以写成 #记忆化 的形式 [here](https://leetcode.cn/problems/dice-roll-simulation/solution/python-ji-yi-hua-sou-suo-by-qin-qi-shu-h-zm2d/)
"""
    def dieSimulator(self, n: int, rollMax: List[int]) -> int:
        mod = 10**9+7
        mx = max(rollMax)
        f = [[0]*(mx+1) for _ in range(6)]
        for i in range(6): f[i][1] = 1
        for _ in range(n-1):
            nf = [[0]*(mx+1) for _ in range(6)]
            for x in range(6):
                for c in range(2, rollMax[x]+1):
                    nf[x][c] = f[x][c-1]
                for y in range(6):
                    if y==x: continue
                    for r in range(1, rollMax[y]+1):
                        nf[x][1] += f[y][r]
                        nf[x][1] %= mod
            f = nf
        return sum(sum(f[x]) for x in range(6)) % mod
    
    """ 1224. 最大相等频率 #hard 见 d88 """
    
sol = Solution()
result = [
    # sol.balancedStringSplit(s = "RLLLLRRRLR"),
    # sol.queensAttacktheKing(queens = [[0,1],[1,0],[4,0],[0,4],[3,3],[2,4]], king = [0,0]),
    sol.dieSimulator(n = 2, rollMax = [1,1,2,2,2,3]),
]
for r in result:
    print(r)
