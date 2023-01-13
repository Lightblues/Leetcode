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
https://leetcode.cn/contest/weekly-contest-327
讨论: https://leetcode.cn/circle/discuss/jy4qll/
T3没想清楚, WA了好多次; T4是一道复杂的模拟题Orz 完全没思路. 

Easonsi @2023 """
class Solution:
    """ 6283. 正整数和负整数的最大计数 """
    def maximumCount(self, nums: List[int]) -> int:
        a = sum(i>0 for i in nums)
        b = sum(i<0 for i in nums)
        return max(a,b)
    
    """ 6285. 执行 K 次操作后的最大分数 #medium. 限制: n,k 1e5
对于一个数组执行K次操作: 每次选最大的加入分数中, 将原来的数字/3 加回去. 问最大分数是多少
思路1: 采用 #最大堆, 复杂度 O(k logn)
"""
    def maxKelements(self, nums: List[int], k: int) -> int:
        nums = [-i for i in nums]
        heapq.heapify(nums)
        acc = 0
        for _ in range(k):
            num = -heappop(nums)
            acc += num
            heappush(nums, -ceil(num/3))
        return acc
    
    """ 6284. 使字符串总不同字符的数目相等 #medium 对于两个字符串, 问能否恰好交换一个字符, 使得两字符串中不同数字的数量相等? 限制: n 1e5
思路0: 下面复杂的逻辑, WA无数次的修补结果...
思路1: 由于字符集S=26, 我们可以枚举所有可能发生交换的字符, 然后判断是否满足条件!
    枚举两个cnt中的字符x,y, 若x==y, 则等于不交换, 只需要比较两个cnt的长度即可
    否则, 还需要根据x,y是否在对方集合中, 相应字符的数量cnt[x], cnt[y]是否为1, 以及两个cnt的长度来判断是否满足条件
    [灵神](https://leetcode.cn/problems/make-number-of-distinct-characters-equal/solution/mei-ju-jian-ji-xie-fa-by-endlesscheng-tjpp/)
"""
    def isItPossible(self, word1: str, word2: str) -> bool:
        # WA无数次的修补结果...WA无数次的修补结果
        cnt1, cnt2 = Counter(word1), Counter(word2)
        if len(cnt1)<len(cnt2):
            cnt1, cnt2 = cnt2, cnt1
        def dictDiff(d1,d2):
            return {k:v for k,v in d1.items() if k not in d2}
        def dictUnion(d1,d2):
            return {k:v for k,v in d1.items() if k in d2}
        d1,d2 = dictDiff(cnt1,cnt2), dictDiff(cnt2,cnt1)
        if len(d1)==len(d2):
            if len(cnt1&cnt2)>0: return True
            if min(d1.values())==min(d2.values())==1: return True
            if max(d1.values())>1 and max(d2.values())>1: return True
        elif len(d1)==len(d2)+1:
            if len((cnt2&cnt1))==0: return False
            if max(d1.values())>1 and max(dictUnion(cnt2,cnt1).values())>1: return True
            if min(d1.values())==1:
                if len(d2)>0 and max(d2.values())>1: return True
                u = dictUnion(cnt2,cnt1)
                if len(u)>0 and min(u.values())==1: return True
        elif len(d1)==len(d2)+2:
            if len((cnt2&cnt1))==0: return False
            if min(d1.values())==1 and max(dictUnion(cnt2,cnt1).values())>1: return True
        return False
    def isItPossible(self, word1: str, word2: str) -> bool:
        """ 思路1, 枚举所有可能发生交换的字符!! """
        cnt1 = Counter(word1)
        cnt2 = Counter(word2)
        for x,c in cnt1.items():
            for y,d in cnt2.items():
                if x==y:
                    # 交换相同字符, 两字符串中不同字符数量不发生改变!
                    if len(cnt1)==len(cnt2): return True
                else:
                    if len(cnt1)-(c==1)+(y not in cnt1) == len(cnt2)-(d==1)+(x not in cnt2):
                        return True
        return False
    
    """ 6306. 过桥的时间 #hard #模拟 
k个工人要将n个箱子从右移动到左边, 一开始的时候工人都在左边. 桥上同时只能有一个人. 
    一个工人有 (leftToRight, pickOld, rightToLeft, putNew) 分别是两次过桥和两次放箱子的时间. 
    定义工人的效率排序为, leftToRight+rightToLeft 越大效率越低, 若相同则id越大效率越低. 桥上只能走一个人, 优先右边过桥, 优先效率低的人通过. 
    问最后一个搬运箱子的人回到左岸的时间. 限制: n 1e4
思路1: #大模拟 用了4个堆
    左右两边分别用一个 wait堆表示等待的人, work堆表示正在搬箱子的人. 
        堆结构: wait只需要用于id/优先级, work堆需要 (完成时间, id)
    维护一个全局的时间cur, 从而控制/模拟过桥逻辑.
        何时更新cur? 这里取决于, 同时只能有一个人过桥 (由wait堆决定), 模拟通过, 更新cur
        注意避免死循环: 两个wait堆可能都是空! 从work堆找到较小的时间, 更新cur, 从而把人加入wait堆
    循环逻辑
        需要搬n个箱子, 直接将剩余的箱子数量作为判断条件; 注意, 只要左边工人出发, 就需要将箱子数量减1
        细节: 退出循环后, 如何得到答案? 将剩余在右边的人模拟回到左边. 
    见 [灵神](https://leetcode.cn/problems/time-to-cross-a-bridge/solution/by-endlesscheng-nzqo/); [视频](https://www.bilibili.com/video/BV1KG4y1j73o/)
"""
    def findCrossingTime(self, n: int, k: int, time: List[List[int]]) -> int:
        """ 
维护一个全局的时间cur, 从而控制/模拟过桥逻辑. 
左边, 有在工作putNew中的那些工人, 有等待过桥的工人; 右边, 有在工作pickOld中的那些工人, 有等待过桥的工人. 
因此, 左右两边分别需要两个堆来完成. workL, waitL; workR, waitR
    wait 队列的逻辑: 根据工人优先级进行排序, 每次选效率最低(优先级最高)
    work 队列逻辑: 需要根据完成时间排序, 然后根据cur来出堆. 

整体控制逻辑: 
1. 左边 workL.top() < cur, 说明完成了工作, 加入waitL, 并出堆;
2. 右边同样的. 
3. 右边先过桥: 若waitR不为空且waitR.top()<cur, 则弹出优先级最高的工人 (把人移到workL中)
4. 左边再过桥: 若waitL不为空且waitL.top()<cur, 则弹出优先级最高的工人 (把人移到workR中)

循环什么时候结束? 
    看剩余需要搬的箱子数量n. 
    注意, 只要左边的过桥, 就需要将n-1.
两种堆的数据结构? 
    wait: 只需要工人id (优先级)
    work: (完成时间, id)
"""
        # leftToRight, pickOld, rightToLeft, putNew
        time.sort(key=lambda t: t[0]+t[2])  # 稳定排序, 这样idx最大的优先级越高
        time.reverse()  # 逆序, idx最小的优先级越高
        cur = 0
        # (完成时间, id)
        workL = []; workR = []
        # id
        waitR = []
        waitL = [i for i in range(k)]
        heapify(waitL)
        while n:
            # 更新work堆: 把完成工作的工人放到wait堆中
            # 左边 workL.top() < cur, 说明完成了工作, 加入waitL, 并出堆;
            while workL and workL[0][0] <= cur:
                _, idx = heappop(workL)
                heappush(waitL, idx)
            while workR and workR[0][0] <= cur:
                _, idx = heappop(workR)
                heappush(waitR, idx)
            # 过桥逻辑: 更新wait堆, 把工人放到work堆中, 注意一次只能过一个人
            if waitR:
                # 右边先过桥: 若waitR不为空且waitR.top()<cur, 则弹出优先级最高的工人 (把人移到workL中)
                idx = heappop(waitR)
                # 更新cur为过桥后的时间
                cur += time[idx][2] 
                heappush(workL, (cur+time[idx][3], idx))    # 还需要放箱子, 才能下一次搬箱子
            # 注意这里, 左边等待队列不为空, 优先过桥, 更新了cur, 重新回到外层while
            elif waitL: 
                idx = heappop(waitL)
                cur += time[idx][0]
                heappush(workR, (cur+time[idx][1], idx))    # 搬箱子
                # 注意, 这里就需要更新n了; 否则是无效的过桥
                n -= 1
            # 注意!! 可能左右wait都为空 (都在搬箱子). 为了避免死循环, 需要更新cur
            else: 
                # 更新cur为下一个完成搬箱子的工人时间, 取min
                if len(workR)==0: cur = workL[0][0]
                elif len(workL)==0: cur = workR[0][0]
                else: cur = min(workL[0][0], workR[0][0])
        # 得到答案「最后一个工人回到左边的时间」
        # 实际上, 由于总是右边等待的人优先 (为空时才会从waitL中取人, n-1), 所以最后waitR一定为空!!!
        # while waitR:
        #     idx = heappop(waitR)
        #     cur += time[idx][2]
        # 剩余还在搬箱的工人
        while workR:
            # (完成时间, id)
            t,idx = heappop(workR)  # t 是完成搬箱的时间
            cur = max(cur, t) + time[idx][2]
        return cur
    
    
sol = Solution()
result = [
    # sol.maximumCount(nums = [-3,-2,-1,0,0,1,2]),
    # sol.maxKelements(nums = [1,10,3,3,3], k = 3),
    # sol.isItPossible(word1 = "abcc", word2 = "aab"),
    # sol.isItPossible(word1 = "ac", word2 = "b"),
    # sol.isItPossible(word1 = "abcde", word2 = "fghij"),
    # sol.isItPossible("ab","abcc"),
    # sol.isItPossible("a","bb"),
    # sol.isItPossible("aa", "bb"),
    # sol.isItPossible("aa","bcd"),
    # sol.isItPossible("aa","ab"),
    # sol.isItPossible("aab","bccd"),
    # sol.isItPossible("az","a"),
    sol.findCrossingTime(n = 1, k = 3, time = [[1,1,2,1],[1,1,3,1],[1,1,4,1]]),
    sol.findCrossingTime(n = 3, k = 2, time = [[1,9,1,8],[10,10,10,10]]),
]
for r in result:
    print(r)
