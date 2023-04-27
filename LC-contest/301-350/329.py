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
https://leetcode.cn/contest/weekly-contest-329
讨论: https://leetcode.cn/circle/discuss/Kclgr5/

Easonsi @2023 """
class Solution:
    def alternateDigitSum(self, n: int) -> int:
        acc = 0; flag = 1
        for d in str(n):
            acc += int(d)*flag
            flag *= -1
        return acc

    """ 根据第 K 场考试的分数排序 """
    def sortTheStudents(self, score: List[List[int]], k: int) -> List[List[int]]:
        n = len(score)
        s = [(score[i][k],i) for i in range(n)]
        s.sort(reverse=True)
        idxs = [i for _,i in s]
        ret = []
        for i in idxs:
            ret.append(score[i])
        return ret
    
    """ 6298. 执行逐位运算使字符串相等 #medium 对于一个二进制串,每次可以选择 (i,j) 坐标, 分别将其变为 s[i] OR s[j], s[i] XOR s[j]. 问对于一个字符串是否可变为target 
思路1: 观察规律, 总结
    考虑变化情况: 00->00; 11->10; 01->11; 10->11. 
        可以发现有01就可以变为全1, 然后对于需要1的位可以用11生成一个0
        因此, 只要s中同时有01, 就可以生成任意非全0的字符串
    不能转换的情况: 1] s全0, 但t中有1; 2] s中有1, 但t全0.
"""
    def makeStringsEqual(self, s: str, target: str) -> bool:
        if s.count('1')==0 and target.count('1')>0: return False
        if s.count('1')>0 and target.count('1')==0: return False
        return True
    
    """ 6299. 拆分数组的最小代价 #hard #DP 可以将一个数组拆分成若干子数组(连续), 每个子数组的分数为, 子数组中非单个元素的总数+k. 问如何分割数组, 使得总分数最小. 限制: n 1e3; 数组元素 [0,n]
思路1: #DP
    DP: 记 f[i] 表示前i个元素的最小代价. 则有递推 f[i] = min{ f[j] + cost[j+1][i] }, 其中 cost[j+1][i] 表示 [j+1,i] 范围的代价
        这样, 不考虑cost的代价, DP复杂度为 O(n^2)
    预先计算代价矩阵 cost, 可以通过两次遍历, 记录当前范围内的数字情况来计算. 复杂度也是 O(n^2)
"""
    def minCost(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # 预先计算好 [i,j] 范围的代价
        cost = [[0]*n for _ in range(n)]
        for i in range(n):
            cnt = Counter()
            acc = 0
            for j in range(i,n):
                if cnt[nums[j]]==1: acc +=2
                elif cnt[nums[j]]>1: acc+=1
                cnt[nums[j]]+=1
                cost[i][j] = acc+k
        # DP. f[i] 表示前i个元素的最小代价
        f = [0]*n
        for i in range(n):
            mn = cost[0][i]
            for j in range(i):
                mn = min(mn, f[j]+cost[j+1][i])
            f[i] = mn
        return f[-1]
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.minCost(nums = [1,2,1,2,1,3,3], k = 2),
    # sol.minCost(nums = [1,2,1,2,1], k = 2),
    # sol.minCost(nums = [1,2,1,2,1], k = 5),
    # sol.makeStringsEqual(s = "1010", target = "0110"),
    # sol.makeStringsEqual(s = "11", target = "00"),
    # sol.sortTheStudents(score = [[10,6,9,1],[7,5,11,2],[4,8,3,15]], k = 2),
    # sol.sortTheStudents(score = [[3,4],[5,6]], k = 0),
    sol.alternateDigitSum(886996),
    sol.alternateDigitSum(521),
]
for r in result:
    print(r)
