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
https://leetcode.cn/circle/discuss/ByQDEU/
灵神: https://www.bilibili.com/video/BV1dg4y1j78A/

Easonsi @2023 """
class Solution:
    """ LCP 72. 补给马车 #easy 
对于长为n的车队, 要求缩减为原来的一半. 缩减方式: 每次合并两辆连续的和最小的车. 
限制: n 1e3
思路1: 暴力, 复杂度 O(^2)
思路2: 链表+堆,  复杂度 O(n logn)
    """
    def supplyWagon(self, supplies: List[int]) -> List[int]:
        n = len(supplies)
        tt = ceil(n/2)
        for _ in range(tt):
            idx = -1; mn = inf
            for i in range(len(supplies)-1):
                if supplies[i]+supplies[i+1] < mn:
                    mn = supplies[i]+supplies[i+1]
                    idx = i
            supplies[idx] = mn
            supplies.pop(idx+1)
        return supplies

    """ LCP 73. 探险营地 #medium 检查每次增加的新的营地的数量最多
简单模拟
    """
    def adventureCamp(self, expeditions: List[str]) -> int:
        n = len(expeditions)
        for i in range(n):
            # 注意空字符串!
            expeditions[i] = set(expeditions[i].split("->")) if expeditions[i] else set()
        s = expeditions[0]
        mx=0; ans=-1
        for i in range(1,n):
            nnew = len(expeditions[i]-s)
            if nnew>mx:
                mx = nnew
                ans = i
            s |= expeditions[i]
        return ans
    
    """ LCP 74. 最强祝福力场 #medium 有一些 (x,y,side) 所定义的正方形, 求被覆盖数量最多的点的数量! 
限制: n 100; x,y,side 1e9; 
思路1: 二维 #差分 + #离散化
    注意到, 只需要考虑整数 (0.5的整点) 计数即可
    如何快速求? 采用差分! 注意这里是二维情况
    数字范围很大, 但是注意正方形数量非常小, 考虑离散化
    """
    def fieldOfGreatestBlessing(self, forceField: List[List[int]]) -> int:
        # (x1,y1,x2,y2)
        squares = []
        for x,y,side in forceField:
            r = side / 2
            squares.append((x-r,y-r, x+r,y+r))
        xs,ys = set(),set()
        for x1,y1,x2,y2 in squares:
            xs.add(x1); xs.add(x2)
            ys.add(y1); ys.add(y2)
        xmap = {x:i for i,x in enumerate(sorted(xs))}
        ymap = {y:i for i,y in enumerate(sorted(ys))}
        xmax = len(xmap); ymax = len(ymap)
        squares = [(xmap[x1],ymap[y1], xmap[x2],ymap[y2]) for x1,y1,x2,y2 in squares]
        # 注意下面二维差分的写法
        acc = [[0]*(ymax+2) for _ in range(xmax+2)] # 注意 +2
        for x1,y1,x2,y2 in squares:
            x1,y1,x2,y2 = x1+1,y1+1,x2+1,y2+1
            acc[x1][y1] += 1
            acc[x1][y2+1] -= 1
            acc[x2+1][y1] -= 1
            acc[x2+1][y2+1] += 1
        ans = 0
        for i in range(1,xmax+1):
            for j in range(1,ymax+1):
                acc[i][j] += acc[i-1][j] + acc[i][j-1] - acc[i-1][j-1]
                ans = max(ans, acc[i][j])
        return ans

    
    """ LCP 75. 传送卷轴 #hard  """

    
sol = Solution()
result = [
    # sol.supplyWagon(supplies = [7,3,6,1,8]),
    # sol.adventureCamp(expeditions = ["leet->code","leet->code->Campsite->Leet","leet->code->leet->courier"]),
    # sol.adventureCamp(expeditions = ["","Gryffindor->Slytherin->Gryffindor","Hogwarts->Hufflepuff->Ravenclaw"]),
    sol.fieldOfGreatestBlessing(forceField = [[4,4,6],[7,5,3],[1,6,2],[5,6,3]]),
]
for r in result:
    print(r)
