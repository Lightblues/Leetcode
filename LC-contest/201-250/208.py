from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-208

读题+手速 场.

@2022 """
class Solution:
    """ 1598. 文件夹操作日志搜集器 """
    def minOperations(self, logs: List[str]) -> int:
        depth = 0
        for step in logs:
            if step=="./": continue
            elif step=="../":
                if depth>0: depth -=1
            else: depth += 1
        return depth
    
    """ 1599. 经营摩天轮的最大利润 #medium 题意奇怪的模拟题 """
    def minOperationsMaxProfit(self, customers: List[int], boardingCost: int, runningCost: int) -> int:
        wait = 0; acc = 0
        mx = 0; ans = -1
        for i,c in enumerate(customers):
            wait += c
            acc += min(4, wait)
            wait -= min(4, wait)
            tmp = boardingCost * acc - (i+1)*runningCost
            if tmp > mx:
                mx = tmp; ans = i+1
        step = len(customers)
        while wait > 0:
            acc += min(4, wait)
            wait -= min(4, wait)
            tmp = boardingCost*acc - (step+1)*runningCost
            if tmp>mx:
                mx = tmp; ans = step+1
            step += 1
        return ans
    """ 1601. 最多可达成的换楼请求数目 #hard 有一组换楼请求, 问最后能选择其中及其使得结果均衡. 直接DFS #回溯 即可. """
    def maximumRequests(self, n: int, requests: List[List[int]]) -> int:
        diffs = [0] * n
        nn = len(requests)
        ans = 0
        def dfs(idx, approved):
            nonlocal ans
            if idx==nn:
                if all(d==0 for d in diffs): ans = max(ans, approved)
                return
            f,t = requests[idx]
            if f==t:
                dfs(idx+1, approved+1)
                return
            diffs[f], diffs[t] = diffs[f]-1,diffs[t]+1
            dfs(idx+1, approved+1)
            diffs[f], diffs[t] = diffs[f]+1,diffs[t]-1
            dfs(idx+1, approved)
        dfs(0,0)
        return ans
    
    
    
""" 1600. 王位继承顺序 #medium 又是一道长长描述的题, 本质上简单考察了DFS
"""
class ThroneInheritance:
    def __init__(self, kingName: str):
        self.g = defaultdict(list)
        self.root = kingName
        self.dead = set()

    def birth(self, parentName: str, childName: str) -> None:
        self.g[parentName].append(childName)

    def death(self, name: str) -> None:
        self.dead.add(name)

    def getInheritanceOrder(self) -> List[str]:
        ans = []
        def dfs(node):
            if node not in self.dead: ans.append(node)
            for child in self.g[node]: dfs(child)
        dfs(self.root)
        return ans


    
    
sol = Solution()
result = [
    sol.maximumRequests(n = 3, requests = [[0,0],[1,2],[2,1]]),
]
for r in result:
    print(r)
