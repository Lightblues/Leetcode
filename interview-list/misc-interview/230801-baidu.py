def findKthLargest(nums, k: int) -> int:
    # 快速选择
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
        
    def quickselect(arr, l, r, k):
        # 返回arr[l,r] 中第k大的元素
        i = partition(arr, l, r)
        if i==k:
            return arr[i]
        elif i<k:
            return quickselect(arr, i+1, r, k)
        else:
            return quickselect(arr, l, i-1, k)
    return quickselect(nums, 0, len(nums)-1, len(nums)-k)    # 从小到大的n-k个数字

print(
    findKthLargest([1,2,3,4,5], 2)
)


from heapq import heappop, heappush


def findMedian(arr) -> float:
    mn = []
    mx = []
    def addNum(num: int) -> None:
        if mn and num < -mn[0]:
            heappush(mn, -num)
            if len(mn) > len(mx)+1:
                heappush(mx, -heappop(mn))
        else:
            heappush(mx, num)
            if len(mx) > len(mn):
                heappush(mn, -heappop(mx))

    def get():
        if len(mn)==len(mx): return (-mn[0]+mx[0])/2
        else: return -mn[0]
        
    for x in arr:
        addNum(x)
        print(get())
findMedian([1,2,3,4,5]),

print(
    findMedian([1,2,3,4,5]),
    findMedian([1,2,3,4,5,6]),
)
