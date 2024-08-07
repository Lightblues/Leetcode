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
https://leetcode.cn/contest/weekly-contest-402
T4 复习了树状数组!
Easonsi @2023 """

class Fenwick:
    """ 树状数组! 用于求支持更新的区间和!!
    NOTE: 树状数组的下标从 1 开始! 
    """
    __slots__ = 'f'

    def __init__(self, n: int):
        self.f = [0] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.f):
            self.f[i] += val
            i += i & -i

    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.f[i]
            i &= i - 1
        return res

    def query(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.pre(r) - self.pre(l - 1)


class Solution:
    """ 3184. 构成整天的下标对数目 I """
    """ 3185. 构成整天的下标对数目 II """
    def countCompleteDayPairs(self, hours: List[int]) -> int:
        cnt = Counter(i%24 for i in hours)
        ans = math.comb(cnt[0], 2) + math.comb(cnt[12], 2)
        for i in range(1,12):
            ans += cnt[i]*cnt[24-i]
        return ans
    
    """ 3186. 施咒的最大总伤害 """
    def maximumTotalDamage(self, power: List[int]) -> int:
        cnt = Counter(power)
        arr = sorted(cnt.items(), key=lambda x:x[0])
        n = len(arr)
        if n==1: return arr[0][0] * arr[0][1]
        f = [0] * n
        f[0] = arr[0][0] * arr[0][1]
        f[1] = arr[1][0] * arr[1][1] + (0 if arr[1][0]<=arr[0][0]+2 else f[0])
        max_pre = 0     # 下面写的有点脏
        for i in range(2,n):
            v = arr[i][0] * arr[i][1]
            if arr[i][0] > arr[i-1][0]+2:
                v += max(f[i-1], f[i-2], max_pre)
            elif arr[i][0] > arr[i-2][0]+2:
                v += max(f[i-2], max_pre)
            else:
                v += max_pre
            f[i] = v
            max_pre = max(max_pre, f[i-2])
        return max(f)
    
    """ 3187. 数组中的峰值 #hard 定义峰值元素, 支持查询 [l,r] 范围峰值元素数量, 以及修改 nums[i]=x 的操作
    非常经典的 #树状数组 的题目! 复习一下!!!
[ling](https://leetcode.cn/problems/peaks-in-array/solutions/2812394/shu-zhuang-shu-zu-pythonjavacgo-by-endle-tj0w/)
    """
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        fenwick = Fenwick(n-1)      # 可能出现的位置是 [1, n-2]
        
        for i in range(1, n-1):
            if nums[i] > nums[i-1] and nums[i] > nums[i+1]:
                fenwick.update(i, 1)
        
        ans = []
        for op, a,b in queries:
            if op == 1:
                ans.append(fenwick.query(a+1,b-1))  # NOTE: 边界上的不能算! 
            else:
                l,r = max(1,a-1), min(n-2,a+1)
                for i in range(l,r+1):
                    if nums[i] > nums[i-1] and nums[i] > nums[i+1]:
                        fenwick.update(i, -1)
                nums[a] = b
                for i in range(l,r+1):
                    if nums[i] > nums[i-1] and nums[i] > nums[i+1]:
                        fenwick.update(i, 1)
        return ans
    
sol = Solution()
result = [
    # sol.countCompleteDayPairs(hours = [72,48,24,3]),
    # sol.countCompleteDayPairs(hours = [12,12,30,24,24]),
    # sol.maximumTotalDamage(power = [7,1,6,6]),
    # sol.maximumTotalDamage(power = [1,1,3,4]),
    # sol.maximumTotalDamage([5,9,2,10,2,7,10,9,3,8]),
    sol.countOfPeaks(nums = [4,1,4,2,1,5], queries = [[2,2,4],[1,0,2],[1,0,4]]),
    sol.countOfPeaks([7,6,3,9,6,10,7],[[2,6,1],[1,2,4],[2,3,1],[1,2,4]]),
]
for r in result:
    print(r)
