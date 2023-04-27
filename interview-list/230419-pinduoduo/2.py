""" 
平面上一组点, 横坐标x给定, 只能交换一组y值, 使得其和X轴围成的面积最大; 若不需要交换则返回-1
限制: n 1e3
思路1: 暴力枚举
    注意到, 对于梯形 (位置为i的高和i-1,i+1构成了两个矩阵), 它的高度变化, 造成的 delta面积仅仅由两遍的梯形高度决定
        也即, dS = 1/2 * (w[i-1]+w[i+1]) * dh
"""
n = int(input())
points = []
for _ in range(n):
    points.append(list(map(int, input().split())))
points.sort()
# 宽度
w = [0] + [points[i][0] - points[i-1][0] for i in range(1,n)] + [0]
mx = 0; ans = None
for i in range(n):
    for j in range(i+1,n):
        hi,hj = points[i][1], points[j][1]
        # 计算面积
        dS = (w[i]+w[i+1]) * (hj-hi) + (w[j]+w[j+1]) * (hi-hj)
        if dS > mx:
            mx = dS
            ans = (points[i][0], points[j][0])
if mx==0: print(-1)
else: print(*ans)