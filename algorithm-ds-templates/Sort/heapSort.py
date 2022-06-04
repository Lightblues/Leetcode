import heapq

""" 堆排序
1. 建立一个堆;
2. 每次从堆中取出最大的元素;
 """

def heap_sort(lst):
    heapq.heapify(lst)
    return [heapq.heappop(lst) for i in range(len(lst))]

data = [1,5,3,2,8,5]
print(data)
print(heap_sort(data))