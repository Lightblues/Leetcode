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
https://leetcode-cn.com/contest/biweekly-contest-96
讨论: https://leetcode.cn/circle/discuss/33ZnsL/

Easonsi @2023 """
class Solution:
    """  """
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        j = set(nums1) & set(nums2)
        return -1 if len(j) == 0 else min(j)
    
    """ 6275. 使数组中所有元素相等的最小操作数 II #medium 给定两个长度相等的数组, 和一个整数k, 每次可以对于arr1[i],arr2[j] 分别+/-k, 问使得两数组相等的最小操作数. 
思路1: 遍历
"""
    def minOperations(self, nums1: List[int], nums2: List[int], k: int) -> int:
        diff = [a-b for a,b in zip(nums1, nums2)]
        # 注意边界!! 
        if k==0: return 0 if all(d==0 for d in diff) else -1
        pos = neg = 0
        for d in diff:
            if d>0:
                if d%k: return -1
                pos += d//k
            elif d<0:
                if (-d)%k: return -1
                neg += (-d)//k
        return pos if pos==neg else -1
    
    """ 6302. 最大子序列的分数 #medium #题型 对于两等长数组, 选择一组下标, 定义score为 `arr1中对应数字之和 * arr2中对应数字最小值`, 求最大分数. 限制: n 1e5
思路1: 对于arr2从大到小排序, 维护 arr1 中长度为k的最大元素. 
"""
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        # 对nums2从大到小排序
        vals = [(b,a) for a,b in zip(nums1, nums2)]
        vals.sort(reverse=True)
        # q 记录目前最大的k个数
        q = [i[1] for i in vals[:k]]; heapify(q)
        acc = sum(q)
        mx = vals[k-1][0] * acc
        # 遍历排序结果
        for a,new in vals[k:]:
            old = heappushpop(q, new)
            acc += new - old
            mx = max(mx, a * acc)
        return mx
    

    """ 6302. 最大子序列的分数 #hard 从 (1,1) 出发, 每次从 (x,y), 可以操作到 (x-y,y), (x,y-x), (2x,y), (x,2y), 问能否到达 (tx,ty)? 限制: [1,1e9]
下面是猜出来的. 
"""
    def isReachable(self, targetX: int, targetY: int) -> bool:
        x,y = sorted([targetX, targetY])
        # @lru_cache(None)
        # def dfs(x,y):
        #     if x
        g = math.gcd(x,y)
        while g%2==0: g//=2
        if g>1: return False
        return True
    
sol = Solution()
result = [
    # sol.getCommon(nums1 = [1,2,3,6], nums2 = [2,3,4,5]),
    # sol.minOperations(nums1 = [4,3,1,4], nums2 = [1,3,7,1], k = 3),
    # sol.minOperations(nums1 = [3,8,5,2], nums2 = [2,4,1,6], k = 1),
    # sol.maxScore(nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3),
    # sol.maxScore(nums1 = [4,2,3,1,1], nums2 = [7,5,10,9,6], k = 1),
    # sol.maxScore([2,1,14,12], [11,7,13,6], 3),
    sol.isReachable(6,9),
    sol.isReachable(4,7),
    sol.isReachable(5,8),
]
for r in result:
    print(r)
