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
https://leetcode.cn/contest/weekly-contest-336
Easonsi @2023 """
class Solution:
    """ 6315. 统计范围内的元音字符串数 """
    def vowelStrings(self, words: List[str], left: int, right: int) -> int:
        vowels = 'aeiou'
        ans = 0
        for w in words[left:right+1]:
            if w[-1] in vowels and w[0] in vowels: ans += 1
        return ans
    
    """ 6316. 重排数组以得到最大前缀分数 """
    def maxScore(self, nums: List[int]) -> int:
        nums.sort(reverse=True)
        ans = 0
        acc = 0
        for x in nums:
            acc += x
            if acc>0: ans += 1
        return ans
    
    """ 6317. 统计美丽子数组数目 """
    def beautifulSubarrays(self, nums: List[int]) -> int:
        preCnt = Counter()
        preCnt[0] += 1
        xx = 0
        ans = 0
        for x in nums:
            xx ^= x
            ans += preCnt[xx]
            preCnt[xx] += 1
        return ans

    """ 6318. 完成所有任务的最少时间 #hard 给定一组 task = (s,e,cnt), 要求从 [s,e] 范围内选出cnt个整数点才能完成. 问最少需要多少个点可以满足要求
思路0: 尝试区间叠加计数; 但应该是不能的? 因为区间内所需的点数不确定! 
思路1: 对于end进行排序, #贪心 填充最后空的位置
     """
    def findMinimumTime(self, tasks: List[List[int]]) -> int:
        """ 错了! 例如 [1,3,1],[1,3,1],[1,3,1] 只需要一个点就可以同时满足, 但是 [4,5,2] 需要更多的点 """
        tasks.sort(key=lambda x: x[1])
        mx = max(i[1] for i in tasks)
        comp = [0] * (mx+2)
        acc = [0] * (mx+2)
        for s,e,_ in tasks:
            acc[s] += 1
            acc[e+1] -= 1
        for i in range(1, mx+2):
            acc[i] += acc[i-1]
        # 
        q = []  # 当前判断的范围 (acc, idx) 根据 acc 逆排序
        preEnd = -1
        for s,e,tt in tasks:
            for i in range(max(preEnd+1,s), e+1):
                heappush(q, (-acc[i], i))
            tt -= sum(comp[s:e+1])
            while tt>0:
                _,idx = heappop(q)
                if s<=idx and comp[idx]==0:
                    comp[idx] = 1
                    tt -= 1
            preEnd = e
        return sum(comp)
    def findMinimumTime(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda x: x[1])
        mx = max(i[1] for i in tasks)
        comp = [0] * (mx+2)
        for s,e,tt in tasks:
            tt -= sum(comp[s:e+1])
            # 贪心填充
            idx = e
            while tt>0:
                if comp[idx]==0:
                    comp[idx] = 1
                    tt -= 1
                idx -=1
        return sum(comp)
    
sol = Solution()
result = [
    # sol.maxScore(nums = [2,-1,0,1,-3,3,-3]),
    # sol.beautifulSubarrays(nums = [4,3,1,2,4]),
    # sol.beautifulSubarrays([1,10,4]),

    # sol.findMinimumTime(tasks = [[2,3,1],[4,5,1],[1,5,2]]),
    # sol.findMinimumTime(tasks = [[1,3,2],[2,5,3],[5,6,2]]),
    sol.findMinimumTime([[14,20,5],[2,18,7],[6,14,1],[3,16,3]]),
]
for r in result:
    print(r)
