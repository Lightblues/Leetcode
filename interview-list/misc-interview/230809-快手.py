""" 找到数组中的前k个最大的数 """

def partition(arr, i,j):
    # 分割 arr[i:j+1], 返回分割点
    pivot = arr[i]
    pointer = i
    for idx in range(i+1,j+1):
        if arr[idx] > pivot:
            # 这里有一些Magic逻辑!
            arr[idx],arr[pointer] = arr[pointer+1],arr[idx]
            pointer += 1
    arr[pointer] = pivot
    return pointer

def f(arr, k):
    # 二分维护待排序区间
    l,r = 0,len(arr)-1
    while l<r:
        m = partition(arr, l,r)
        if m>k: r = m-1
        else: l = m+1
    return arr[:k]

arr = [1,2,3,4,5]
arr = [1,3,4,2,5,4]
print(
    f(arr, 4),
    f(arr, 3),
    f(arr, 2),
    f(arr, 1)
)