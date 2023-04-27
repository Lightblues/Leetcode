from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-200
@2022 """
class Solution:
    """ 1534. 统计好三元组 """
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        n = len(arr)
        ans = 0
        for i in range(n):
            for j in range(i+1,n):
                if abs(arr[i]-arr[j]) > a: continue
                for k in range(j+1,n):
                    if abs(arr[j]-arr[k]) <= b and abs(arr[k]-arr[i]) <= c: ans += 1
        return ans
    """ 1535. 找出数组游戏的赢家 """
    def getWinner(self, arr: List[int], k: int) -> int:
        # 注意k可能很大, 而需要当前数组最大值时, 必然会被永远保留
        mxx = max(arr)
        mx = max(arr[:2]); acc = 1
        if k==1: return mx
        q = deque(arr[2:])
        while True:
            if a==mxx: return a
            a = q.popleft()
            if a>mx:
                q.append(mx)
                mx = a; acc = 1
            else: 
                q.append(a)
                acc += 1
                if acc==k: return mx
    
    """ 1536. 排布二进制网格的最少交换次数 #medium #题型 #冒泡
通过相邻行交换将一个01方针变为下三角阵. 问最少交换次数. 限制: 矩阵长 200.
思路0: 一开始想, 每一行对于最后0的数量有约束, 例如最后只有1个零的行只能放在最后两排. 因此对于每一行中后缀零的数量计数, 然后转为逆序. 但实际上, 最后并不需要逆序! 因为题目的要求只需要满足下三角即可.
思路1: 更简单的思路是 #贪心. 从上往下来找第一个满足第i行的, 将其交换到第i行即可. (类似 #冒泡 排序). 这样, 复杂度为 O(n^2)
    细节: 如何找到贪心的交换行? 直接模拟冒泡排序即可, 注意下面代码的写法 (并不复杂)
    见 [official](https://leetcode.cn/problems/minimum-swaps-to-arrange-a-binary-grid/solution/pai-bu-er-jin-zhi-wang-ge-de-zui-shao-jiao-huan-ci/).
"""
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)
        nonZeros = [0]*n
        for i in range(n):
            for j in range(n-1,-1,-1):
                if grid[i][j] != 0:
                    nonZeros[i] = j; break
        # 每次贪心找第一个符合条件的
        ans = 0
        for i in range(n):
            # 前面非零的部分最多有 i 个 (从0开始)
            t = -1
            for j in range(i,n):
                if nonZeros[j]<=i: 
                    t = j; break
            if t==-1: return -1     # 不符合要求
            ans += t-i
            # note: 模拟交换
            for k in range(t,i,-1):
                nonZeros[k],nonZeros[k-1] = nonZeros[k-1],nonZeros[k]
        return ans
    
    """ 1537. 最大得分 #hard
有两个严格递增的序列AB, 我们要得到一个从左到右的序列, 对于AB中共同出现的数字位置可以进行「交叉」. 路径的得分为所有元素之和, 注意相等元素只记一次, 问最大的分. 限制: 长度 1e5
思路1: 最两个序列, 找到所有的交叉点, 对于每两个点之间的段落取较大值.
思路2: 用两个值来记录AB序列中到目前为止的最大值. #双指针 进行遍历, 遇到交叉点的时候两个值发生交互. 如何维护双指针? 尽量保持指向的值相等. 见 [官答](https://leetcode.cn/problems/get-the-maximum-score/solution/zui-da-de-fen-by-leetcode-solution/).
"""
    def maxSum(self, nums1: List[int], nums2: List[int]) -> int:
        mod = 10**9+7
        m,n = len(nums1),len(nums2)
        # acc 便于计算区间和
        acc1, acc2 = list(accumulate(nums1, initial=0)), list(accumulate(nums2, initial=0))
        # 找到所有交叉点
        m1 = {nums1[i]:i for i in range(m)}
        m2 = {nums2[i]:i for i in range(n) if nums2[i] in m1}
        # 边界: 没交叉点
        if len(m2)==0: return max(sum(nums1), sum(nums2))
        splits = sorted(m2.keys())
        ans = sum(splits)       # 所有交叉点得分; 下面的片段不计边界分数.
        # 遍历所有交叉点之间的片段, 取AB中的较大值.
        s,e = splits[0],splits[-1]
        ans += max(acc1[m1[s]], acc2[m2[s]]) + max(acc1[-1]-acc1[m1[e]+1], acc2[-1]-acc2[m2[e]+1])
        for i in range(1, len(splits)):
            s,e = splits[i-1],splits[i]
            ans += max(acc1[m1[e]]-acc1[m1[s]+1], acc2[m2[e]]-acc2[m2[s]+1])
        return ans % mod
    
sol = Solution()
result = [
    # sol.getWinner(arr = [2,1,3,5,4,6,7], k = 2),
    sol.minSwaps(grid = [[0,0,1],[1,1,0],[1,0,0]]),
    # sol.maxSum(nums1 = [2,4,5,8,10], nums2 = [4,6,8,9]),
]
for r in result:
    print(r)
