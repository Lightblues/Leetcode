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
https://leetcode-cn.com/contest/biweekly-contest-128
T3 UCS 变体
T4 想到了 #单调栈 就比较简单
Easonsi @2023 """
class Solution:
    """ 3110. 字符串的分数 """
    def scoreOfString(self, s: str) -> int:
        b = ord(s[0])
        ss = 0
        for c in s[1:]:
            ss += abs(ord(c)-b)
            b = ord(c)
        return ss
    
    """ 3111. 覆盖所有点的最少矩形数目 """
    def minRectanglesToCoverPoints(self, points: List[List[int]], w: int) -> int:
        xs = sorted(set(i for i,j in points))
        pre = -w-1; cnt = 0
        for x in xs:
            if pre+w < x: 
                cnt += 1
                pre = x
        return cnt
    
    """ 3112. 访问消失节点的最少时间 #medium UCS, 节点会在某些时刻消失 """
    def minimumTime(self, n: int, edges: List[List[int]], disappear: List[int]) -> List[int]:
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        ans = [inf] * n; ans[0] = 0
        vis = set(); h = [(0,0)] # time, u
        while h:
            t, u = heappop(h)
            if u in vis: continue
            vis.add(u)
            for v,w in g[u]:
                if v in vis: continue
                if t+w < ans[v] and t+w < disappear[v]:
                    ans[v] = t+w
                    heappush(h, (t+w, v))
        return [i if i < inf else -1 for i in ans]
    
    """ 3113. 边界元素是最大值的子数组数目 对于一个数组, 找到所有子数组, 使得第一和最后一个元素是最大值. 限制: n 1e5
思路1: 从左往右遍历, 用一个栈来维护数值的递减顺序
[ling](https://leetcode.cn/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/solutions/2738894/on-dan-diao-zhan-pythonjavacgo-by-endles-y00d/)
    讲了一些变体
    """
    def numberOfSubarrays(self, nums: List[int]) -> int:
        s = []
        res = 0
        for i,x in enumerate(nums):
            while s and s[-1][0] < x: s.pop()
            if s and s[-1][0] == x:
                s[-1][1] += 1
                res += s[-1][1]
            else:
                s.append([x,1])
                res += 1
        return res

sol = Solution()
result = [
    # sol.scoreOfString("hello"),
    # sol.minRectanglesToCoverPoints(points = [[2,1],[1,0],[1,4],[1,8],[3,5],[4,6]], w = 1),
    # sol.minimumTime(n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,3,5]),
    # sol.minimumTime(n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,1,5]),
    sol.numberOfSubarrays(nums = [1,4,3,3,2]),
]
for r in result:
    print(r)
