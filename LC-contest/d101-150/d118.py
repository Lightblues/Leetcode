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
https://leetcode-cn.com/contest/biweekly-contest-118
https://leetcode.cn/circle/discuss/PScw7D/

T4 好难orz, 有时间回来做一下! TODO

Easonsi @2023 """
class Solution:
    """ 2942. 查找包含给定字符的单词 """
    
    """ 2943. 最大化网格图中正方形空洞的面积 """
    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        # 找到 hBars 中最多连续出现的数量
        hBars.sort()
        h_mx = 1; acc = 1
        for i,x in enumerate(hBars):
            if i>0 and x==hBars[i-1]+1:
                acc += 1
                h_mx = max(h_mx, acc)
            else:
                acc = 1
        vBars.sort()
        v_mx = 1; acc = 1
        for i,x in enumerate(vBars):
            if i>0 and x==vBars[i-1]+1:
                acc += 1
                v_mx = max(v_mx, acc)
            else: acc = 1
        return (min(h_mx, v_mx)+1)**2
        
    """ 2944. 购买水果需要的最少金币数
思路1: #DP
    记 f[i] 表示买前i个所需的最小金币数. 则有
    f[i] = min{ f[idx-1] + prices[idx] }, 其中idx要满足条件 idx+idx >= i
    """
    def minimumCoins(self, prices: List[int]) -> int:
        n = len(prices)
        f = [inf] * (n+1)
        prices = [0] + prices   # 对齐下标
        f[1] = prices[1]; f[0] = 0  # 注意 f[0] 也要初始化
        for i in range(2, n+1):
            for idx in range(i, 0, -1):
                if idx+idx >= i:
                    f[i] = min(f[i], f[idx-1]+prices[idx])
                else: break
        return f[n]

    """ 2945. 找到最大非递减数组的长度 #hard 对于一个数组, 每次可以选择一个自数组, 将其替换为它的和; 需要将其构建为非递减数组; 问最大长度
限制: N 1e5
思路0: WA
    试图贪心: 每次出发往后匹配 —— 但有问题: 例如 [4 3 8 9] 的例子, 应该把前两个合起来! 
思路1: #TODO
[灵神](https://leetcode.cn/problems/find-maximum-non-decreasing-array-length/solutions/2542102/dan-diao-dui-lie-you-hua-dp-by-endlessch-j5qd/)
    """
    def findMaximumLength(self, nums: List[int]) -> int:
        # 思路0: WA
        n = len(nums)
        pre = nums[0]; cnt = 1
        idx = 1; acc = 0
        while idx < n:
            while idx<n and acc<pre:
                acc += nums[idx]
                idx += 1
            if acc >= pre:
                cnt += 1
                pre = acc
                acc = 0
        return cnt


sol = Solution()
result = [
    # sol.maximizeSquareHoleArea(n = 2, m = 1, hBars = [2,3], vBars = [2]),
    # sol.maximizeSquareHoleArea(n = 2, m = 3, hBars = [2,3], vBars = [2,3,4]),
    # sol.minimumCoins(prices = [3,1,2]),
    # sol.minimumCoins(prices = [1,10,1,1]),
    sol.findMaximumLength(nums = [5,2,2]),
    sol.findMaximumLength(nums = [1,2,3,4]),
    sol.findMaximumLength(nums = [4,3,2,6]),
]
for r in result:
    print(r)
