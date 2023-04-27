""" 压缩表示
有M个维度, 每个维度的取值有Mi种可能; 对于T个配置情况进行压缩表示, 每个配置情况有一个值Ti. 问这些配置行可以被压缩成最少多少行
限制: M 5; Mi 5; T 20; Ti 100. 
"""
M = int(input())
filed2keys = {}
for i in range(M):
    line = input().split()
    filed2keys[i] = line[1:]
T = int(input())
items = {}
for _ in range(T):
    line = input().split()
    items[tuple(line[:-1])] = int(line[-1])

