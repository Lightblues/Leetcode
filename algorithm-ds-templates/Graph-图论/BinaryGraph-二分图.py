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

class BinaryGraph:
    def __init__(self, n, m) -> None:
        self.g = [[] for _ in range(n)]
        self.n = n
        self.m = m
        self.pa = [-1] * n
        self.pb = [-1] * m
        self.dfs = 0        # 时间戳记
    
    def add(self, u,v):
        self.g[u].append(v)
    
    def dfs(self, v):
        # 最大匹配
        pass

    def solve(self):
        res = 0
        while True:
            self.dfn += 1
            cnt = 0
            for i in range(self.n):
                if self.pa[i] == -1 and self.dfs(i):
                    cnt += 1
            if cnt==0: break
            res += cnt
        return res

""" 
https://leetcode.cn/contest/weekly-contest-312
https://leetcode-cn.com/contest/biweekly-contest-81
@2022 """
class Solution:
    """ LCP 04. 覆盖 #hard 给定一个grid, 有些部分是坏的, 问能够不重叠地防止多少个 1*2 的骨牌 (可横放). 限制: 长宽 n 8.
提示: 将grid按照相邻的规则标记为 x,y, 则放置的骨牌一定占据 1个x, 1个y. 注意到, **可以将本问题转化为二分图最大匹配**.
思路1: 为了求最大匹配, 可以用 #匈牙利 算法.
    基本思路: 1) 初始时，最大匹配集合为空; 2) 我们先找到一组匹配边，加入匹配集合; 3) 找到一条增广路径，我们将其中的所有匹配边变为未匹配边，将所有的未匹配边变为匹配边; 4) 循环步骤 33，直到图中不存在增广路径。算法结束
    所谓「增广路径」: 匹配/未匹配边交替, 并且以未匹配边开始和结束的路径.
"""
    def domino(self, n: int, m: int, broken: List[List[int]]) -> int:
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
