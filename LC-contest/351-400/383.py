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
https://leetcode.cn/contest/weekly-contest-383
https://leetcode.cn/circle/discuss/WmtlPM/

Z函数有意思! 

Easonsi @2023 """
class Solution:
    """ 3028. 边界上的蚂蚁 """
    def returnToBoundaryCount(self, nums: List[int]) -> int:
        pos = 0
        ans = 0
        for x in nums:
            pos += x
            if pos==0: ans +=1
        return ans
    
    """ 3029. 将单词恢复初始状态所需的最短时间 I  """
    
    """ 3030. 找出网格的区域平均强度 #medium """
    def resultGrid(self, image: List[List[int]], threshold: int) -> List[List[int]]:
        m,n = len(image), len(image[0])
        record = [[[] for _ in range(n)] for _ in range(m)]
        def checkRegion(i,j):
            for di in range(3):
                for dj in range(2):
                    if abs(image[i+di][j+dj]-image[i+di][j+dj+1])>threshold: return False
            for dj in range(3):
                for di in range(2):
                    if abs(image[i+di][j+dj]-image[i+di+1][j+dj])>threshold: return False
            return True
        def do_record(i,j):
            record_value = sum(image[i+di][j+dj] for di in range(3) for dj in range(3)) // 9
            for di in range(3):
                for dj in range(3):
                    record[i+di][j+dj].append(record_value)
            return
        for i in range(0,m-2):
            for j in range(0,n-2):
                if checkRegion(i,j):
                    do_record(i,j)
        # 
        for i in range(m):
            for j in range(n):
                if record[i][j]:
                    record[i][j] = sum(record[i][j]) // len(record[i][j])
                else:
                    record[i][j] = image[i][j]
        return record

    @staticmethod
    def z_function(s: str):
        """ Z Algorithm 对于一个字符串s, 计算其每个位置的前缀和后缀相同的长度 
        可视化网站: https://personal.utdallas.edu/~besp/demo/John2010/z-algorithm.htm
        oi-wiki: https://oi-wiki.org/string/z-func/
        为什么复杂度是 O(n)? 因为在 while循环中, 每次至少会使得 right + 1
        """
        n = len(s)
        z = [0] * n
        left, right = 0, 0          # 维护一个滑动窗口 (z-box)
        for i in range(1,n):        # 位置0没有意义
            if i <= right:          # 在范围内的话, 复用此前的结果
                # Z 函数核心思想! 
                z[i] = min(right-i+1, z[i-left])    # 若在 z-box 中, 可知 z[i...right] == z[(i-left)...(right-left)] —— 因为 s[0...right-left] == s[left...right]]
            while i+z[i] < n and s[z[i]] == s[i+z[i]]:
                left, right = i, i+z[i]
                z[i] += 1
        return z

    """ 3031. 将单词恢复初始状态所需的最短时间 II #hard 
等价于, 按照每k的步骤跳, 检查最少到哪里可以构成前缀相同的字符串
限制: n 1e6
思路1: #Z 函数（扩展 KMP）
    Z-函数的定义是什么? z[i] 表示 s[i...n-1] 和 s 的最长公共前缀长度! (也即从i位置往后匹配s的前缀)
参见 [ling](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/solutions/2630932/z-han-shu-kuo-zhan-kmp-by-endlesscheng-w44j/), 见视频
    """
    def minimumTimeToInitialState(self, word: str, k: int) -> int:
        n = len(word)
        z = [0] * n
        left, right = 0, 0          # 维护一个滑动窗口 (z-box)
        for i in range(1,n):        # 位置0没有意义
            if i <= right:          # 在范围内的话, 复用此前的结果
                # 注意有 right边界! 去除这个min的话, 例如 aaab 这种就有问题!
                z[i] = min(right-i+1, z[i-left])    # 若在 z-box 中, 可知 z[i...right] == z[(i-left)...(right-left)] —— 因为 s[0...right-left] == s[left...right]]
            while i+z[i] < n and word[z[i]] == word[i+z[i]]:
                left, right = i, i+z[i]
                z[i] += 1
            # 检查是否满足条件
            if i%k==0 and i+z[i] >= n:
                return i//k
        return math.ceil(n/k)
    

    
sol = Solution()
result = [
    # sol.resultGrid(image = [[5,6,7,10],[8,9,10,10],[11,12,13,10]], threshold = 3),
    # sol.resultGrid(image = [[10,20,30],[15,25,35],[20,30,40],[25,35,45]], threshold = 12),

    # sol.z_function("aabcaabxaaaz"),
    sol.minimumTimeToInitialState(word = "abacaba", k = 3),
    sol.minimumTimeToInitialState(word = "abacaba", k = 4),
]
for r in result:
    print(r)
