import enum
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
https://leetcode.cn/contest/biweekly-contest-134
T4 关联 logTrick! AND/OR 具有的性质
[灵神题单](https://leetcode.cn/discuss/post/3580371/fen-xiang-gun-ti-dan-wei-yun-suan-ji-chu-nth4/)
Easonsi @2025 """
class Solution:
    """ 3206. 交替组 I #easy 对于一个环, 计算长度为3的间隔区间的数量 """
    def numberOfAlternatingGroups(self, colors: List[int]) -> int:
        k = 3
        n = len(colors)
        colors += colors[:k-1]
        ans = 0
        for i in range(n):
            if colors[i] != colors[i+1] and colors[i+1] != colors[i+2]:
                ans += 1
        return ans
    
    """ 3207. 与敌人战斗后的最大分数 题目比较复杂, 见网页 """
    def maximumPoints(self, enemyEnergies: List[int], currentEnergy: int) -> int:
        mn = min(enemyEnergies)
        if currentEnergy < mn: return 0
        currentEnergy += sum(enemyEnergies) - mn
        return currentEnergy // mn
    
    """ 3208. 交替组 II #medium #medium 对于一个环, 计算长度为k的间隔区间的数量
限制: n 1e5
思路1: 维护一个符合条件的最右侧的指针
    """
    def numberOfAlternatingGroups(self, colors: List[int], k: int) -> int:
        colors += colors[:k-1]
        def get_first_alternate_k(idx):
            i = idx; l = 1
            while l < k:
                if i >= len(colors) - 1: return -1
                if colors[i] != colors[i+1]:
                    i += 1
                    l += 1
                else:
                    i += 1
                    l = 1
            return i
        i = 0
        ans = 0
        while i < len(colors)-1 and i!=-1:
            if i!=0 and colors[i] != colors[i+1]:
                i += 1
                ans += 1
            else:
                i = get_first_alternate_k(i)
                if i != -1: ans += 1
        return ans


    """ 3209. 子数组按位与值为 K 的数目 #hard 问一个数组的子数组中, 多少个子数组的按位与等于k
限制: n 1e5, x 1e9
思路1: 前缀AND + 二分查找. #logTrick
    从左往右遍历i, 考虑后缀数组 [0...i], [1...i], ...[i] 的AND, 是一个递增数组! 
        考虑一个新的 x=nums[i], 从右往左更新的时候, 若 ands[j]&x == ands[j], 说明前序都不会更新了! 结束内层循环!
        复杂度: O(n log(C)) 因为每个位置最多被更新log(C)次
    如何计算等于k的数量? 直接二分查找
        除此之外, 因为ands元素的更新是递减的, 可以避免二分, 采用 三指针, 或者 "维护等于 k 的子数组个数"
[ling](https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/solutions/2833497/jian-ji-xie-fa-o1-kong-jian-pythonjavacg-u7fv/)
    """
    def countSubarrays(self, nums: List[int], k: int) -> int:
        ands = []
        ans = 0
        for i,x in enumerate(nums):
            ands.append(x)
            for j in range(i-1, -1, -1):
                if ands[j]&x == ands[j]: break
                ands[j] &= x
            ans += bisect_right(ands, k) - bisect_left(ands, k)
        return ans
    
sol = Solution()
result = [
    # sol.numberOfAlternatingGroups(colors = [0,1,0,0,1]),
    # sol.maximumPoints(enemyEnergies = [3,2,2], currentEnergy = 2),

    # sol.numberOfAlternatingGroups(colors = [0,1,0,1,0], k = 3),
    # sol.numberOfAlternatingGroups(colors = [0,1,0,0,1,0,1], k = 6),
    # sol.numberOfAlternatingGroups([0,1,0,0,1], 3),

    sol.countSubarrays(nums = [1,1,1], k = 1),
    sol.countSubarrays(nums = [1,1,2], k = 1),
]
for r in result:
    print(r)
