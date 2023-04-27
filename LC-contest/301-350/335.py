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
https://leetcode.cn/contest/weekly-contest-335
Easonsi @2023 """

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 6307. 递枕头 """
    def passThePillow(self, n: int, time: int) -> int:
        time = time % (2*n-2)
        if time<=n-1:
            return time+1
        else:
            return 2*n-1-time
    
    """ 二叉树中的第 K 大层和 """
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        ss = []
        q = [root]
        while q:
            s = 0
            nq = []
            for node in q:
                s += node.val
                if node.left: nq.append(node.left)
                if node.right: nq.append(node.right)
            ss.append(s)
            q = nq
        ss.sort(reverse=True)
        return ss[k-1] if k<=len(ss) else -1

    """ 6309. 分割数组使乘积互质 #medium #题型 #因子 要求对一个数组在某点分割, 使得前后两个数组中没有相同的质因子. 求所有有效的位置的最小位置. 
限制: 元素大小 1e4; n 1e4
思路1: 先对所有数字因子分解; 拓展「分组边界」
    例如对于示例 [4,7,8,15,3,5], 将其转为因子 [2,7,2,3/5,3,5]. 显然0位置是需要的, 我们找到所有包含2的位置, 更新右边界... 直到左侧数组中的因子是「自洽的」, 也即不出现在右侧. 
    具体见代码!
思路2: 类似 #跳跃游戏 
    对于每个质因子p, 它出现的边界定义了 [left, right] 区间!
    类似「0055. 跳跃游戏」, 从左端点出发, 求能够到达的最右位置. 
[灵神](https://leetcode.cn/problems/split-the-array-to-make-coprime-products/solution/ben-zhi-shi-tiao-yue-you-xi-by-endlessch-8chd/)
     """
    def findValidSplit(self, nums: List[int]) -> int:
        # @lru_cache(None)
        # def primes(x):
        #     # 分解得到x的所有质因数
        #     ps = []
        #     for i in range(2, x+1):
        #         if x%i==0:
        #             ps.append(i)
        #             x = x//i
        #             if x==1: break
        #     return ps
        # 快速对于一组数字进行因子分解
        @lru_cache(None)
        def primes(x):
            # 递归 @cache, 返回所有的因子 (可能出现 [2,2,3] 这种重复)
            if x==1: return []
            for i in range(2, int(sqrt(x))+1):
                if x%i==0:
                    return [i] + primes(x//i)
            return [x]
        # {prime: idxs}
        prime2idxs = defaultdict(set)
        for i,x in enumerate(nums):
            for p in primes(x):
                prime2idxs[p].add(i)
        
        visited = set() # 记录已经拓展过的因子
        mx = 0
        for i in range(len(nums)-1):
            # 需要检查primes
            todo = set(primes(nums[i])) - visited
            for p in todo:
                mx = max(mx, max(prime2idxs[p]))
                visited.add(p)
            # 边界: 左边「自洽」了
            if mx<=i: return i
        return -1

    def findValidSplit(self, nums: List[int]) -> int:
        left = {}  # left[p] 表示质数 p 首次出现的下标
        right = [-1] * len(nums)  # right[i] 表示左端点为 i 的区间的右端点的最大值

        def f(p: int, i: int) -> None:
            if p in left:
                right[left[p]] = i  # 记录左端点 l 对应的右端点的最大值
            else:
                left[p] = i  # 第一次遇到质数 p

        for i, x in enumerate(nums):
            d = 2
            while d * d <= x:  # 分解质因数
                if x % d == 0:
                    f(d, i)
                    x //= d
                    while x % d == 0:
                        x //= d
                d += 1
            if x > 1: f(x, i)

        max_r = 0
        for l, r in enumerate(right):
            if l > max_r:  # 最远可以遇到 max_r
                return max_r  # 也可以写 l-1
            max_r = max(max_r, r)
        return -1


    """ 6310. 获得分数的方法数 #hard 有一组题以 (cnt, mark) 的形式给出, 问总得分为 target 的可能情况. (注意, 例如m道相同类型的题目答对x道的情况, 只算一种, 不区分) 取模. 
限制: target 1e3; n 50; cnt,mark 50
思路1: #DP
    记 `f[t][i]` 表是用前i个物品可以得到t分的方法数, 则有递推
    `f[t][i] = sum{ f[t-mask_j*x][i-1] }` 这里求和所有满足 x>=0 and t-mask_j*x>=0 的情况.
    正确性: 这样是不会重复的!
    边界: f[0][0] = 1, 实际上 f[0][i] = 1 不过代码上可以整合到上面公式中
[灵神](https://leetcode.cn/problems/number-of-ways-to-earn-points/solution/fen-zu-bei-bao-pythonjavacgo-by-endlessc-ludl/)
    总结是 #分组背包 模板题
关联 「1981. 最小化目标值与所选元素的差」「2218. 从栈中取出 K 个硬币的最大面值和」
     """
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        mod = 10**9+7
        n = len(types)
        f = [[0]*(n+1) for _ in range(target+1)]
        f[0][0] = 1     # 边界
        # 注意这里需要 t==0, 因为要更新 f[0][i] = 1
        for t in range(target+1):
            for i in range(1, n+1):
                cnt, mark = types[i-1]
                for j in range(cnt+1):
                    if t-j*mark<0: break
                    f[t][i] += f[t-j*mark][i-1]
        return f[target][n] % mod


sol = Solution()
result = [
    # sol.passThePillow(3, 2),
    # sol.passThePillow(4,5),
    # sol.findValidSplit(nums = [4,7,8,15,3,5]),
    # sol.findValidSplit(nums = [4,7,15,8,3,5]),
    sol.waysToReachTarget(target = 6, types = [[6,1],[3,2],[2,3]]),
    sol.waysToReachTarget(target = 5, types = [[50,1],[50,2],[50,5]]),
]
for r in result:
    print(r)
