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
Easonsi @2023 """
class Solution:
    """
    Merge sort
    """
    def mergeSort(self, arr):
        print("Splitting ", arr)
        if len(arr) > 1:
            mid = len(arr)//2
            lefthalf = arr[:mid]
            righthalf = arr[mid:]

            self.mergeSort(lefthalf)
            self.mergeSort(righthalf)

            i = 0
            j = 0
            k = 0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i] < righthalf[j]:
                    arr[k] = lefthalf[i]
                    i = i+1
                else:
                    arr[k] = righthalf[j]
                    j = j+1
                k = k+1

            while i < len(lefthalf):
                arr[k] = lefthalf[i]
                i = i+1
                k = k+1

            while j < len(righthalf):
                arr[k] = righthalf[j]
                j = j+1
                k = k+1
            print("Merging ", arr)


    """
    Quick sort
    """
    def quickSort(self, arr: list):

        def quickHelper(arr: list, first: int, last: int):
            if first < last:
                splitpoint = partition(arr, first, last)
                quickHelper(arr, first, splitpoint - 1)
                quickHelper(arr, splitpoint + 1, last)

        # def partition(self, arr: list, first: int, last: int):
        #     pivot = arr[first]
        #     left = first + 1
        #     right = last
        #
        #     done = False
        #     while not done:
        #         while left <= right and arr[left] <= pivot:
        #             left = left + 1
        #         while arr[right] >= pivot and right >= left:
        #             right = right - 1
        #         if right < left:
        #             done = True
        #         else:
        #             temp = arr[left]
        #             arr[left] = arr[right]
        #             arr[right] = temp
        #     temp = arr[first]
        #     arr[first] = arr[right]
        #     arr[right] = temp
        #
        #     return right

        # 自己按照《算法导论》实现了一下
        def partition(arr: list, first: int, last: int):
            pivot = arr[last]       # 选定最后一个元素为 pivot
            le_pivot = first-1      # 指针，在遍历过程中满足 le_pivot 及其右侧的元素 <=pivot
            for i in range(first, last):
                if arr[i] <= pivot:
                    le_pivot += 1
                    arr[le_pivot], arr[i] = arr[i], arr[le_pivot]
            # 最后 pivot 和 le_pivot+1 位置进行交换
            arr[le_pivot+1], arr[last] = arr[last], arr[le_pivot+1]
            return le_pivot+1

        quickHelper(arr, 0, len(arr) - 1)
        
    def testQuickSort(self):
        arr = [4, 5, 6, 3, 2, 1]
        print("before:", arr)
        self.quickSort(arr)
        print("after:", arr)
    
    
    
    
    
    

    
sol = Solution()
result = [
    sol.testQuickSort(),
    
]
for r in result:
    print(r)
