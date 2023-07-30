""" 给定长度为n的不同货币, 要求构成aim的最小数量
限制: aim 5e3, n 1e4, 要求时间 O(n * aim), 空间 O(aim)
思路1: #DP 
    记 f(x) 表示构成x的最小数量, 则有转移 f(x) = min(f(x-coin) for coin in coins) + 1
    边界: f(0) = 0
"""

def minCoins(arr, aim):
    """  """
    dp = [0] + [float('inf')] * aim
    for i in range(1, aim+1):
        dp[i] = min([dp[i-coin] if i-coin>=0 else float('inf') for coin in arr]) + 1
    return dp[-1] if dp[-1] != float('inf') else -1

n, aim = map(int, input().split())
arr = list(map(int, input().split()))
print(minCoins(arr, aim))
