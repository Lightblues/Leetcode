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
https://leetcode.cn/contest/weekly-contest-401

TODO: 
Easonsi @2023 """
class Solution:
    """ 3178. 找出 K 秒后拿着球的孩子 """
    def numberOfChild(self, n: int, k: int) -> int:
        k = k % (2*(n-1))
        if k < n-1: return k
        return 2*n-2-k
    
    """ 3179. K 秒后第 N 个元素的值 """
    def valueAfterKSeconds(self, n: int, k: int) -> int:
        mod = 10**9 + 7
        arr = [1] * n
        for i in range(k):
            for j in range(1, n):
                arr[j] = (arr[j-1] + arr[j]) % mod
        return arr[n-1]
    
    """ 3180. 执行操作可获得的最大总奖励 I #medium 从一个数组中依次取数字, 要求累积和 > 当前数字, 问可得到的最大数字
限制: n, x 2e3
思路0: 
    """
    def maxTotalReward(self, rewardValues: List[int]) -> int:
        from sortedcontainers import SortedList
        rewardValues = list(set(rewardValues))
        rewardValues.sort()
        _max = 2 * rewardValues[-1]
        sl = SortedList()
        for x in rewardValues:
            news = set()
            for i in sl:
                if i >= x: break
                if (i+x not in news) and (i+x < _max): 
                    news.add(i+x)
            for i in news: sl.add(i)
            if x not in sl: sl.add(x)
        return sl[-1]
        
    
sol = Solution()
result = [
    # sol.numberOfChild(n = 3, k = 5),
    # sol.valueAfterKSeconds(n = 4, k = 5),
    sol.maxTotalReward(rewardValues = [1,1,3,3]),
]
for r in result:
    print(r)
