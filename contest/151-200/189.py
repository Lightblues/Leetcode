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
https://leetcode.cn/contest/weekly-contest-189
@2022 """
class Solution:
    """ 1450. 在既定时间做作业的学生人数 """
    def busyStudent(self, startTime: List[int], endTime: List[int], queryTime: int) -> int:
        ans = 0
        for s,e in zip(startTime, endTime):
            if s<=queryTime<=e: ans += 1
        return ans
    
    """ 1451. 重新排列句子中的单词 """
    def arrangeWords(self, text: str) -> str:
        words = [i.lower() for i in text.split(' ')]
        words.sort(key=lambda x: len(x))
        words[0] = words[0].capitalize()
        return ' '.join(words)
    
    """ 1452. 收藏清单 #medium 有一组集合, 问其中「不是其他任意集合的子集」的集合. 限制: n 100, 每个集合的长度 s 500.
思路1: #暴力. 枚举子集关系, 每次检查是否为子集, 总体复杂度 O(n^2 s)
"""
    def peopleIndexes(self, favoriteCompanies: List[List[str]]) -> List[int]:
        companies = reduce(lambda x,y: x|y, [set(i) for i in favoriteCompanies])
        company2id = {c:i for i,c in enumerate(companies)}
        sets = [set(company2id[c] for c in cc) for cc in favoriteCompanies]
        ans = []
        for i,s in enumerate(sets):
            for j,ss in enumerate(sets):
                if j==i: continue
                if s.issubset(ss): break
            else:
                ans.append(i)
        return ans
    
    """ 1453. 圆形靶内的最大飞镖数量 #hard #题型 #几何 二维坐标上有一组点, 飞镖可以覆盖半径为r的区域, 问能否覆盖的最大点数. 
限制: n 100. r 5000. 二维平面 [+/- 1e4]
思路1: 这里的点数量较小, 可以考虑 #暴力 枚举.
    提示: 我们肯定可以在两个图上点的半径为r的交点上找到答案. (考虑移动圆找到边界)
    复杂度: O(n^3). 最多有 n^2 个交点, 以每个点为圆心进行检查的复杂度为 n.
    问题变换: 如何求 (x1,y1), (x2,y2) 两个点为圆心, r 为半径的两圆的交点? 
        一种方式可以通过 #向量 的角度来理解. 我们要在中点 (x1+x2/2, y1+y2/2) 的基础上加上直角三角形的「高」 这条向量. 
    参见 [here](https://leetcode.cn/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/solution/c-xiang-liang-suan-yuan-xin-jian-dan-yi-dong-by-sm/)
    补充: 需要两个交点吗? 实验验证, 似乎这里只需要一个方向即可 (即使只枚举了 i<j), 应该可以有一个数学的证明.
细节: 又是被 #浮点 误差坑的一题!
"""
    def numPoints(self, darts: List[List[int]], r: int) -> int:
        # 又基本是 copilot补的标准答案
        delta = 1e-8        # 避免浮点误差
        def dist(a,b):
            return (a[0]-b[0])**2 + (a[1]-b[1])**2
        def get_cross(a,b,r):
            # 得到 a,b 两点以r为圆心的两个圆的交点.
            d = dist(a,b)
            if d > 4*r**2: return []
            mx, my = [(a[0]+b[0])/2, (a[1]+b[1])/2]
            if d == 4*r**2: return [[mx,my]]
            height = (r**2-d/4)**0.5    # 直角三角形高
            # 分别乘以 sin, cos 值.
            dx = (a[1]-b[1])/d**0.5 * height
            dy = (b[0]-a[0])/d**0.5 * height
            # 神奇的是, 这里只需要一个方向即可 (即使只枚举了 i<j), 应该可以有一个数学的证明.
            # return [[mx+dx,my+dy], [mx-dx,my-dy]]
            return [[mx+dx,my+dy]]
        ans = 1
        for i in range(len(darts)):
            for j in range(i+1, len(darts)):
                # if i==j: continue
                for cross in get_cross(darts[i], darts[j], r):
                    cnt = 0
                    for dart in darts:
                        if dist(dart, cross) <= r**2 + delta: cnt += 1
                    ans = max(ans, cnt)
        return ans
    
sol = Solution()
result = [
    # sol.busyStudent(startTime = [1,2,3], endTime = [3,2,7], queryTime = 4),
    # sol.arrangeWords(text = "Leetcode is cool"),
    # sol.peopleIndexes(favoriteCompanies = [["leetcode","google","facebook"],["leetcode","amazon"],["facebook","google"]]),
    sol.numPoints(darts = [[-2,0],[2,0],[0,2],[0,-2]], r = 2),
    sol.numPoints([[-3,0],[3,0],[2,6],[5,4],[0,9],[7,8]], 5),
    sol.numPoints([[4,5],[-4,1],[-3,2],[-4,0],[0,2]], 5),
]
for r in result:
    print(r)
