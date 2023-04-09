""" 换座位
n行, m大列, a小列. 每次换到下一行, 下一大列的相同小列上. 对于0/1高度, 判断多少需要调整的. 
限制: n,m 200; a 5

"""
n,m,a = map(int, input().split())
seats = []
for _ in range(n):
    seats.append(list(input().strip().replace(" ", "")))
ans = 0
for i in range(n):
    for j in range(m*a):
        ni = (i+1)%n
        nj = (j+a)%(m*a)
        if seats[i][j] != seats[ni][nj]:
            ans += 1
print(ans)

