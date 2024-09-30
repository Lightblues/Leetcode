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
https://leetcode.cn/contest/weekly-contest-416
有点太简单了
Easonsi @2023 """
class Solution:
    """ 3295. 举报垃圾信息 """
    def reportSpam(self, message: List[str], bannedWords: List[str]) -> bool:
        s = set(bannedWords)
        return sum(m in s for m in message) >= 2
    
    """ 3296. 移山所需的最少秒数 
思路1: 
    工人i负责x所需的时间是 tims[i] * x(x+1)/2
    """
    def minNumberOfSeconds(self, mountainHeight: int, workerTimes: List[int]) -> int:
        n = len(workerTimes)
        mx = min(workerTimes) * mountainHeight*(mountainHeight+1)//2
        def check(x):
            acc = 0
            for t in workerTimes:
                a = math.sqrt(2*x/t+1/4) - 1/2
                acc += int(a)
                if acc >= mountainHeight: return True
            return False
        
        l,r = 0,mx
        ans = mx
        while l <= r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                r = mid-1
            else:
                l = mid+1
        return ans
    
    """ 3297. 统计重新排列后包含另一个字符串的子字符串数目 I 等价于, 问word1的所有子串中, 包含 word2 的数量
限制: len(word1) 1e5; len(word2) 1e4
    """
    def validSubstringCount(self, word1: str, word2: str) -> int:
        c2 = Counter(word2)
        num_unvalid = len(c2)
        r = 0; n = len(word1); ans = 0
        c = Counter()
        for i,x in enumerate(word1):
            if i>0: 
                c[word1[i-1]] -= 1
                if c[word1[i-1]] < c2[word1[i-1]]: num_unvalid += 1
            while r<n and num_unvalid>0:
                x = word1[r]
                c[x] += 1
                if x in c2 and c[x] == c2[x]: num_unvalid -= 1
                r += 1
            if num_unvalid > 0: break
            ans += (n-r+1)
        return ans
    
sol = Solution()
result = [
    # sol.reportSpam(message = ["hello","world","leetcode"], bannedWords = ["world","hello"]),
    # sol.minNumberOfSeconds( mountainHeight = 4, workerTimes = [2,1,1]),
    # sol.minNumberOfSeconds(10, [3,2,2,4]),
    sol.validSubstringCount(word1 = "bcca", word2 = "abc"),
    sol.validSubstringCount(word1 = "abcabc", word2 = "abc"),
]
for r in result:
    print(r)
