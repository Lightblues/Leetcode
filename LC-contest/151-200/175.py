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
https://leetcode.cn/contest/weekly-contest-175

T3的背景很有意思, 居然可以用暴力求解; T4状压DP看到了标签才想到, 还需要加强. 

@2022 """
class Solution:
    """ 1346. 检查整数及其两倍数是否存在 """
    
    """ 1347. 制造字母异位词的最小步骤数 """
    
    """ 1349. 参加考试的最大学生数 #hard 有一个grid表示座位情况, 部分机器是坏的. 一个学生可以看到左右和斜前方左右的四个位置. 问最多能安排多少人? 限制: m,n 8
https://leetcode.cn/problems/maximum-students-taking-exam/
思路1: #状压 #DP
    遍历每一行, 用mask表示学生坐的分布. 根据 上一行的座位情况+本行的空位 遍历所有可能的安排. 
    根据本行的空位+上一行的座位情况, 可以知道所有可坐的位置. 枚举所有的情况. 
    复杂度: 状态空间 O(2^n * m), 转移过程中, 枚举所有可坐的位置, 每次判断一行 复杂度 O(2^n n), 总复杂度大概 O(4^n * nm)
see [官答](https://leetcode.cn/problems/maximum-students-taking-exam/solutions/101748/can-jia-kao-shi-de-zui-da-xue-sheng-shu-by-leetcod/)
"""
    def maxStudents(self, seats: List[List[str]]) -> int:
        m,n = len(seats), len(seats[0])
        # canSee = [(0,-1), (0,1), (-1,-1), (-1,1)] # 可以看到的位置.
        MX = 1<<n
        # 注意, 不加cache会超时!
        @lru_cache(None)
        def f(i, mask) -> int:
            # 遍历到第i行, mask表示上一行学生坐的分布. 返回这种情况下后续排最多能坐多少人
            if i==m: return 0
            # 找到所有可坐的位置
            ava = 0
            for j in range(n):
                if seats[i][j] == '#': continue
                if j>0 and mask & (1<<j-1) or mask & (1<<j+1): continue
                ava += 1<<j
            ans = 0
            # 转移: 简单起见, 直接暴力枚举
            for sub in range(MX):
                if sub & ava != sub: continue
                if "11" in bin(sub): continue
                ans = max(ans, bin(sub).count('1') + f(i+1, sub))
            return ans
        return f(0, 0)
    
""" 1348. 推文计数 #medium #题型 一条推文由 <name, time> 构成. 要求查询 getTweetCountsPerFrequency(freq, name, s,e) 范围内的推文数量. [s,e] 区间根据 freq进行分割 (60/3600/86400), 统计其中名字为name的推文数量.
限制: 查询次数 1e4; 时间 1e9; e-s 1e4
思路1: #线性表 #暴力
    直接记录每个name的推文的所有时间. 对于每次查询, 遍历所有时间, 统计数量.
    复杂度: 插入 n次, 查询 q次, 查询的时间范围为 t. 对于每次查询, 需要遍历所有时间, 同时还要开一个和t线性的返回数组. 因此复杂度为 `O(q (t+n))`.
思路2: #平衡二叉树 或者 #有序数组
    复杂度: 每次插入复杂度为 O(logn). 每次查询复杂度为 O(logn * t) [按照官答的思路, 也可以是 logn + t]. 因此总复杂度为 `O(nlogn + q(t logn))`.
见 [官答](https://leetcode.cn/problems/tweet-counts-per-frequency/solutions/101747/tui-wen-ji-shu-by-leetcode-solution/)
"""
class TweetCounts:
    freq2sec = {'minute': 60, 'hour': 3600, 'day': 86400}
    def __init__(self):
        self.record = defaultdict(list)

    def recordTweet(self, tweetName: str, time: int) -> None:
        self.record[tweetName].append(time)

    def getTweetCountsPerFrequency(self, freq: str, tweetName: str, startTime: int, endTime: int) -> List[int]:
        sec = self.freq2sec[freq]
        ret = [0] * ((endTime - startTime) // sec + 1)
        for t in self.record[tweetName]:
            if startTime <= t <= endTime:
                ret[(t - startTime) // sec] += 1
        return ret

from sortedcontainers import SortedList
class TweetCounts:
    freq2sec = {'minute': 60, 'hour': 3600, 'day': 86400}
    def __init__(self):
        self.record = defaultdict(SortedList)

    def recordTweet(self, tweetName: str, time: int) -> None:
        self.record[tweetName].add(time)

    def getTweetCountsPerFrequency(self, freq: str, tweetName: str, startTime: int, endTime: int) -> List[int]:
        sec = self.freq2sec[freq]
        ans = []
        sl = self.record[tweetName]
        l = sl.bisect_left(startTime)
        t = startTime + sec
        while t <= endTime:
            r = sl.bisect_left(t)
            ans.append(r-l)
            l = r
            t += sec
        r = sl.bisect_right(endTime)
        ans.append(r-l)
        return ans
        
sol = Solution()
result = [
    testClass("""["TweetCounts","recordTweet","recordTweet","recordTweet","getTweetCountsPerFrequency","getTweetCountsPerFrequency","recordTweet","getTweetCountsPerFrequency"]
[[],["tweet3",0],["tweet3",60],["tweet3",10],["minute","tweet3",0,59],["minute","tweet3",0,60],["tweet3",120],["hour","tweet3",0,210]]""")
    # sol.maxStudents(seats = [["#",".","#","#",".","#"],
    #           [".","#","#","#","#","."],
    #           ["#",".","#","#",".","#"]]),
    # sol.maxStudents(seats = [[".","#"],
    #           ["#","#"],
    #           ["#","."],
    #           ["#","#"],
    #           [".","#"]]),
]
for r in result:
    print(r)
