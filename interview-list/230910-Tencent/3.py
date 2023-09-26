""" 
一组里面的元素, 定义了连接关系. 给定一个删除顺序, 问每次删除之后的分割(团的)数量. 
    定义的连接关系是: 两个字符串的最大公共子序列长度 >=k
限制: n 500
思路1: 逆序构建, 用 #并查集 维护.
"""
n,k = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(input().strip())
deleteOrder = list(map(int, input().split()))
deleteOrder = [i-1 for i in deleteOrder][::-1]

def check(s,t):
    """ 计算两个字符串的最长公共子序列 """
    dp = [[0]*(len(t)+1) for _ in range(len(s)+1)]
    for i in range(1,len(s)+1):
        for j in range(1,len(t)+1):
            if s[i-1]==t[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i][j-1], dp[i-1][j])
    return dp[-1][-1] >= k
# print(check('abc','ab'))
# print(check('abc','aca'))

fa = list(range(n))
n_group = n
ans = [0]
for i,idx in enumerate(deleteOrder):
    for j in range(i):
        if check(arr[idx], arr[deleteOrder[j]]):
            if fa[idx] != fa[deleteOrder[j]]:
                n_group -= 1
                fa[idx] = fa[deleteOrder[j]]
    ans.append(n_group - (n-i-1))
for i in ans[::-1]:
    print(i)