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
https://leetcode.cn/contest/weekly-contest-160

难度较高~ T1 用了二分. T2 考察了格雷码, 有待练习. 
T3是暴力的搜索. T4本身是个NP问题, 在小数据下可以暴力回溯. 

@2022 """
class Solution:
    """ 1237. 找出给定方程的正整数解 #medium 这里所给的函数是单调递增的, 满足 f(x, y) < f(x + 1, y) 和 f(x, y) < f(x, y + 1)
思路1: #二分
"""
    def findSolution(self, customfunction: 'CustomFunction', z: int) -> List[List[int]]:
        ans = []
        mx = 1001
        # Naive, TLE
        # for x,y in product(range(1,mx), range(1,mx)):
        #     if customfunction.f(x,y)==z: ans.append([x,y])
        # 修改成二分查找, 就OK了, 可以进一步优化, 利用上一行的idx更新下一行的范围...
        a = list(range(1,mx))
        for x in range(1,mx):
            idx = bisect_left(a, z, key=lambda y: customfunction.f(x,y))
            if idx<mx and customfunction.f(x,a[idx])==z: ans.append([x,a[idx]])
        return ans
    
    """ 1238. 循环码排列 #medium 给定一个n和start, 要求返回一个 0...2^n-1 的排列, 第一个数字是start, 并且相邻元素「二进制表示形式只有一位不同」 (首尾也相邻) 限制: n 16
思路1: 本质上就是 #格雷码
    格雷码的生成策略: 一开始是 0,1; 生成下一位 00,01, 11,10. 规律是: 将原本的前面补0, 然后倒序前面补1. 
    本题要找从start的开始的, 偏置即可.
https://leetcode.cn/problems/circular-permutation-in-binary-representation/
关联: 0089. 格雷编码. 
"""
    def circularPermutation(self, n: int, start: int) -> List[int]:
        # 生成格雷码
        ans = [0,1]
        for i in range(1,n):
            ans = ans + [x+2**i for x in ans[::-1]]
        # 找到start的位置
        idx = ans.index(start)
        return ans[idx:] + ans[:idx]
    """ 0089. 格雷编码 #medium 生成n位 #格雷码 序列. 限制: n 16
"""
    def grayCode(self, n: int) -> List[int]:
        if n == 0:
            return [0]
        gray_pre = self.grayCode(n-1)
        return gray_pre + [i+2**(n-1) for i in gray_pre[::-1]]
    
    """ 1239. 串联字符串的最大长度 #medium 有一组字符串, 选择其中子序列, 将这些字符串串连, 要求其中没有重复字符. 求最大长度. 限制: n 16
思路0: 预先构建节点之间的互斥(或者是相连)关系, 然后用 #回溯法 枚举所有可能的组合.
    证明是错的! 因为相斥关系不单单依赖当前的两个节点
思路1: 仍然是回溯法, 但是不预先构建互斥关系, 而是在回溯的过程中, 每次都检查当前的组合是否合法.
    复杂度: 枚举复杂度 2^n, 每次检查的复杂度 O(L), L是字符集大小, 因此总复杂度 O(2^n * L)
改进: #位运算 /表示. 见 [官答](https://leetcode.cn/problems/maximum-length-of-a-concatenated-string-with-unique-characters/solution/chuan-lian-zi-fu-chuan-de-zui-da-chang-d-g6gk/)
"""
    def maxLength(self, arr: List[str]) -> int:
        arr = [s for s in arr if len(set(s))==len(s)]
        n = len(arr)
        ans = 0
        arr = [set(s) for s in arr]
        def f(i, cur:set):
            nonlocal ans
            ans = max(ans, len(cur))
            for j in range(i,n):
                if not cur&arr[j]:
                    f(j, cur|arr[j])
        f(0,set())
        return ans
    
    """ 1240. 铺瓷砖 #hard 要用正方形瓷砖铺满 n*m 的矩形, 问最少需要的瓷砖数. 限制: m,n 13
注意: 不能分解成两个子矩阵! 见 [图](https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/)
思路1: #暴力 #回溯 + #剪枝
    尝试从左上角往下填充. 在 (x,y) 格尝试填入 1,2,3... 的正方形...
    如何填充满? 遍历的时候, 按照行优先, 一行一行填充. 
        判断 (x,y) 最大能填多大的正方形? 查看下边界和右边界
    剪枝: 填充过程中, 如果发现当前的填充已经超过了最优解, 就不用继续了.
        #启发 策略: 从大到小填充.
    见 [here](https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/solution/python3-hui-su-jian-zhi-by-minori-lsea/)
    在本题的小数据情况下, 还可以用 DP 来做, 但在大数据时不正确! 见 [here](https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/solution/ji-yi-hua-sou-suo-python-by-alienjiren-m947/)
关于本题 NP-hard 的 [解释](https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/solution/guan-yu-ben-ti-shi-npwan-quan-wen-ti-de-zheng-ming/)
本题答案的可视化: http://int-e.eu/~bf3/squares/view.html
"""
    def tilingRectangle(self, n: int, m: int) -> int:
        grid = [[False] * m for _ in range(n)]
        ans = n*m
        def f(x,y, cur):
            nonlocal ans
            # 终止条件
            if x==n: ans = min(ans,cur); return
            # 剪枝
            if cur>=ans: return
            # 遍历下一行
            if y==m: f(x+1,0,cur); return
            # 已经填充了
            if grid[x][y]: f(x,y+1,cur); return
            
            # 主体部分: 尝试在 (x,y) 填入 mx, mx-1, ... 1 的正方形
            mx = 1  # 可填充的最大正方边长
            while x+mx<n and y+mx<m and grid[x][y+mx]==False:
                mx += 1
            for i in range(mx):
                for j in range(mx):
                    grid[x+i][y+j] = True
            f(x,y+mx,cur+1)
            for d in range(mx-1,-1,-1):     # 填入更小的正方形. 注意要遍历到 0! 也即删除当前填充的正方形
                for i in range(d+1):
                    grid[x+i][y+d] = False
                    grid[x+d][y+i] = False
                if d==0: return     # 不填入! 回溯的时候删除影响.
                f(x,y+d,cur+1)
        f(0,0,0)
        return ans
    
sol = Solution()
result = [
    # sol.circularPermutation(3,2),
    # sol.maxLength(arr = ["un","iq","ue"]),
    # sol.maxLength(["cha","r","act","ers"]),
    # sol.tilingRectangle(n = 2, m = 3),
    # sol.tilingRectangle(n = 5, m = 8),
    sol.tilingRectangle(n = 11, m = 13),
    sol.tilingRectangle(16,17),
]
for r in result:
    print(r)
