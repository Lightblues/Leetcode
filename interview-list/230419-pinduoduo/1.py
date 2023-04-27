""" 
统计棱形的数量, 满足所有点的横坐标满足 0<=x<=X, 0<=y<=Y, 并且对称轴平行于坐标轴
思路1: 数学
    横坐标之差显然需要是偶数, 枚举长度为 2,4,...X 的棱形
        计数平行X的对称轴可能的数量: X-1 + X-3 + ...
    对于横轴高度为y的棱形, 它能够匹配的棱形数量为 min( y, Y-y )
"""
x,y = map(int, input().split())
factor = 0
x -= 1
while x > 0:
    factor += x
    x -= 2
ans = 0
for i in range(y):
    ans += min(i, y-i) * factor
print(ans)