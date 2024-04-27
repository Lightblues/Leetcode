""" 
恢复数组 | 对于一个未知数组 arr, 有两个丢失的元素, 分别计算他们的前缀和, 现在要求恢复原数组. 保障了该数组是可以被恢复的. 
思路1: 
    分别对于前缀数组计算 diff, 注意对于两个对应的位置 i,j 只可能出现 j = i-1/i/i+1 三种情况. 
    NOTE: 「可被恢复」, 意味着被删掉的两个元素不是相邻的. 

4
8 18 14
15 9 1
# 1 8 6 4

5
1 4 8 13
1 3 6 11
"""
from math import inf
n = int(input())
acc1 = list(map(int, input().strip().split()))
acc2 = list(map(int, input().strip().split()))
acc1.sort(); acc2.sort()
diff1 = [acc1[i+1]-acc1[i] for i in range(n-2)]     # n-2
diff2 = [acc2[i+1]-acc2[i] for i in range(n-2)]
condition = -1  # 0: acc1, 1: acc2
i = j = 0
arr = []
diff1.append(inf); diff2.append(inf)
while i<n-2 or j<n-2:
    if diff1[i]==diff2[j]:
        arr.append(diff1[i])
        i,j = i+1,j+1
    else:
        if condition==-1:
            if j<n-3 and diff1[i]==diff2[j+1]:      # acc1 miss first
                arr.append(diff2[j])
                arr.append(diff1[i])
                condition = 0
                i,j = i+1,j+2
            else:
                arr.append(diff1[i])
                arr.append(diff2[j])
                condition = 1
                i,j = i+2,j+1
        elif condition==0:
            arr.append(diff1[i])
            i += 1
        else:
            arr.append(diff2[j])
            j += 1
# 注意加上一开始的元素
if condition==0:
    arr = [acc2[0]] + arr
else:
    arr = [acc1[0]] + arr
print(' '.join(map(str, arr)))
