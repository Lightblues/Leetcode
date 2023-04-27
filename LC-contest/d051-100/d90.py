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
https://leetcode-cn.com/contest/biweekly-contest-90
灵神视频: https://www.bilibili.com/video/BV1zP411P7Ej/

T2手残提交wa了一次. T4想不到优雅的解法, 直接暴力sl, 但因为没有注意到 SortedList 不能直接修改的问题WA了一次. (不会报错, 但因为修改可能导致非有序, 可能有错)

@2022 """
class Solution:
    """ 6225. 差值数组不同的字符串 #easy 所有字符串长度相同. 计算每一个字符串的差值, 找到唯一不同的那个 """
    def oddString(self, words: List[str]) -> str:
        def f(word):
            ords = [ord(x)-ord(word[0]) for x in word]
            return "".join(map(str, ords))
        s = [f(w) for w in words]
        # 找到唯一不同的那个
        cnt = Counter(s)
        for k,v in cnt.items():
            if v==1: return words[s.index(k)]
    
    """ 6228. 距离字典两次编辑以内的单词 """
    def twoEditWords(self, queries: List[str], dictionary: List[str]) -> List[str]:
        def check(s,t):
            cnt = sum(a!=b for a,b in zip(s,t))
            return cnt<=2
        ans = []
        for q in queries:
            for t in dictionary:
                if check(q,t):
                    ans.append(q)
                    break
        return ans
    
    """ 6226. 摧毁一系列目标 #medium 基本计数即可 """
    def destroyTargets(self, nums: List[int], space: int) -> int:
        r2cnt = defaultdict(int)
        r2min = defaultdict(lambda: inf)
        for x in nums:
            r = x % space
            r2cnt[r] += 1
            r2min[r] = min(r2min[r], x)
        mxCnt = max(r2cnt.values())
        return min(r2min[r] for r in r2cnt if r2cnt[r]==mxCnt)


    """ 6227. 下一个更大元素 IV #hard #题型 #review 对数组的每个元素求「对应元素的 第二大 整数」, 其定义为, 该元素idx右侧的第二个比val大的元素值.
思路1: 记录待匹配的元素信息 #二分 查找并进行更新. 
    怎么记录还没有找到对应值的信息? 需要的信息有 (val, cnt, idx), 其中cnt记录右侧比val大的元素数量.
    顺序遍历, 每次二分查找, 对于 sl[:idx] 之前的记录进行更新 (然后讲该记录插入sl)
        若 cnt>=2 说明完成了匹配, remove; 否则, cnt+=1
    为了保证有序结构, 暴力 用了 SortedList
    复杂度: 每次进行二分, 由于每个元素最多更新两次, 因此 O(nlogn)
思路2: 利用两个 #单调栈
    考虑「下一个更大元素」的情况, 可以维护一个单调递减栈来实现. (因为对于之前的更小的元素, 已经找到了更大的元素)
    本题中, 需要「第二大元素」, 可以用两个单调栈来实现. 
        具体而言, 先将元素存储到s, 若遇到更大的元素则将其转移到另一个单调栈 t中, 再次被弹出则说明找到了第二大元素.
    复杂度: O(n)
    [灵神](https://leetcode.cn/problems/next-greater-element-iv/solution/by-endlesscheng-q6t5/)
思路3: 利用高级的数据结构 #elegant
    #名次树; ST表+二分; 线段树二分; 树状数组
    下面的代码: 从大到小遍历nums中的元素, 用一个 名次树 (SortedList) 记录出现的下标. 则在考察一个更小元素的时候, 查看其在 名次树 中的位置即可!
"""
    from sortedcontainers import SortedList
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        sl = SortedList()
        ans = [-1] * n
        for i,x in enumerate(nums):
            # 保存待匹配的元素 (val, cnt, idx), 其中cnt记录右侧比val大的元素数量
            idx = sl.bisect_left((x,0,0))
            # 由于 sl 中的元素无法直接进行修改, 因此需要记录修改的元素.
            toRemoved = []
            toAdd = []
            for ii in range(idx):
                cc = sl[ii][1]
                if cc==1:
                    ans[sl[ii][2]] = x
                    toRemoved.append(sl[ii])
                else: 
                    # 更新cnt, 注意sl的元素无法直接修改!
                    toAdd.append((sl[ii][0], 1, sl[ii][2]))
                    toRemoved.append(sl[ii])
            for tr in toRemoved: sl.remove(tr)
            for ta in toAdd: sl.add(ta)
            sl.add((x,0,i))
        return ans
    
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        # 思路2: 利用两个 #单调栈
        ans = [-1] * len(nums)
        s = []  # 还没找到更大元素的
        t = []  # 找到了下一个更大元素的, 但还没找到第二大元素的
        for i,x in enumerate(nums):
            while t and nums[t[-1]]<x:
                ans[t.pop()] = x
            # 需要讲s中被弹出的元素顺序加入到t中, 可以一步完成
            j = len(s) - 1
            while j>=0 and nums[s[j]]<x:
                j -= 1
            t += s[j+1:]
            del s[j+1:]
            s.append(i)
        return ans
    
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        # 思路3: 利用高级的数据结构 #elegant
        ans = [-1] * len(nums)
        s = SortedList()
        # 注意对于x倒序, 但是相同大小的元素应该从左往右考察
        for _,i in sorted((-x,i) for i,x in enumerate(nums)):
            idx = s.bisect_left(i) + 1
            if idx < len(s): 
                ans[i] = nums[s[idx]]
            s.add(i)
        return ans
    
sol = Solution()
result = [
    # sol.oddString(words = ["adc","wzy","abc"]),
    # sol.oddString(["aaa","bob","ccc","ddd"]),
    # sol.twoEditWords(queries = ["word","note","ants","wood"], dictionary = ["wood","joke","moat"]),
    # sol.twoEditWords(queries = ["yes"], dictionary = ["not"]),
    # sol.destroyTargets(nums = [3,7,8,1,1,5], space = 2),
    sol.secondGreaterElement(nums = [2,4,4,0,9,9,6]),
    sol.secondGreaterElement(nums = [3,3]),
    sol.secondGreaterElement([900,959,984,73,70,13,483,980,600,561,371,222,517,383,533,381,340,317,489,975,420,979,228,269,121,132,951,478,752,167,796,960,812,519,971,851,380,289,574,733,381,786,631,806,695,160,147,22,203,996,763,58,530,979,990,952,502,916,234,817,848,975,808,467,349,792,461,412,85,580,498]),

]
for r in result:
    print(r)
