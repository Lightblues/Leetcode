""" C. Where's the Bishop?
在一个8*8的棋盘上, 标注了一个象可以走的所有位置, 要求找到该棋子的位置.
限制: 象不在四边 (也即坐标在 [2,7] 之间)
思路1: #模拟 #归纳
    由于不在四边, 从上往下看每一行象可达的数量, 可以象所在行可达1个位置, 上面一行一定是2个位置.
    
例子
.....#..
#...#...
.#.#....
..#.....
.#.#....
#...#...
.....#..
......#.
"""
def f():
    input()
    flag = False
    ans = None
    for i in range(8):
        line = input().strip()
        c = line.count('#')
        if c == 2: flag = True
        if c==1 and flag and ans is None: ans = (i, line.index('#'))
    print(ans[0]+1, ans[1]+1)

n = int(input())
for _ in range(n):
    f()
