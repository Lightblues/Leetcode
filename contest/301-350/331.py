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
https://leetcode.cn/contest/weekly-contest-331
讨论: https://leetcode.cn/circle/discuss/2Gdn7F/
灵神: https://www.bilibili.com/video/BV1sG4y1T7oc/

T3的二分反应还是慢了; T4的构造也很巧妙, 自己还需努力
Easonsi @2023 """
class Solution:
    """ 6348. 从数量最多的堆取走礼物 """
    def pickGifts(self, gifts: List[int], k: int) -> int:
        gifts = [-g for g in gifts]
        heapify(gifts)
        for _ in range(k):
            mx = -heappop(gifts)
            heappush(gifts, -math.floor(math.sqrt(mx)))
        return -sum(gifts)
    """ 6347. 统计范围内的元音字符串数 """
    def vowelStrings(self, words: List[str], queries: List[List[int]]) -> List[int]:
        vowels = 'aeiou'
        words = [w[0] in vowels and w[-1] in vowels for w in words]
        acc = list(accumulate(words, initial=0))
        return [acc[j+1]-acc[i] for i,j in queries]
    
    """ 6346. 打家劫舍 IV #medium 要求从数组中选择不相邻的k个位置, score为其中的最大值. 问最小的score
限制: n 1e5; 元素大小 1e9
思路1: 对于一个固定的score, 我们可以贪心在 O(n) 时间检查; 因此, 二分即可!
    灵神总结: 「有单调性, 就可以考虑二分」!! 
思路1.1: #二分 #DP 注意下面调用 bisect_left 的用法, 用于二分查找!
    [灵神](https://leetcode.cn/problems/house-robber-iv/solution/er-fen-da-an-dp-by-endlesscheng-m558/)
    关联: 0198. 打家劫舍
"""
    def minCapability(self, nums: List[int], k: int) -> int:
        def test(x):
            pre = -2
            cnt = 0
            for i,num in enumerate(nums):
                if pre!=i-1 and x>=num:
                    cnt += 1
                    pre = i
                    if cnt>=k: return True
            return False
        l,r = min(nums),max(nums)
        # 闭区间
        while l<=r:
            mid = (l+r)//2
            res = test(mid)
            if res: r = mid-1
            else: l = mid+1
        return r+1
    def minCapability(self, nums: List[int], k: int) -> int:
        # from 灵神
        def check(mx: int) -> int:
            f0 = f1 = 0
            for x in nums:
                if x > mx: f0 = f1
                else: f0, f1 = f1, max(f1, f0 + 1)
            return f1
        return bisect_left(range(max(nums)), k, key=check)

    """ 6345. 重排水果 #hard #构造 对于两组长度都是n的数组, 每次可以在两个数组中选择 (i,j) 位置互换. 每次交换的代价为两个数字中的min. 问使得两数组相等的最小代价 (重排后相同)
限制: n 1e5
思路1: #思维
    显然, 由于要求相等, 若arr1少了x, 那个arr2一定多了x. 注意, 每次进行交换, 对一个数组而言会发生一多一少两个变化!
    只需要考虑一个数组! 考虑 arr1和目标数组arr 的差异数组 diff, (不管是多了还是少了都算). 则需要进行的交换次数为 len(diff)//2
    考虑两种交换的方式: 
        1] 直接交换 (x,y), 代价为 min{x,y}; 
        2] 利用一个中间变量 mn 进行两次交换 (x,mn), (mm,y) (这里假设最小值在arr2, 反之一样的), 代价为 2*mn
    注意: 我们只需要考虑 diff 的前一半就可以了! 因为后一半是被交换的对象, 代价为0!
    见 [肖恩](https://leetcode.cn/circle/discuss/2Gdn7F/view/43FuHN/)
思路2: #贪心 #构造
    从 #贪心 交换开始, 更加直观, 见 灵神视频. 
    更为直接的想法: 先统计出 arr1, arr2 中需要被取出的数字集合! 
    如何交换它们? 贪心来说, 对它们排序, 反向组合! 再考虑利用中间变量mn的方式! 具体见代码
    [灵神](https://leetcode.cn/problems/rearranging-fruits/solution/tan-xin-gou-zao-by-endlesscheng-c2ui/)
"""
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        cnt1 = Counter(basket1); cnt2 = Counter(basket2)
        cnt = cnt1 + cnt2
        # 判断是否可行
        for k,v in cnt.items():
            if v%2: return -1
            cnt[k] //= 2
        # 需要交换的数量
        swaps = 0
        for x,c in cnt.items():
            swaps += abs(c-cnt1[x])
        swaps //= 2
        # 只需要考虑前一半
        ans = 0
        mn = min(cnt.keys())
        for x in sorted(cnt):
            diff = abs(cnt[x]-cnt1[x])
            if diff < swaps:
                ans += min(2*mn, x)*diff
                swaps -= diff
            else:
                ans += min(2*mn, x)*swaps
                break
        return ans
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        # 思路2: 从 #贪心 交换开始, 更加直观, 见 灵神视频. 
        cnt = Counter()     # 只用一个cnt的技巧
        for x,y in zip(basket1, basket2):
            cnt[x] += 1
            cnt[y] -= 1
        # 
        for x,c in cnt.items():
            if c%2: return -1
        # 得到两个数组中需要取出的元素 (交换)
        out1, out2 = [], []
        for x,c in cnt.items():
            if c>0: out1 += [x] * (c//2)
            elif c<0: out2 += [x] * (-c//2)
        # 贪心: 反向匹配
        out1.sort()
        out2.sort(reverse=True)
        mn = min(cnt)
        return sum(min(x,y, 2*mn) for x,y in zip(out1, out2))
    
sol = Solution()
result = [
    # sol.vowelStrings(words = ["aba","bcb","ece","aa","e"], queries = [[0,2],[1,4],[1,1]]),
    # sol.minCapability(nums = [2,3,5,9], k = 2),
    # sol.minCapability(nums = [2,7,9,3,1], k = 2),
    # sol.pickGifts(gifts = [25,64,9,4,100], k = 4),
    # sol.pickGifts([1,1,1,1],10),
    sol.minCost(basket1 = [4,2,2,2], basket2 = [1,4,1,2]),
    sol.minCost(basket1 = [2,3,4,1], basket2 = [3,2,5,1]),
]
for r in result:
    print(r)
