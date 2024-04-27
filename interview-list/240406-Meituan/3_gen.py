from itertools import accumulate
n = 5
arr = [1,2,3,4,5]
i,j = 1,3
arr1 = arr[:]
arr1.pop(i)
acc1 = list(accumulate(arr1))
arr2 = arr[:]
arr2.pop(j)
acc2 = list(accumulate(arr2))
print(n)
print(" ".join(map(str, acc1)))
print(" ".join(map(str, acc2)))