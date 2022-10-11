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
https://leetcode.cn/contest/weekly-contest-177

前两题好玩! T1是基本的日期计算, 需要掌握; T2验证二叉树很有意思, 想不清楚容易WA; T4题面很清楚, 需要考虑一些细节.

@2022 """
class Solution:
    """ 1360. 日期之间隔几天 #easy #题型
给定两个 `YYYY-MM-DD` 形式的字符串, 问两个日期之间间隔几天. 限制: 年份 1971 年到 2100
思路1: 基本的日期计算. 计算从 1971-01-01 日开始到该天的天数.
    细节: 如何判断闰年? `(year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)`
[官答](https://leetcode.cn/problems/number-of-days-between-two-dates/solution/ri-qi-zhi-jian-ge-ji-tian-by-leetcode-solution/)
"""
    def daysBetweenDates(self, date1: str, date2: str) -> int:
        # 直接调包. 很好用!
        import datetime
        return abs((datetime.datetime.strptime(date1, "%Y-%m-%d") - datetime.datetime.strptime(date2, "%Y-%m-%d")).days)
    def daysBetweenDates(self, date1: str, date2: str) -> int:
        # 思路1: 基本的日期计算. 计算从 1971-01-01 日开始到该天的天数.
        days = [31,28,31,30,31,30,31,31,30,31,30,31]
        def leap_year(year):
            return (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)
        def getDays(year,month,day):
            # 返回从 1971 开始第几天
            acc = 0
            for y in range(1971,year):
                acc += 366 if leap_year(y) else 365
            for m in range(month-1):
                acc += days[m]
            if month > 2 and leap_year(year):
                acc += 1
            acc += day
            return acc
        # print(getDays(1971,1,1), getDays(1971,3,1))
        y1,m1,d1 = map(int,date1.split('-'))
        y2,m2,d2 = map(int,date2.split('-'))
        return abs(getDays(y1,m1,d1) - getDays(y2,m2,d2))
    
    """ 1361. 验证二叉树 #medium #题型 对于每一个节点, 通过两个数组给出它的左右节点. 判断这样的连接方式是否构成一颗合法的二叉树.
如何判断是否合法? 1. 有且仅有一个根节点. 2. 不能有环.
思路1: 先找到root节点, 然后BFS看是否有环.
    如何找root? 可以记录一个 indeg 数组, 有且仅有一个节点的 indeg 为 0.
思路2: 可以用 #并查集 来记录联通情况 (判断是否有环)
    一开始 WA 了, 因为单纯用 并查集 无法处理 collapse 的情况! 后来加了 father 来处理这一情况.
    然后, 注意这里是有向边! 额外用了 `father` 记录节点的父亲节点, 若冲突则说明出现了 collapse.
[官答](https://leetcode.cn/problems/validate-binary-tree-nodes/solution/yan-zheng-er-cha-shu-by-leetcode-solution/)
"""
    def validateBinaryTreeNodes(self, n: int, leftChild: List[int], rightChild: List[int]) -> bool:
        # 找到root: 有且仅有一个节点没有父节点
        indeg = [0] * n
        for u in leftChild + rightChild:
            if u != -1: indeg[u] += 1
        if sum(i==0 for i in indeg) != 1: return False
        root = indeg.index(0)
        
        # 从 root 出发 BFS, 判断是否能到达所有节点
        seen = set([root])
        q = collections.deque([root])
        while len(q) > 0:
            u = q.popleft()
            for c in [leftChild[u], rightChild[u]]:
                if c!=-1:
                    # 判断是否有环
                    if c in seen: return False
                    seen.add(c); q.append(c)
        return len(seen) == n
    def validateBinaryTreeNodes(self, n: int, leftChild: List[int], rightChild: List[int]) -> bool:
        # 思路2: 用并查集判断是否有环
        # 一开始 WA 了, 因为单纯用 并查集 无法处理 collapse的情况! 后来加了 father 来处理这一情况.
        # 有效的边的数量应该是 n-1
        links = sum(i!=-1 for i in leftChild + rightChild)
        if links != n-1: return False
        
        fa = list(range(n))
        # sz = [1] * n
        father = [-1] * n
        def find(x):
            if fa[x] != x: fa[x] = find(fa[x])
            return fa[x]
        def merge(x,y):
            if x>y: x,y = y,x
            fx,fy = find(x),find(y)
            fa[fy] = fx

        for i,(l,r) in enumerate(zip(leftChild, rightChild)):
            for c in [l,r]:
                if c==-1: continue
                if father[c]!=-1: return False
                father[c] = i
                if find(i)==find(c): return False
                merge(i,c)
        return True
    
    """ 1362. 最接近的因数 #medium 给定一个整数num, 要求找到两个整数 a,b, 使得 a*b = num+1 或 num+2. 并且 a,b 尽可能接近.
思路1: 暴力搜索.
"""
    def closestDivisors(self, num: int) -> List[int]:
        mn = num
        a,b = 1,num+1
        def search(x):
            nonlocal mn,a,b
            for i in range(1, int(x**0.5)+1):
                if x%i==0:
                    c,d = i,x//i
                    if abs(c-d) < mn: a,b,mn = c,d,abs(c-d)
        search(num+1); search(num+2)
        return [a,b]

    """ 1363. 形成三的最大倍数 #hard #细节 #题型 给定一组0-9数字, 按照任意顺序选择连接, 要求得到的最大的能被3整除的数.
思路1: 按照和3的关系分成 0/1/2 三组. 首先要求数位尽可能长.
    主要看 1/2 的个数, 假设分别记为 a,b. 考虑不同情况. 假设 a>b. 1) 取 b组 1+2 组合, 再加上 (a-b)//3 个 1; 2) 还可能是a,b= 3,1 这种情况, 取3个1更优.
    分析可知, 当 (a-b) % 3==2时, 选择组合2更好.
有一些细节, 参见 [官答](https://leetcode.cn/problems/largest-multiple-of-three/solution/xing-cheng-san-de-zui-da-bei-shu-by-leetcode-solut/).
"""
    def largestMultipleOfThree(self, digits: List[int]) -> str:
        digitsby3 = [[],[],[]]
        for d in digits: digitsby3[d%3].append(d)
        a,b = len(digitsby3[1]),len(digitsby3[2])
        # 上面的两种特殊情况. 注意 (2,0) 也不能去不能取.
        if a>b>0 and (a-b)%3==2: a,b = a,b-1
        elif b>a>0 and (b-a)%3==2: a,b = a-1,b
        # 其他情况.
        else: 
            if a>b: a,b = b+((a-b)//3)*3,b
            else: a,b = a,a+((b-a)//3)*3
        # 所有采用的数位.
        ds = digitsby3[0] + sorted(digitsby3[1],reverse=True)[:a] + sorted(digitsby3[2],reverse=True)[:b]
        ds.sort(reverse=True)
        if len(ds)==0: return ""
        # 去除前导0.
        elif ds[0]==0: return "0"
        else: return "".join(map(str,ds))
        

    
sol = Solution()
result = [
    # sol.daysBetweenDates(date1 = "2020-01-15", date2 = "2019-12-31"),
    # sol.validateBinaryTreeNodes(n = 4, leftChild = [1,-1,3,-1], rightChild = [2,-1,-1,-1]),
    # sol.validateBinaryTreeNodes(n = 4, leftChild = [1,-1,3,-1], rightChild = [2,3,-1,-1]),
    # sol.validateBinaryTreeNodes(n = 2, leftChild = [1,0], rightChild = [-1,-1]),
    # sol.validateBinaryTreeNodes(n = 6, leftChild = [1,-1,-1,4,-1,-1], rightChild = [2,-1,-1,5,-1,-1]),
    # sol.validateBinaryTreeNodes(4, [1,0,3,-1], [-1,-1,-1,-1]),
    # sol.closestDivisors(123),
    # sol.closestDivisors(999),
    # sol.largestMultipleOfThree(digits = [8,1,9]),
    # sol.largestMultipleOfThree(digits = [8,6,7,1,0]),
    sol.largestMultipleOfThree(digits = [1]),
    sol.largestMultipleOfThree(digits = [0,0,0,0,0,0]),
]
for r in result:
    print(r)
