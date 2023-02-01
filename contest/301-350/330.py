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
https://leetcode.cn/contest/weekly-contest-330
灵神: https://www.bilibili.com/video/BV1mD4y1E7QK/

T3 想出来了转换; T4 好难没做出来, 但其实题型比较经典了. 
Easonsi @2023 """
class Solution:
    """ 6337. 统计桌面上的不同数字 """
    def distinctIntegers(self, n: int) -> int:
        return n-1 if n!=1 else 1
    """ 6338. 猴子碰撞的方法数 注意数据范围在 1e9! 必须用pow """
    def monkeyMove(self, n: int) -> int:
        mod = 10**9 + 7
        return (pow(2,n, mod)-2) % mod
    
    """ 6339. 将珠子放入背包中 #hard 要将一个weight数组表示的珠子放入k个背包, 要求背包中的珠子是连续的 (子数组)
定义放入 [i,j] 数组的背包分数位 weights[i] + weights[j]. 对于一种分配, 总分数为所有背包分数之和, 问最大最小差值. 限制: k,n 1e5
思路1: #转换
    等价于在数组中插入 k-1 个分割点; 每一个分割点两侧会被计入得分  (两个边界总会被计入, 可以看作第k个分割, 不影响答案)
    因此, 可以定义位置为i的分割点得分为 weights[i] + weights[i+1]
    因此, 问题等价于在这些中找 k-1 个; 为求最大差值, 排序即可.
"""
    def putMarbles(self, weights: List[int], k: int) -> int:
        if k==1: return 0
        ws = []
        for i in range(1,len(weights)):
            ws.append(weights[i] + weights[i-1])
        ws.sort()
        k-=1
        return sum(ws[-k:])-sum(ws[:k])

    """ 6340. 统计上升四元组 #hard 对于有序的坐标 (i,j,k,l), 若 nums[i] < nums[k] < nums[j] < nums[l] 则是有序的四元组
注意, 是 1324的结构. 对于一个 [1...n]的排列, 求四元组数量. 限制: n 4000
思路1: 枚举中间两个数 j,k 
    这样, 我们需要知道 在1...j-1 范围内比 nums[k] 小的数; 在 k+1...n 范围内比 nums[j] 大的数
    因此, 我们用 
        great[k][x] 记录在k右边的比x大的数量
        less[j][x] 记录在j左边的比x小的数量
    复杂度: O(n^2)  但是常数较大
    [灵神](https://leetcode.cn/problems/count-increasing-quadruplets/solution/you-ji-qiao-de-mei-ju-yu-chu-li-pythonja-exja/)
思路2: 两次遍历, 重点记录 132 形式的数量. 非常精彩 更直观的思路? 但 #hard
    外层枚举四元组最后的l (要求是最大的). 用一个cnt数组来记录 cnt[j] 是以j为中心的 132 形式数量
    内层枚举j. 并且在遍历过程中更新 cnt和答案! 
    具体见代码. 复杂度也是 O(n^2)
    见 [here](https://leetcode.cn/problems/count-increasing-quadruplets/solution/by-destiny-god-4qc6/)
"""
    def countQuadruplets(self, nums: List[int]) -> int:
        n = len(nums)
        # great[k][x] 记录在k右边的比x大的数量
        great = [None] * n
        great[-1] = [0] * (n+1) # [1...n] 的排列
        for k in range(n-2,-1,-1):
            great[k] = great[k+1][:]
            for x in range(1,nums[k+1]):
                great[k][x] += 1
        # less[j][x] 记录在j左边的比x小的数量
        less = [None]*n
        less[0] = [0] * (n+1) # [1...n] 的排列
        for j in range(1,n):
            less[j] = less[j-1][:]
            for x in range(nums[j-1]+1,n+1):
                less[j][x] += 1
        # 
        ans = 0
        for j in range(1,n-2):
            for k in range(j+1,n-1):
                if nums[j] > nums[k]:
                    ans += less[j][nums[k]] * great[k][nums[j]]
        return ans
    
    def countQuadruplets(self, nums: List[int]) -> int:
        # 思路2: 两次遍历, 重点记录 132 形式的数量. 非常精彩
        n = len(nums)
        ans = 0
        cnt = [0] * n   # 统计以 j 为 “中间“ 的、类似132顺序的三元组的个数
        for l in range(n):  # 枚举四元组最后一个元素
            lessL = 0       # 统计比 nums[l] 小的元素
            for j in range(l):
                if nums[j]<nums[l]: # l 可以是最后一个元素. (此时l无法作为132中的2)
                    ans += cnt[j]
                    lessL += 1
                else:               # l 不可以是最后一个元素. (此时l可以作为132中的2, 累计到j位置)
                    cnt[j] += lessL
        return ans

    
import random
random.seed(22)
arr = list(range(4000))
random.shuffle(arr)
sol = Solution()
result = [
    # sol.putMarbles(weights = [1,3,5,1], k = 2),
    # sol.putMarbles(weights = [1, 3], k = 2),
    # sol.putMarbles([1,4,2,5,2],3),
    # sol.putMarbles([25,74,16,51,12,48,15,5],1),
    # sol.monkeyMove(3),
    # sol.monkeyMove(4),
    # sol.monkeyMove(10**9),
    sol.countQuadruplets([1,2,3,4]),
    sol.countQuadruplets([1,3,2,4,5]),
    # sol.countQuadruplets(arr),
]
for r in result:
    print(r)
