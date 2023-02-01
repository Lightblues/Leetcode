from easonsi import utils
from easonsi.util.leetcode import *
import random
import time

""" 
== 快速排序
0075. 颜色分类 #medium #题型
    有3种颜色, 要求「原地」修改使得数组变为有序的状态.
0215. 数组中的第K个最大元素 #medium #题型 #star
    给定一个数组, 要求返回其中第k大的元素.
    思路1: 维护一个大小为k 的 最小 #堆
    思路2: #快速选择, 基于 #快速排序
0347. 前 K 个高频元素 #medium #题型
    给定一个数组, 返回其中出现频次前k高的元素. 题目保证了答案唯一. 要求复杂度小于 O(n logn)
    注意这里只需要得到前k大的元素而不需要完整排序, 因此每次期望减半, 复杂度 O(n)

"""
class Solution():



    """ 0215. 数组中的第K个最大元素 #medium #题型 #star 
[另见 sliding Window 的循环不变量部分]
给定一个数组, 要求返回其中第k大的元素.
限制: 数组长度 1e5
思路1: 维护一个大小为k 的 最小 #堆
    复杂度: O(n logk)
思路2: #快速选择, 基于 #快速排序
    基本思路是, 每次选择一个pivot, 将数组元素按照相较pivot的大小关系分成两边.
    具体而言, 需要实现 `partition(arr, l,r)` 在 `arr[l...r]` 中随机选择一个pivot, 并返回其下标.
    复杂度: 平均复杂度 `O(n)`, 最坏情况下 `O(n^2)`. 为此, 在选择pivot的时候可以增加 random.
    具体见 [官答](https://leetcode.cn/problems/kth-largest-element-in-an-array/solution/shu-zu-zhong-de-di-kge-zui-da-yuan-su-by-leetcode-/)
从 #循环不变量 的角度, 另见 [here](https://leetcode.cn/leetbook/read/sliding-window-and-two-pointers/rli5s3/)
"""
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 推排序
        h = nums[:k]
        heapify(h)
        for num in nums[k:]:
            if num>h[0]:
                heappushpop(h, num)
        return h[0]
            
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 快速选择
        random.seed(time.time())
        def partition(arr, l,r):
            # 选择 arr[r] 作为 pivot, 进行划分.
            x = arr[r]  # pivot
            i = l-1     # 记录最右边的 <=x 的位置
            for j in range(l, r):
                if arr[j]<=x:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            i += 1
            arr[i], arr[r] = arr[r], arr[i]
            return i
        def randomPartition(arr, l, r):
            # 在partition的基础上, 随机选择一个位置作为 pivot.
            idx = random.randint(l, r)
            arr[idx], arr[r] = arr[r], arr[idx]
            return partition(arr, l, r)
        
        def quickselect(arr, l, r, k):
            # 返回arr中第k大的元素
            # i = partition(arr, l, r)
            i = randomPartition(arr, l, r)
            if i==k:
                return arr[i]
            elif i<k:
                return quickselect(arr, i+1, r, k)
            else:
                return quickselect(arr, l, i-1, k)
        
        return quickselect(nums, 0, len(nums)-1, len(nums)-k)
    
    """ 0347. 前 K 个高频元素 #medium #题型
给定一个数组, 返回其中出现频次前k高的元素. 题目保证了答案唯一. 要求复杂度小于 O(n logn)
思路1: 对于计数的结果, 要求得到 「 #topK」, 经典可以用 #堆 解决
    复杂度: O(n logk)
思路2: 对于「topK」问题, 另一个经典解法是 #快排.
    注意这里只需要得到前k大的元素而不需要完整排序, 因此每次期望减半, 复杂度 O(n)
"""
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        h = []  # (cnt, num)
        for a,c in cnt.items():
            if len(h)==k:
                if h[0][0] < c: heappushpop(h, (c,a))
                else: continue
            else: heappush(h, (c,a))
        return [a for c,a in h]
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 思路2: 快排. 注意这里指需要得到前k大的元素而不需要完整排序, 因此每次期望减半, 复杂度 O(n)
        def swep(i,j): cnt[i],cnt[j] = cnt[j],cnt[i]
        def qsort(l,r,k):
            # 对于 [l...r] 区间, 保证前k个元素是最大的.
            if l>=r: return
            # 引入随机
            picked = random.randint(l,r)
            # 选择最后一个作为pivot
            swep(r,picked)
            pivot = cnt[r][0]
            idx = l     # [l...idx) > pivot. idx 是下一个要被填入的位置.
            for i in range(l,r):
                if cnt[i][0]>pivot:
                    swep(i,idx)
                    idx += 1
            swep(idx,r)
            # [l...idx] 位置是最大的 idx-l+1 个元素.
            # k = idx-l+1 / idx-l 都不用再递归了.
            if idx-l>k: qsort(l,idx-1,k)
            elif idx-l+1<k: qsort(idx+1,r,k-(idx-l+1))
        cnt = Counter(nums)
        cnt = [(c,a) for a,c in cnt.items()]
        qsort(0, len(cnt)-1, k)
        return [a for c,a in cnt[:k]]
    
    
    


sol = Solution()
result = [
    # sol.findKthLargest([3,2,1,5,6,4], k = 2),
    # sol.topKFrequent([3,0,1,0], 1),
    # sol.topKFrequent(nums = [1,1,1,2,2,3], k = 2),
    
]
for r in result:
    print(r)