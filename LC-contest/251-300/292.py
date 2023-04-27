from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6056. 字符串中最大的 3 位相同数字 """
    # import re
    # re.findall(r"")
    def largestGoodInteger(self, num: str) -> str:
        lastCh = " "
        count = 0
        ans = ""
        for ch in num+" ":
            if ch==lastCh:
                count += 1
                continue
            if count >= 3:
                if lastCh*3 > ans:
                    ans = lastCh*3
            count = 1
            lastCh = ch
        return ans
    
    """ 6057. 统计值等于子树平均值的节点数
对于一棵二叉树, 统计「节点值 = 节点所定义的子树中所有节点值的平均值」的节点数量
"""
    def averageOfSubtree(self, root: Optional[TreeNode]) -> int:
        def dfs(node: TreeNode) -> List[int]:
            """ 返回: ans, sum, count """
            if node is None:
                return (0, 0, 0)
            if node.left is None and node.right is None:
                return (1, node.val, 1)
            ans1, sum1, count1 = dfs(node.left)
            ans2, sum2, count2 = dfs(node.right)
            tmp = (sum1+sum2+node.val) // (count1+count2+1) == node.val
            return (ans1+ans2+tmp, sum1+sum2+node.val, count1+count2+1)
        return dfs(root)[0]
    
    """ 6058. 统计打字方案数
按照 0-9 到字母的键盘映射 (例如, 按 `'5'` 两次得到字母 `'k'`). 这样, `33` 可能表示 `dd` 或者 `e`.
给定按键的序列, 计算其映射出来的字母的方案数

思路: #DP + 累乘
首先, 对于一个数字, 比如 `2` 映射到 `abc`; 给一个长度为 i 的连续 2, 其可能的方案数是: `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`. 因此先用DP预先计算好所有的结果.
然后对于案件序列按照上述 DP 累乘即可
注意: 1) 一个数字可能对应 3/4 个字母, 需要区分; 2) 这样 DP 递归的数字很大, 要在计算过程进行 MOD, 自己提交时没有加, Python 大整数计算超时.
"""
    def countTexts(self, pressedKeys: str) -> int:
        MOD = 10**9+7
        
        def get_count(s: str) -> int:
            # 只包含数字 '2' 到 '9'
            if s in "79": return 4
            return 3
        
        def dp3():
            dp = [0]*max(len(pressedKeys)+1, 10)
            dp[1] = 1
            dp[2] = 2
            dp[3] = 4
            for i in range(4, len(pressedKeys)+1):
                # 注意加 MOD!!
                dp[i] = (dp[i-1] + dp[i-2] + dp[i-3])%MOD
            return dp
        def dp4():
            dp = [0]*max(len(pressedKeys)+1, 10)
            dp[1:5] = [1, 2, 4, 8]
            for i in range(5, len(pressedKeys)+1):
                dp[i] = (dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4])%MOD
            return dp
        dp3, dp4 = dp3(), dp4()
        
        ans = 1
        lastCh, count = " ", 0
        for ch in pressedKeys+" ":
            if ch == lastCh:
                count += 1
                continue
            if count > 0:
                c = get_count(lastCh)
                if c==3: ans = (ans*dp3[count])%MOD
                elif c==4: ans = (ans*dp4[count])%MOD
            lastCh, count = ch, 1
        return ans
    
    """ 6059. 检查是否有合法括号字符串路径
给定一个仅包括 `()` 的grid, 要求判断从左上到右下是否存在一条路径, 使得括号序列合法.

思路0: DFS, 超时了! 因为grid搜索的复杂度为 2^n, 这里n=100还是会超.
    改进: 参考 [here](https://leetcode-cn.com/problems/check-if-there-is-a-valid-parentheses-string-path/solution/tian-jia-zhuang-tai-hou-dfscpythonjavago-f287/) 加了 cache 之后过了
    离谱的是, 用默认的 lru_cache(maxsize=128) 会超时, 答案中用的是 Python 3.9 新的 cache = lru_cache(maxsize=None) 就可以过, 而且速度很快, 可能是 lru_cache 的实现太重了吧
思路1: #DP 
    从上往下一层一层遍历: 没一点可以由左侧或者上方的节点转移过来
    用 dp[i][j] 记录从左上角遍历到 (i,j), 剩余的左括号的数量, 用 set 记录.
    转移: 对于 (i,j), 取 dp[i-1][j], dp[i][j-1] 的 union, 然后根据 grid[i][j] 是左/右括号, 对于集合中的每个元素 +/-1, 注意不能出现负数
    """
    def hasValidPath(self, grid: List[List[str]]) -> bool:
        """ DFS """
        m, n = len(grid), len(grid[0])
        if (m+n)%2==0: return False
        if grid[-1][-1]!=")": return False
        def get_next(i,j):
            res = []
            if j<n-1: res.append((i,j+1))
            if i<m-1: res.append((i+1,j))
            return res
        
        # def dfs(i,j, stack):
        #     # 由于上面的判断, 这里直接合法了
        #     if (i,j)==(m-1,n-1) and len(stack)==1: return True
            
        #     if grid[i][j]=="(": stack.append("(")
        #     else:
        #         if len(stack)==0: return False
        #         stack.pop()
        #     for ni,nj in get_next(i,j):
        #         if dfs(ni,nj, stack[:]): return True
        #     return False
        
        # 最重要的是这里的 cache!! 离谱的是默认 maxsize=128 会超时, 而 maxsize=None (也即 3.9 新的 cache 函数) 就不会超时了
        @lru_cache(maxsize=None)
        def dfs(i,j, stackLen):
            # 由于上面的判断, 这里直接合法了
            if (i,j)==(m-1,n-1) and stackLen==1: return True
            # 剪枝? 其实不剪枝也无所谓
            # if stackLen - (m+n-1-i-j)>0: return False
            
            if grid[i][j]=="(": stackLen += 1
            else:
                if stackLen==0: return False
                stackLen -= 1
            for ni,nj in get_next(i,j):
                if dfs(ni,nj, stackLen): return True
            return False
        return dfs(0,0,0)

    def hasValidPath(self, grid: List[List[str]]) -> bool:
        # https://leetcode-cn.com/problems/check-if-there-is-a-valid-parentheses-string-path/solution/tian-jia-zhuang-tai-hou-dfscpythonjavago-f287/
        m, n = len(grid), len(grid[0])
        if (m + n) % 2 == 0 or grid[0][0] == ')' or grid[m - 1][n - 1] == '(': return False  # 剪枝

        @cache  # 效果类似 vis 数组
        def dfs(x: int, y: int, c: int) -> bool:
            if c > m - x + n - y - 1: return False  # 剪枝：即使后面都是 ')' 也不能将 c 减为 0
            if x == m - 1 and y == n - 1: return c == 1  # 终点一定是 ')'
            c += 1 if grid[x][y] == '(' else -1
            return c >= 0 and (x < m - 1 and dfs(x + 1, y, c) or y < n - 1 and dfs(x, y + 1, c))  # 往下或者往右
        return dfs(0, 0, 0)  # 起点

    
    def hasValidPath_1(self, grid: List[List[str]]) -> bool:
        """ DP
        dp[i][j] 记录从左上角遍历到 (i,j), 剩余的左括号的数量.
        """
        m, n = len(grid), len(grid[0])
        if (m+n)%2==0: return False
        if grid[0][0]!= "(": return False
        if grid[-1][-1]!=")": return False
        
        # 按照行 DP, 每一个元素记录可能保留的 ( 数量
        dp = [set() for _ in range(n)]
        dp[0].add(1)
        for i in range(1, n):
            ch = grid[0][i]
            if ch=="(":
                s = set(c+1 for c in dp[i-1])
                dp[i] = s
            else:
                l = list(dp[i-1])
                if (len(l)==1 and l[0]==0):
                    break
                s = set(c-1 for c in dp[i-1] if c>0)
                if len(s)==0: break
                dp[i] = s
        for i in range(1, m):
            newDP = [set() for _ in range(n)]
            if len(dp[0])>0:
                count = list(dp[0])[0]
                if grid[i][0]=="(":
                    newDP[0].add(count+1)
                else:
                    if count>0: newDP[0].add(count-1)
            for j in range(1, n):
                s = dp[j].union(newDP[j-1])
                ch = grid[i][j]
                if ch=="(":
                    newDP[j] = set(c+1 for c in s)
                else:
                    l = list(s)
                    if len(l)==0 or (len(l)==1 and l[0]==0):
                        # 注意这里不能 break!! 因为可能前面的几个 j 为空集
                        continue
                    newDP[j] = set(c-1 for c in s if c>0)
            dp = newDP
        if 0 in dp[-1]: return True
        return False

sol = Solution()
result = [
    # sol.largestGoodInteger(num = "6777133339"),
    
    # sol.countTexts(pressedKeys = "2"),
    # sol.countTexts(pressedKeys = "22233"),
    # sol.countTexts(pressedKeys = "222222222222222222222222222222222222"),
    
    # T,F
    sol.hasValidPath(grid = [["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]),
    sol.hasValidPath(grid = [[")",")"],["(","("]]),
    
    sol.hasValidPath(grid = [["(","(","(","(","(",")",")","(",")",")","(",")",")","(",")","(","(",")",")","(",")","(",")",")","(",")",")",")",")","(",")","(","("],["(",")",")","(","(",")",")",")",")","(",")","(",")","(",")","(","(",")",")","(","(","(","(",")",")",")",")",")","(","(",")","(","("],[")",")","(","(",")",")",")",")","(",")","(",")",")",")","(","(",")","(",")","(","(","(",")",")",")",")",")",")",")",")",")","(","("],["(","(","(",")","(",")",")",")","(",")","(","(","(",")","(",")","(",")","(",")","(",")","(",")",")",")","(","(",")","(",")",")",")"],[")","(",")","(",")",")",")",")","(","(","(","(",")","(",")","(","(","(","(","(",")","(","(",")",")","(","(","(",")","(",")",")","("],[")",")",")","(",")",")",")","(","(",")",")","(","(","(","(",")","(","(",")",")","(",")",")",")","(",")",")","(",")",")","(","(","("],[")","(",")","(","(",")",")","(",")",")",")","(","(","(",")","(","(","(",")","(",")","(",")",")",")",")",")","(",")",")","(","(",")"],["(","(",")",")","(",")",")","(","(","(","(",")","(",")","(","(","(","(","(","(",")","(",")","(",")",")","(","(","(",")","(","(",")"],[")",")","(","(",")",")","(","(","(","(","(","(","(",")",")","(","(","(",")",")","(",")","(","(",")",")","(",")",")","(",")","(","("],[")",")",")",")","(",")",")","(","(","(","(",")",")",")","(",")",")",")",")",")",")","(","(","(","(",")",")",")",")","(","(","(",")"]]),
    sol.hasValidPath([["(","(","(",")","(","(",")",")",")",")","(",")","(","(",")",")",")","(","(",")",")","(",")",")","(","(",")",")"],[")",")","(",")",")",")",")","(","(",")",")","(","(","(","(",")",")","(","(","(",")",")","(",")",")",")","(","("],["(",")","(","(",")",")",")",")",")",")",")",")","(",")","(",")",")","(","(","(",")","(","(","(","(",")",")",")"],[")","(",")",")",")",")","(","(",")",")","(",")",")",")","(",")","(",")","(","(","(","(",")","(",")",")","(",")"],[")","(",")","(","(","(","(","(",")","(",")","(","(",")","(",")",")","(",")","(","(","(","(","(",")","(",")","("],[")",")",")","(",")","(","(","(","(","(","(",")",")","(",")","(","(",")",")","(","(",")",")",")","(","(",")",")"],["(","(","(",")",")","(",")","(","(","(",")","(",")","(",")",")","(",")",")",")",")",")",")","(","(",")","(","("],["(",")",")",")","(",")",")",")","(","(",")",")",")","(","(","(",")","(",")","(","(","(",")","(","(",")","(","("],[")","(","(","(",")",")","(",")",")",")",")",")",")",")",")",")","(","(","(","(","(",")","(",")",")",")","(","("],["(",")","(","(",")","(",")",")",")",")","(","(",")",")",")","(","(","(","(",")","(",")",")","(","(",")","(","("],["(",")","(",")","(","(","(",")",")",")","(","(","(",")",")",")","(","(",")",")",")","(","(",")","(","(",")","("],[")",")",")","(",")","(","(","(",")",")",")","(","(","(",")",")",")",")",")","(",")",")","(","(",")",")",")",")"],["(",")",")",")","(",")",")",")","(","(","(",")","(",")",")",")","(",")",")","(","(",")",")","(","(","(","(","("],["(",")",")","(","(","(","(",")",")",")","(","(",")","(",")","(",")","(","(","(","(",")",")",")","(","(","(",")"],[")","(","(",")",")","(",")","(",")","(","(",")",")","(","(","(",")",")","(","(","(",")",")",")","(","(","(",")"]]),
]
for r in result:
    print(r)

# grid = [["(","(","(","(","(",")",")","(",")",")","(",")",")","(",")","(","(",")",")","(",")","(",")",")","(",")",")",")",")","(",")","(","("],["(",")",")","(","(",")",")",")",")","(",")","(",")","(",")","(","(",")",")","(","(","(","(",")",")",")",")",")","(","(",")","(","("],[")",")","(","(",")",")",")",")","(",")","(",")",")",")","(","(",")","(",")","(","(","(",")",")",")",")",")",")",")",")",")","(","("],["(","(","(",")","(",")",")",")","(",")","(","(","(",")","(",")","(",")","(",")","(",")","(",")",")",")","(","(",")","(",")",")",")"],[")","(",")","(",")",")",")",")","(","(","(","(",")","(",")","(","(","(","(","(",")","(","(",")",")","(","(","(",")","(",")",")","("],[")",")",")","(",")",")",")","(","(",")",")","(","(","(","(",")","(","(",")",")","(",")",")",")","(",")",")","(",")",")","(","(","("],[")","(",")","(","(",")",")","(",")",")",")","(","(","(",")","(","(","(",")","(",")","(",")",")",")",")",")","(",")",")","(","(",")"],["(","(",")",")","(",")",")","(","(","(","(",")","(",")","(","(","(","(","(","(",")","(",")","(",")",")","(","(","(",")","(","(",")"],[")",")","(","(",")",")","(","(","(","(","(","(","(",")",")","(","(","(",")",")","(",")","(","(",")",")","(",")",")","(",")","(","("],[")",")",")",")","(",")",")","(","(","(","(",")",")",")","(",")",")",")",")",")",")","(","(","(","(",")",")",")",")","(","(","(",")"]]
# for l in grid:
#     print(" ".join(l))
