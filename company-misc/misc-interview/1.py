""" 
返回top-K

 """

# def topK(i,j,k):
#     if i == j:
#         return [i]
#     m = (i+j)//2
#     left = topK(i,m,k)
#     right = topK(m+1,j,k)
#     return merge(left,right,k)

def topK(arr, k):
    """ 返回top-K的元素 """
    n = len(arr)
    def merge(i,j,k):
        if i == j:
            return [i]
        m = (i+j)//2
        left = merge(i,m,k)
        right = merge(m+1,j,k)
        return merge(left,right,k)
    return merge(0,n-1,k)

def quick_select(nums, L, R, k):
    """快速选择, 返回 nums 中第 k 大的数 (k 从 0 开始)."""
    t = L
    nums[t], nums[R] = nums[R], nums[t]
    left, idx = L - 1, L
    while idx < R:
        if nums[idx] > nums[R]:
            left += 1
            nums[left], nums[idx] = nums[idx], nums[left]
        idx += 1
    left += 1
    nums[left], nums[R] = nums[R], nums[left]
    if left == k:
        return nums[left]
    elif left > k:
        return quick_select(nums, L, left - 1, k)
    elif left < k:
        return quick_select(nums, left + 1, R, k)


def findKthLargest(nums, k: int) -> int:
    return quick_select(nums, 0, len(nums) - 1, k - 1)


print(findKthLargest([1,2,3,4,5,6,7,8,9], 3))