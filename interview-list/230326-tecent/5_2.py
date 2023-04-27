""" 
一个 (W,H) 的木板, 给定一组斜率为 1/-1 的切割线, 问最终得到多少块小木板. 限制: W,H 500; n 1e3

思路1: #数学 先画图模拟一下! 
    对于一条切割线, 它的位置仅仅由它个木块边界的两个交点决定! 此外, 我们可以根据 1/-1 和切线与y轴的截距分成两组
    注意到, (不重复的) k条斜率为1的切线将木块分成k+1块; 然后, 对于每条斜率为-1的切线, 若它和斜率为1的切线的交点数量为x, 则会新增x+1个木块
    因此: 问题在算 y=x+a; y=-x+b 的交点为 1/2*(b-a, b+a)
 """
h,w = map(int, input().split())
g1, g2 = [], []
m = int(input())
for _ in range(m):
    x1,y1, x2,y2 = map(int, input().split())
    if int((y2-y1) / (x2-x1))==1:
        if y1-x1 in g1:
            g1.add(y1-x1)
    else:
        if y1+x1 in g1:
            g2.add(y1+x1)
ans = 1 + sum(1 for y in g1 if -w<y<h)
for b in g2:
    if not 0<b<h+w: continue
    acc = 1
    for a in g1:
        xx,yy = (b-a)/2, (b+a)/2
        if 0<xx<w and 0<yy<h: acc += 1
    ans += acc
print(ans)

