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
https://leetcode.cn/contest/weekly-contest-325
讨论: https://leetcode.cn/circle/discuss/RmydJj/
新冠感染期间果然没啥状态...

@2022 """
class Solution:
    """ 6269. 到目标字符串的最短距离 #easy #题型 对于一个环形数组, 计算 (i,j) 之间的距离 """
    def closetTarget(self, words: List[str], target: str, startIndex: int) -> int:
        n = len(words)
        idxs = [i for i,w in enumerate(words) if w==target]
        if len(idxs)==0: return -1
        ans = n
        for idx in idxs:
            # 对于两个idx排序之后更方便处理!
            a,b = sorted([idx, startIndex])
            ans = min(ans, b-a, a-(b-n))
        return ans
    
    """ 6270. 每种字符至少取 K 个 #medium #题型 字符串仅由 abc 三个字符构成, 要从首尾取一些字符, 每种至少k个, 问最小需要取多少个? 限制: 字符串长度 1e5; 0<=k<=len(s)
思路1: #二分 检查首尾取x个是否可满足条件
    每次通过滑窗检查, 复杂度 O(x); 二分的范围为 [0,n]
    #细节: 被坑的一点是 k==0 的情况!
思路2: #同向双指针 复杂度 O(n) 见 [two-pointer]
    见 [灵神](https://leetcode.cn/problems/take-k-of-each-character-from-left-and-right/solution/on-shuang-zhi-zhen-by-endlesscheng-4g9p/)
"""
    def takeCharacters(self, s: str, k: int) -> int:
        # 边界: 注意k=0的情况
        if k==0: return 0
        n = len(s)
        def _check(cnt):
            # 检查 Counter中的字符是否满足条件
            return len(cnt)==3 and all(v>=k for v in cnt.values())
        # 整体字符串进行边界检查
        cnt = Counter(s)
        if not _check(cnt): return -1
        def check(x):
            # 检查是否可以通过在首尾取 x个字符, 完成k的限制
            cnt = Counter(s[:x])
            if _check(cnt): return True
            for i in range(x):
                cnt[s[x-i-1]] -= 1
                cnt[s[-i-1]] += 1
                if _check(cnt): return True
            return False
        # 二分搜索最小的解
        l,r = 3,n
        ans = n
        while l<=r:
            mid = (l+r)//2
            if check(mid): 
                ans = mid
                r = mid-1
            else: l = mid+1
        return ans

    """ 6271. 礼盒的最大甜蜜度 #medium #题型 需要从一组价格为 price 的糖果中选k个打包, 定义其「甜蜜度」 是礼盒中任意两种糖果 价格 绝对差的最小值, 要求获得最大「甜蜜度」. 限制: n 1e5. 价格 1e9
思路1: #二分 
    子问题「能否选取一组k个糖果使得甜蜜度至少为 x」可以通过谈心求解 复杂度 O(n). 二分的范围 [0, (mx-mn)/(k-1)]
参见 [灵神](https://leetcode.cn/problems/maximum-tastiness-of-candy-basket/solution/er-fen-da-an-by-endlesscheng-r418/)
关联: 「1552. 两球之间的磁力」
"""
    def maximumTastiness(self, price: List[int], k: int) -> int:
        pass
        
    """ 6272. 好分区的数目 #hard #题型 将一个数组分成两部分, 要求每个部分之和都大于等于 k, 问有多少中分割方式, 对答案取模. 限制: 数组长度 1e3, k 1e3
提示: 问题等价于, 数组中, 范围在 [k, sum(nums)-k] 的数量. (注意, 若一个数组和在这一范围内, 则另一个也必然在这一范围内)
思路1: 注意到这里的 k<=1000, 可以利用这一性质
    计算「之和 <=x 的子数组数量」
        我们对数组排序, 利用Counter统计子数组和出现的次数 (大于x的就不用了), 遍历累计, 则该问题的复杂度在 O(n*x) 限制内. 
    如何计算 [k, sum(nums)-k] 范围内的数量? 我们只需要计算 [0, k-1] 的数量即可, 另一个边界的数量是一样的! 
        注意, 利用k的范围, 复杂度控制在 O(n*k) 以内
        最后答案就是 所有非空子数组数量 - 2* 数组和在(0, k-1]范围内子数组的数量
[灵神](https://leetcode.cn/problems/number-of-great-partitions/solution/ni-xiang-si-wei-01-bei-bao-fang-an-shu-p-v47x/)
其中指出, 「之和 <=x 的子数组数量」是经典的「01 背包」问题. 
"""
    def countPartitions(self, nums: List[int], k: int) -> int:
        mod = 10**9 + 7
        nums.sort()
        def count(x):
            # 计算之和 <=x 的子数组数量
            cnt = Counter()
            for a in nums:
                # 定义一个新的 Counter, 因为不能在原 cnt上修改
                cnt_new = Counter()
                if a<=x:
                    cnt_new[a] += 1
                for b in cnt.keys():
                    if a+b<=x: cnt_new[a+b] += cnt[b] % mod
                # 剪枝
                if len(cnt_new)==0: break
                cnt += cnt_new
            return sum(cnt.values())
        # 要使得分区满足条件, 则一个分区的和必须在 [k, sum(nums)-k]
        l,r = k, sum(nums)-k
        if l>r: return 0
        # 注意, sum(nums)-k 可能非常大! 用上的 count 函数计算会超时!!
        # acc = count(r) - count(l-1)
        #  acc % mod
        cnt_oneside = pow(2, len(nums), mod) - 2 # 所有非空子数组的数量
        return (cnt_oneside - count(k-1)*2) % mod

sol = Solution()
result = [
    # sol.closetTarget(words = ["hello","i","am","leetcode","hello"], target = "hello", startIndex = 1),
    # sol.closetTarget(["hsdqinnoha","mqhskgeqzr","zemkwvqrww","zemkwvqrww","daljcrktje","fghofclnwp","djwdworyka","cxfpybanhd","fghofclnwp","fghofclnwp"],"zemkwvqrww",8),

    # sol.maximumTastiness(price = [13,5,1,8,21,2], k = 3),
    # sol.maximumTastiness(price = [7,7,7,7], k = 2),
    sol.countPartitions(nums = [1,2,3,4], k = 4),
    sol.countPartitions(nums = [6,6], k = 2),
    sol.countPartitions(nums = [3,3,3], k = 4),
    sol.countPartitions([96,40,22,98,9,97,45,22,79,57,95,62],505),
    sol.countPartitions([977208288,291246471,396289084,732660386,353072667,34663752,815193508,717830630,566248717,260280127,824313248,701810861,923747990,478854232,781012117,525524820,816579805,861362222,854099903,300587204,746393859,34127045,823962434,587009583,562784266,115917238,763768139,393348369,3433689,586722616,736284943,596503829,205828197,500187252,86545000,490597209,497434538,398468724,267376069,514045919,172592777,469713137,294042883,985724156,388968179,819754989,271627185,378316864,820060916,436058499,385836880,818060440,727928431,737435034,888699172,961120185,907997012,619204728,804452206,108201344,986517084,650443054], 95),
]
for r in result:
    print(r)
