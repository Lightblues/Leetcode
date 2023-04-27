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
https://leetcode.cn/contest/weekly-contest-187

T3 之前写过了, 重新写一遍居然还挺顺; T4用一开始的比较基本的思路还挺顺的, 但很多答案中提到的二分思路, 其中的计数函数比较玄学...

todo: [多路归并技巧总结](https://leetcode.cn/problems/find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows/solution/by-lfool-z9n4/) 

@2022 """
class Solution:
    """ 1436. 旅行终点站 """
    def destCity(self, paths: List[List[str]]) -> str:
        cin, cout = set(), set()
        for u,v in paths: cin.add(v); cout.add(u)
        dest = cin.difference(cout)
        return dest.pop()
    
    """ 1437. 是否所有 1 都至少相隔 k 个元素 """
    def kLengthApart(self, nums: List[int], k: int) -> bool:
        idx = -k-1
        for i,num in enumerate(nums):
            if num==1:
                if i-idx<=k: return False
                idx = i
        return True
    
    """ 1438. 绝对差不超过限制的最长连续子数组 #medium 对于一个子数组, 定义「绝对差」为最大最小元素的差距. 在绝对差限制 limit的条件下, 求最长的合法子数组. 限制: n 1e5
思路1: #双指针+两个 #最大最小堆
    维护区间内的最大最小值.
    如何维护? 一种思路是建立最大最小堆. 然后在推移l指针的过程中, 将过期元素丢掉.
    一种更 #优雅 的方案是, 采用 #单调队列. 这是因为, **在维护窗口的过程中, 对于可能成为窗口最大值的元素, 我们仅需要用一个递减栈来记录, 其他元素不可能成为最大值.** 参见 [sildingWindow]
思路0: #有序集合 暴力 复杂度 O(n logn)
思路3: #单调队列, 见 [mono-deque]
"""
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # 思路1: #双指针+两个 #最大最小堆
        l = 0; ans = 1
        mx, mn = [], []
        def popOutdated():
            # aux 将过期的元素从堆中弹出
            while mx and mx[0][1]<l: heappop(mx)
            while mn and mn[0][1]<l: heappop(mn)
        for r, num in enumerate(nums):
            heappush(mn, (num, r)); heappush(mx, (-num, r))
            popOutdated()
            while -mx[0][0]-mn[0][0]>limit:
                l += 1
                popOutdated()
            ans = max(ans, r-l+1)
        return ans
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # 思路1: #有序集合 暴力 复杂度 O(n logn)
        s = SortedList()
        n = len(nums)
        left = right = ret = 0
        while right < n:
            s.add(nums[right])
            while s[-1] - s[0] > limit:
                s.remove(nums[left])
                left += 1
            ret = max(ret, right - left + 1)
            right += 1
        return ret

    """ 1439. 有序矩阵中的第 k 个最小数组和 #hard #题型 矩阵的每一行都是非递减的. 拿取的规则是从每一行那一个元素, 要求得到数字和第 k小的. 限制: m,n 40.  k 200
思路1: 利用 最小堆 遍历到第k小
    所有可能的选择方式较多, 我们仅考虑「当前可能最小的选择」. 显然, 假如当前的选择列分别为 [0,0,0], 则此小的选择只可能在 `[1,0,0], [0,1,0], [0,0,1]` 中. 
    因此, 维护一个 #最小堆. 同时记录当前值所对应的 idx. 每次选择后, 拓展idx的边界即可.
思路2: #二分. 显然可取的 mn,mx 是确定的, 可以在这一范围内进行二分搜索.
    所以, 可以是「给定x, 判断可选的方案数是否大于等于k」. 
        这可以通过 DFS 暴力解 (第一行选 0...n-1, 第二行选 0...n-1, ...).
        注意 #剪枝 ! 利用这里的k的数字范围较小的特点进行剪枝.
参见 [here](https://leetcode.cn/problems/find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows/solution/go-xiao-ding-dui-shuang-bai-by-flare-dlcmc/)
"""
    def kthSmallest(self, mat: List[List[int]], k: int) -> int:
        m,n = len(mat), len(mat[0])
        # 
        idx = tuple([0]*m)      # idx: 当前所选的列组合
        queue = [(sum(r[0] for r in mat), idx)]
        seen = set([idx])       # 已选过的列组合
        for _ in range(k):
            v, idx = heapq.heappop(queue)
            for r,ix in enumerate(idx):
                if ix+1<n:
                    nidx = tuple(list(idx[:r])+[ix+1]+list(idx[r+1:]))      # 注意转为 tuple 以进行hash.
                    if nidx in seen: continue
                    seen.add(nidx)
                    heapq.heappush(queue, (v-mat[r][ix]+mat[r][ix+1], nidx))
        return v
    def kthSmallest(self, mat: List[List[int]], k: int) -> int:
        # 思路2: 二分. 这里的计数好玄学... 第一种写出来 #TLE 了
        m,n = len(mat), len(mat[0])
        
        def getCount(x, row=0, curSum=0):
            # 注意! 这样写会超时.
            # 给定x, 判断 <=x 的可选方案数
            cnt = 0
            for col in range(n):
                s = curSum + mat[row][col]
                if s>x: break
                cnt += getCount(x, row+1, s) if row+1<m else 1
                # 剪枝!!
                if cnt>k: break
            return cnt
        def getCount(x, row=0, curSum=0):
            # 给定x, 判断 <=x 的可选方案数
            nonlocal cnt
            if curSum>x or row>=m: return
            if cnt > k: return
            getCount(x, row+1, curSum)
            for i in range(1, n):
                s = curSum-mat[row][0]+mat[row][i]
                if s>x: break
                cnt += 1
                getCount(x, row+1, s)
            # return cnt
            
        l, r = sum(r[0] for r in mat), sum(r[-1] for r in mat)
        init = l; 
        ans = None
        while l<=r:
            mid = (l+r)//2
            cnt = 1
            # cnt = getCount(mid, 0, 0)
            getCount(mid, 0, init)
            # 何时记录ans? 由于 getCount 返回的是 「大于等于x的数量」, 而我们要求的是第k小. 因此归并成 `cnt>=k` 的逻辑中停止即可.
            if cnt>=k: ans = mid;  r = mid-1
            else: l = mid+1
        return ans
    
        
        
sol = Solution()
result = [
    # sol.destCity(paths = [["B","C"],["D","B"],["C","A"]]),
    # sol.kthSmallest(mat = [[1,3,11],[2,4,6]], k = 5),
    # sol.kthSmallest(mat = [[1,3,11],[2,4,6]], k = 9),
    # sol.kthSmallest([[1,1,10],[2,2,9]], 7),
    sol.longestSubarray(nums = [8,2,4,7], limit = 4),
    sol.longestSubarray(nums = [10,1,2,4,7,2], limit = 5),
]
for r in result:
    print(r)
