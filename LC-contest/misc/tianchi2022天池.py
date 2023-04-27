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
https://leetcode.cn/contest/tianchi2022/
[灵神](https://www.bilibili.com/video/BV1ne4y177wN/)

T3 需要一定的思维量, 大胆贪心. 
Orz T4好难, 但确实值得思考, 需要加强一下 #背包 问题. 

@2022 """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    """ 221021天池-01. 统计链表奇数节点 """
    
    """ 221021天池-02. 光线反射 #medium 给定一个grid放置一些镜子, 从左上角射出一条光线, 求光线最终离开时刻经过的路径长度. 限制: m,n 100
思路1: 暴力 #模拟 即可
"""
    def getLength(self, grid: List[str]) -> int:
        m,n = len(grid), len(grid[0])
        # 0,1,2,3 分别从 上、右、下、左开始
        d2diff = [(1,0), (0,-1), (-1,0), (0,1)]
        # 实际上, 下面的转换矩阵可以通过 #异或 操作来实现: 分别 ^3, ^1
        # 原因? 因为反射关系两两一组
        chL = [3, 2, 1, 0]    # 经过主对角线反射结果
        chR = [1, 0, 3, 2]    # 经过副对角线反射结果
        cnt = 0
        def f(i,j, direction):
            nonlocal cnt
            if not (0<=i<m and 0<=j<n): return
            cnt += 1
            if grid[i][j] == '.':
                dx,dy = d2diff[direction]
                return f(i+dx, j+dy, direction)
            elif grid[i][j]=='L':
                dir = chL[direction]
                dx,dy = d2diff[dir]
                return f(i+dx, j+dy, dir)
            else:
                dir = chR[direction]
                dx,dy = d2diff[dir]
                return f(i+dx, j+dy, dir)
        f(0,0,0)
        return cnt
    
    """ 221021天池-03. 整理书架 #medium 有一列书, 要求取出数量最少的书, 使得相同编号的书的数量至多为 limit. 求所有方案中, 剩余书的排列最小的一个. 限制: n 1e5. limit 10. 
思路1: 遇到字典序考虑 #贪心. 顺序用 #栈 来记录当前的选择. 并控制数量限制. 
    具体而言, 每个数字可以pop的数量是有限制的, 我们用ava字典来记录. 若达到了限制则只能push进栈. 
    还需要保证栈内出现次数不超过limit, 可以用一个cnt字典记录当前栈内该元素数量. 
"""
    def arrangeBookshelf(self, order: List[int], limit: int) -> List[int]:
        cnt = Counter(order)
        # 可以不用的数字 (pop) 的数量
        ava = defaultdict(int)
        for k,v in cnt.items():
            if v>limit: ava[k] = v-limit
        s = []
        cnt = defaultdict(int)  # 当前栈内该元素数量. 
        for a in order:
            # 栈内元素数量限制
            if cnt[a]>=limit: 
                ava[a] -= 1
                continue
            while s and s[-1]>a and ava[s[-1]]>0:
                ava[s[-1]] -= 1
                cnt[s[-1]] -= 1
                s.pop()
            s.append(a)
            cnt[a] += 1
        return s
    
    """ 221021天池-04. 意外惊喜 #hard #hardhard #review (同hulu的笔试题) 给定一组非递减数组, 只能顺序得到同一数组中的元素, 在一共limit次机会的限制, 问最大分数. 限制: m 2e3; n 1e3. limit 1000
关键提示: 没有选完的数组至多有一个. 
    也即, 不可能出现, 有两个数组都只选了一部分的情况!
思路1: #分治 
    基本思路是, 枚举所有的没有选完的数组, 其他的数组要么选完, 要么不选. 因此其他的可以转为01背包问题.
    复杂度: 枚举每个物品, 然后每个01背包 O(n*limit), 因此总体 O(n^2 * limit) 会超. 
    优化: 这些01背包会有一些重复的运算. 
        思路是 #分治 
    复杂度: 基于 #归并 排序, 多了一个 O(limit) 的循环, 因此是 O(limit * nlogn). 
    见 [灵神](https://www.bilibili.com/video/BV1ne4y177wN/)
关联: 2218. 从栈中取出 K 个硬币的最大面值和 #hard
    为什么不能用该题的代码了? 因为复杂度不够了!
    上题没有数字递增的性质. 
https://oi-wiki.org/dp/knapsack/
"""
    def brilliantSurprise(self, present: List[List[int]], limit: int) -> int:
        dp = [0] * (limit+1)    # 空间压缩, dp[j] 表示体积限制为 j 的最大价值.
        ans = 0
        
        def f(a, total):
            nonlocal dp, ans
            if len(a) == 1:
                # 它就是那个没有选完的数组
                # 假设其他的01背包都算好了, 枚举选择的前缀的长度.
                s = 0
                for i,x in enumerate(a[0]):
                    if i >= limit: break
                    s += x
                    # 选取前i个元素, 01背包用容量为limit-(i+1)的背包
                    ans = max(ans, s+dp[limit-i-1])
            else:
                # 分治
                tmp = dp.copy() # 记录原本的 DP数组
                m = len(a)//2
                left, right = a[:m], a[m:]
                
                # 计算左侧 01背包
                for i,row in enumerate(left):
                    for j in range(limit, len(row)-1, -1):  # 倒序遍历
                        # 基本01背包的递推公式! 这里的 len(row)理解为体积, total[i]理解为价值
                        dp[j] = max(dp[j], dp[j-len(row)]+total[i])
                # 带着这个左侧计算好的 01背包DP, 递归右半部分. 
                f(right, total[m:])
                
                # 计算右侧 01背包
                dp = tmp    # 还原 DP数组
                for i,row in enumerate(right, m):
                    for j in range(limit, len(row)-1, -1):  # 倒序遍历
                        # 基本01背包的递推公式! 这里的 len(row)理解为体积, total[i]理解为价值
                        dp[j] = max(dp[j], dp[j-len(row)]+total[i])
                f(left, total[:m])
                
        
        total = [sum(i) for i in present]
        f(present, total)
        return ans
    
sol = Solution()
result = [
    # sol.getLength(grid = ["...","L.L","RR.","L.R"]),
    # sol.getLength(grid = ["R.",".."]), 
    # sol.arrangeBookshelf(order = [5,5,6,5], limit = 2),
    # sol.arrangeBookshelf(order = [3,3,9,8,9,2,8], limit = 1),
    # sol.arrangeBookshelf(order = [2,1,2,2,1,3,3,1,3,3], limit = 2),
    # sol.arrangeBookshelf([2,2,1,2,2], 3), 
    # sol.arrangeBookshelf([10,4,12,1,6,10,1,10,2,10,10,7], 1), 
    
    sol.brilliantSurprise(present = [[1,2],[2,3],[3,4]], limit = 3),
    sol.brilliantSurprise(present = [[1,2,100],[4,5],[3,4]], limit = 4), 
]
for r in result:
    print(r)
