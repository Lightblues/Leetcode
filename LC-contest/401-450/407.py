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
https://leetcode.cn/contest/weekly-contest-407
T4 差分数组! 
Easonsi @2023 """
class Solution:
    """ 3226. 使两个整数相等的位更改次数 """
    def minChanges(self, n: int, k: int) -> int:
        if n | k != n: return -1
        return (n-k).bit_count()
    
    """ 3227. 字符串元音游戏 """
    def doesAliceWin(self, s: str) -> bool:
        n = len(s)
        c = sum(i in 'aeiou' for i in s)
        return c>0
    
    """ 3228. 将 1 移动到末尾的最大操作次数 """
    def maxOperations(self, s: str) -> int:
        ans = 0
        acc = 0
        pre = '1'
        for c in s + '1':   # note to add dummy!
            if c=='1':
                if pre=='0': ans += acc
                acc += 1
            pre = c
        return ans
    
    """ 3229. 使数组等于目标数组所需的最少操作次数 #hard #题型 给定两个数组 x,y, 每次可以选择一个子数组将整体 +/-1, 问使得他们相等的最小操作次数. 
限制: n 1e5; x 1e8
思路1: 数组 #差分数组
    问题等价于, 对于 x-y, 将该数组变成一个全0数组! 
    区间操作可以转化为差分数组上两个数字的加减! 
        这里用到的是完整的差分数组. 对于长度为n的数组 arr, 其差分数组为 d = [arr[0], arr[1]-arr[0], arr[2]-arr[1], ..., -arr[n-1]], 长度为 n+1
        差分数组有性质: 对于 arr[i...j] 的 +k 操作, 等价于在差分数组上将 d[i] 加上 k, d[j+1] 减去 k
        前后可以理解成哨兵, 开头的 d[0]=arr[0] 保证了前缀和 = arr[i]; 结尾的 d[n]=arr[n-1] 保证了 sum(d)=0
    因此, 本题中的一次操作对应了d上的一个数字 +1, 一个 -1. 目标是将d变为全0! 又因为 sum(d)=0, 只需要计算d中的正数之和即可! 
[ling](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-to-target/)
差分题库: https://leetcode.cn/problems/car-pooling/solutions/2550264/suan-fa-xiao-ke-tang-chai-fen-shu-zu-fu-9d4ra/
思路2: 一个更 "低级" 的解法
    同样, 求差分数组, 但是没有最后一位. 
    现在, 同样需要将差分数组 d 变为全0. 注意! 区别于思路1中的差分数组定义, 这里对于数组区间操作可以转换为差分数组上两个位置的 +1/-1, 或者是一个位置的 +1/-1 (后缀区间)
    我们从左到右遍历, 假设当前的数字为 x, 此前进行的+1操作有 s 次 (这意味着最多有s次 "免费" 的-1操作). 分类讨论
        x >= 0, s >= 0: 需要增加x次+1操作, 同时 s+=x
        x >= 0, s < 0: (此前多了-s次 -1操作)
            若 x > -s: 需要额外的 x-(-s)次+1操作 =x+s; 同时 s <- s+x
            若 x < -s: 不需要额外操作 =0; 同时 s <- s+x
            可以合并为需要操作 max(0, x+s) 次+1操作
        x < 0, s < 0: 需要增加 |x| 次-1操作, 同时 s+=x
        x < 0, s >= 0: 
            类似上面的讨论, 需要额外的 max{(-x)-s, 0} 次-1操作
    --> 发现永远 s += x ! 同时内部逻辑似乎可以被解法一优雅地解释! 
"""
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        arr = [t-x for t,x in zip(target,nums)]
        diff = [arr[0]] + [y-x for x,y in itertools.pairwise(arr)] + [-arr[-1]] # 一个完整的差分数组, 结尾是 -a[-1]. 这样保证了 sum(diff) = 0
        ops = sum(i for i in diff if i>0)
        return ops
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        arr = [t-x for t,x in zip(target,nums)]
        diff = [arr[0]] + [y-x for x,y in itertools.pairwise(arr)] # 这里没有
        s = diff[0]
        ans = abs(s)        # NOTE: 这里应该是 abs!
        for i in range(1, len(diff)):
            x = diff[i]
            if x>=0:
                if s>=0: ans += x
                else: ans += max(0, x+s)
            else:
                if s <= 0: ans += -x
                else: ans += max(0, -x-s)
            s += x
        return ans


sol = Solution()
result = [
    # sol.minChanges(n = 13, k = 4),
    # sol.maxOperations(s = "1001101"),
    # sol.maxOperations("110"),
    sol.minimumOperations( nums = [3,5,1,2], target = [4,6,2,4]),
    sol.minimumOperations([4,4,1,1,2,5,5,1,1], [3,2,3,4,5,2,3,3,4]),
]
for r in result:
    print(r)
