def longest_increasing_subsequence(arr):
    n = len(arr)
    # dp[i]表示以第i个元素结尾的最长递增子序列长度
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    # 找到dp中的最大值即为最长递增子序列长度
    max_length = max(dp)
    
    # 从dp中找到最长递增子序列的元素
    lis = []
    for i in range(n - 1, -1, -1):
        if dp[i] == max_length:
            lis.append(arr[i])
            max_length -= 1
    
    return lis[::-1]  # 反转列表，得到正序的最长递增子序列

# 示例输入
input_sequence = [10, 22, 9, 33, 21, 50, 41, 60, 80]
result = longest_increasing_subsequence(input_sequence)
print("最长递增子序列:", result)