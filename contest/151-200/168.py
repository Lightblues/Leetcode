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
https://leetcode.cn/contest/weekly-contest-168

T2经典题型, 数据结构需要考虑. T3可以有精彩的 可行性优化. T4是个有趣的模拟题目, 但理解之后就是基本的BFS. 

@2022 """
class Solution:
    """ 1295. 统计位数为偶数的数字 """
    
    """ 1296. 划分数组为连续数字的集合 #medium #题型 给定一个数组和一个整数k, 判断数组能否分割成 n/k 组, 每组是k个连续的数字. 限制: n 1e5
思路1: 基本思路是 #贪心
    贪心, 也即每次选择剩余的最小的那个数字, 然后从数组中去除 [x, x+k-1]. 问题是如何执行「删除」操作? 
        1.0 直接用list的 remove 操作, 结果 #TLE
        1.1 官答的思路是用cnt字典来记录每个字符的使用情况. 然后遍历 **排好序** 的数组, 遇到全部使用完的数字就跳过. 
        1.2 还可以直接用 `SortedDict` 直接完成了排序. 
    [官答](https://leetcode.cn/problems/divide-array-in-sets-of-k-consecutive-numbers/solution/hua-fen-shu-zu-wei-lian-xu-shu-zi-de-ji-he-by-le-2/)
"""
    def isPossibleDivide(self, nums: List[int], k: int) -> bool:
        # 思路1.0: #TLE 了! 因为list的remove操作复杂度较高!
        if len(nums)%k != 0: return False
        nums.sort()
        while len(nums)>0:
            n = nums[0]
            for i in range(k):
                if n+i not in nums: return False
                nums.remove(n+i)
        return True
    def isPossibleDivide(self, nums: List[int], k: int) -> bool:
        # 1.2 还可以直接用 `SortedDict` 直接完成了排序. 
        from sortedcontainers import SortedDict
        sd = SortedDict(Counter(nums))
        for x,c in sd.items():
            for i in range(c):
                for j in range(x, x+k):
                    if j not in sd or sd[j] == 0: return False
                    sd[j] -= 1
        return True
    def isPossibleDivide(self, nums: List[int], k: int) -> bool:
        # 1.1 官答的思路是用cnt字典来记录每个字符的使用情况. 然后遍历 **排好序** 的数组, 遇到全部使用完的数字就跳过. 
        nums.sort()
        cnt = Counter(nums)
        for x in nums:
            if cnt[x]==0: continue
            for num in range(x, x+k):
                if cnt[num] == 0: return False
                cnt[num] -= 1
        return True
    
    """ 1297. 子串的最大出现次数 #medium 给定一个长n的字符串, 找到长度在 [mn,mx] 范围内的, 其中的不同字符数最多为 maxLetters的子串, 要求其在s中出现的次数最多 (若有多个任一即可). 
限制: n 1e5; mn, mx 26
思路1: #暴力 统计字符串中所有出现的长度在 [mn,mx] 范围内的子串, 统计每个子串出现的次数. #滑动窗口
    复杂度: 不同字符串的数量 O(n * L^2). 这里的L是mx,mn 的数量级.
思路2: 可行性优化. 注意到, 题目并不要求「找到最长的满足要求的字符串」. 而根据要求, **答案 (之一) 一定可以是一个长mn的子串**. 
    这样, 我们仅需要枚举长度为mn的子串即可. 复杂度 O(n L)
思路3: 进一步可以用 #滚动哈希 来求字符串哈希. 统计次数. 
    关联: 1044. 最长重复子串 #hard 
[官答](https://leetcode.cn/problems/maximum-number-of-occurrences-of-a-substring/solution/zi-chuan-de-zui-da-chu-xian-ci-shu-by-leetcode-sol/)
"""
    def maxFreq(self, s: str, maxLetters: int, minSize: int, maxSize: int) -> int:
        cnt = Counter()
        # 1.1 枚举长 [mn,mx] 范围内所有子串
        # for l in range(minSize, maxSize+1):
        #     for i in range(l, len(s)+1):
        #         cnt[s[i-l:i]] += 1
        # 2.1 枚举长 mn 的子串
        for i in range(minSize, len(s)+1):
            cnt[s[i-minSize:i]] += 1
        for k,v in sorted(cnt.items(), key=lambda x:x[1], reverse=True):
            if len(set(k)) <= maxLetters: return v
        return 0
    def maxFreq(self, s: str, maxLetters: int, minSize: int, maxSize: int) -> int:
        # 官答, 用了字典记录出现的不同字符进行剪枝. 
        n = len(s)
        occ = collections.defaultdict(int)
        ans = 0
        for i in range(n - minSize + 1):
            cur = s[i : i + minSize]
            exist = set(cur)
            if len(exist) <= maxLetters:
                occ[cur] += 1
                ans = max(ans, occ[cur])
        return ans

    """ 1298. 你能从盒子里获得的最大糖果数 #hard #模拟 #题型 有一组盒子, 用 `[status, candies, keys, containedBoxes]` 表示每一个盒子 是否打开 (1/0); 包含的糖果数量; 包含哪些盒子的钥匙; 包含的盒子. 
一开始有 initialBoxes. 问最后能获得的最大糖果数. 限制: n 1e3; 
思路0: 比较繁琐的递归搜索
    维护 已打开/已得到没有钥匙的盒子 字典. 模拟打开盒子, 取得 糖果/钥匙/盒子. 
    具体而言, 拿到一个盒子
        已打开过: 跳过;
        上锁了没有钥匙: 加入待打开盒子;
思路1: #BFS
    整理一下思路, 我们可以用 `has_box` 记录我们拥有的盒子, `can_open` 记录是否可以打开该盒子. 
    用一个 queue 记录可以打开的盒子, BFS即可. 用keys更新can_open, 用containedBoxes更新has_box, 并将可以打开的加入到queue中.
    [官答](https://leetcode.cn/problems/maximum-candies-you-can-get-from-boxes/solution/ni-neng-cong-he-zi-li-huo-de-de-zui-da-tang-guo-2/)
"""
    def maxCandies(self, status: List[int], candies: List[int], keys: List[List[int]], containedBoxes: List[List[int]], initialBoxes: List[int]) -> int:
        res = 0
        opened = set()  # 1. 已打开
        toOpen = set()  # 2. 待打开
        newKeys = set() # 3. 有钥匙
        def openBox(b):
            """ 模拟打开盒子 """
            nonlocal res
            # 1. 已打开
            if b in opened: return
            # 2. 上锁了没有钥匙
            if status[b]==0 and b not in newKeys: return
            # 3. 打开
            res += candies[b]
            opened.add(b)
            toOpen.update(containedBoxes[b])
            newKeys.update(keys[b])
            for nb in containedBoxes[b]:
                openBox(nb)
            for nk in keys[b]:
                if nk in toOpen: openBox(nk)
        toOpen.update(initialBoxes)
        for b in initialBoxes: openBox(b)
        return res

    def maxCandies1(self, status: List[int], candies: List[int], keys: List[List[int]], containedBoxes: List[List[int]], initialBoxes: List[int]) -> int:
        # 思路1: #BFS
        n = len(status)
        can_open = [status[i] == 1 for i in range(n)]       # 是否可以打开
        has_box, used = [False] * n, [False] * n            # 是否有盒子，是否已经使用过
        
        q = collections.deque() # 可以打开的盒子
        ans = 0
        for box in initialBoxes:
            has_box[box] = True
            if can_open[box]:
                q.append(box)
                used[box] = True
                ans += candies[box]
        
        while len(q) > 0:
            big_box = q.popleft()
            for key in keys[big_box]:
                can_open[key] = True
                if not used[key] and has_box[key]:
                    q.append(key)
                    used[key] = True
                    ans += candies[key]
            for box in containedBoxes[big_box]:
                has_box[box] = True
                if not used[box] and can_open[box]:
                    q.append(box)
                    used[box] = True
                    ans += candies[box]
        
        return ans


sol = Solution()
result = [
    # sol.maxCandies(status = [1,0,1,0], candies = [7,5,4,100], keys = [[],[],[1],[]], containedBoxes = [[1,2],[3],[],[]], initialBoxes = [0]), 
    # sol.maxCandies(status = [1,0,0,0,0,0], candies = [1,1,1,1,1,1], keys = [[1,2,3,4,5],[],[],[],[],[]], containedBoxes = [[1,2,3,4,5],[],[],[],[],[]], initialBoxes = [0]), 
    # sol.maxCandies([1,1,1], [100,1,100], [[],[0,2],[]], [[],[],[]], [1]),
    # sol.isPossibleDivide(nums = [1,2,3,3,4,4,5,6], k = 4),
    sol.maxFreq(s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4),
    sol.maxFreq(s = "abcde", maxLetters = 2, minSize = 3, maxSize = 3),
]
for r in result:
    print(r)
