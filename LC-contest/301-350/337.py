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
https://leetcode.cn/contest/weekly-contest-337
https://www.bilibili.com/video/BV1EL411C7YU/

WA了5次orz... T2没有考虑要从左上角开始; T3一开始想错了, 然后用的set一共WA了3次; T4不难结果手抖WA了一次...

Easonsi @2023 """
class Solution:
    """ 6319. 奇偶位数 """
    def evenOddBit(self, n: int) -> List[int]:
        s = bin(n)[2:][::-1]
        ans = [0,0]
        for i,x in enumerate(s):
            if x=='1':
                ans[(i)%2] += 1
        return ans
    
    """ 6322. 检查骑士巡视方案 """
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        # 注意有个坑! 要求开始在左上角
        if grid[0][0]!=0: return False
        n = len(grid)
        path = [(grid[i][j],i,j) for i in range(n) for j in range(n)]
        path.sort()
        for i in range(1, len(path)):
            dx,dy = abs(path[i][2]-path[i-1][2]), abs(path[i][1]-path[i-1][1])
            if sorted([dx,dy]) != [1,2]: return False
        return True
    
    """ 6352. 美丽子集的数目 #medium 对于所有的子集, 求「任意两个整数差不为k」的数量 
限制: 数组长度 n 20
思路0: 从所有的分空自数组中删去不符合要求的, #TLE 了!
    划分成不同的子集, 例如 对于k=1的情况, 将 [1,2, 5,6,7] 划分成 [1,2], [5,6,7] 两个序列; 对于每个序列, 统计其中无效的数量 (例如长度为3就是 2^1 + 2^0)
思路1: 直接暴力 #回溯 每次在回溯的过程中判断是否满足! 注意复杂度 2^20 大概是 1e6 级别的
    注意: 需要考虑非空! 
    注意! 回溯要比 #二进制枚举 的效率更高 (灵神)
    灵神指出是 #子集型回溯 见「0078. 子集」
[灵神](https://leetcode.cn/problems/the-number-of-beautiful-subsets/solution/tao-lu-zi-ji-xing-hui-su-pythonjavacgo-b-fcgs/)
     """
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        # 思路1: #回溯. 下面的path实现太慢了! 可以参考灵神用 list计数或者Counter! 
        n = len(nums)
        nums.sort()
        ans = 0
        path = []   # 注意可能有重复的元素! 因此不能用set
        def f(i,pre):
            nonlocal ans, path
            if i>=n: 
                ans += 1; return
            f(i+1,pre)
            if nums[i]-k not in path: 
                path.append(nums[i])
                f(i+1,nums[i])
                path.pop()
        f(0,-k)
        # 注意: 需要考虑非空
        return ans - 1

    """ 6321. 执行操作后的最大 MEX #medium 定义MEX是数组中没有出现的最小非负整数. 可以对数组中的任意数字进行 +/-value 操作, 问可能的最大MEX
思路1: 可知初始数字有用的只是 %value 因此直接计数, 然后for循环找到第一个不满足的即可
     """
    def findSmallestInteger(self, nums: List[int], value: int) -> int:
        nums = [x%value for x in nums]
        cnt = Counter(nums)
        for i in range(len(nums)+1):
            t = i%value
            if cnt[t]<=0: return i
            cnt[t] -= 1
    
sol = Solution()
result = [
    # sol.evenOddBit(17),
    # sol.evenOddBit(2),
    # sol.checkValidGrid(grid = [[0,11,16,5,20],[17,4,19,10,15],[12,1,8,21,6],[3,18,23,14,9],[24,13,2,7,22]]),
    # sol.checkValidGrid(grid = [[0,3,6],[5,8,1],[2,7,4]]),
    sol.beautifulSubsets(nums = [2,4,6], k = 2),
    sol.beautifulSubsets(nums = [1], k = 1),
    sol.beautifulSubsets([4,2,5,9,10,3],1),
    sol.beautifulSubsets([10,4,5,7,2,1], 3),
    sol.beautifulSubsets([1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000],1),
    # sol.findSmallestInteger(nums = [1,-10,7,13,6,8], value = 5),
    # sol.findSmallestInteger(nums = [1,-10,7,13,6,8], value = 7),
    # sol.findSmallestInteger([3,0,3,2,4,2,1,1,0,4], 5),
]
for r in result:
    print(r)
