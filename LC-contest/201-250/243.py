from http import server
import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re
from numpy import real

# https://github.com/grantjenks/python-sortedcontainers
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-243
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1880. 检查某单词是否等于两单词之和  """
    def isSumEqual(self, firstWord: str, secondWord: str, targetWord: str) -> bool:
        first = [ord(ch)-ord('a') for ch in firstWord]
        second = [ord(ch)-ord('a') for ch in secondWord]
        target = [ord(ch)-ord('a') for ch in targetWord]
        first = int("".join(map(str, first)))
        second = int(''.join(map(str, second)))
        target = int(''.join(map(str, target)))
        return first+second == target
    
    """ 1881. 插入后的最大值 """
    def maxValue(self, n: str, x: int) -> str:
        l = len(n)
        x = str(x)
        if n[0]=='-':
            idx = 1
            while idx<l and n[idx] <= x:
                idx += 1
        else:
            idx = 0
            while idx<l and n[idx] >= x:
                idx += 1
        return n[:idx]+x+n[idx:]
    
    """ 1882. 使用服务器处理任务 #medium 关联 1834
有一组tasks, 每个所需的时间为 tasks[i]. 还有一组servers, 每个的权重为servers[i]. 任务按照第 0,1,2,... 的顺序到达, 每次从空闲的服务器中选择权重最小的来处理. 问每个任务被分配到的服务器的编号.
思路1: 用两个 #最小堆 分别记录空闲的机器 (根据服务器权重) 和正在运行/busy的机器 (根据结束时间排序)
    关键是如何处理时刻t没有空余机器的情况? 
    1) 官答中给的思路是, 顺序遍历tasks! 在遍历过程中 (用一个for循环), 维护一个全局的ts变量, 记录下一个空闲机器的时间 (定义了一个release函数释放释放在ts及其之前结束的机器); 若当前任务到达时没有idle机器, 则设置ts为最近的一个结束时间.
    2) 自己一开始的想法: 用一个队列tasksQue 记录待处理的任务. 和上面的区别在于, 遍历tasks之后可能有任务没有进行处理, 最后需要再处理tasksQue中剩余的任务. 稍微复杂一点.
    复杂度: 在顺序处理n个任务的时候, 我们需要将ts之前结束的机器释放, 但注意到会执行任务的机器一共只有n个, 因此复杂度最多为 `O(n log(n))`. 这是粗糙的分析, 详见 [官答](https://leetcode.cn/problems/process-tasks-using-servers/solution/process-tasks-using-servers-by-leetcode-rot1m/)
"""
    def assignTasks(self, servers: List[int], tasks: List[int]) -> List[int]:
        # 思路 1.2
        serversAva = [(score,i) for i,score in enumerate(servers)]
        serversUsed = []
        heapify(serversAva)
        ans = [-1] * len(tasks)
        tasksQue = deque()
        for time,task in enumerate(tasks):
            while serversUsed and serversUsed[0][0] <= time:
                _,score,sidx = heappop(serversUsed)
                heappush(serversAva, (score,sidx))
            tasksQue.append((time,task))
            while tasksQue and serversAva:
                i,tt = tasksQue.popleft()
                score,sidx = heappop(serversAva)
                ans[i] = sidx
                heappush(serversUsed, (tt+time,score,sidx))
        # 还有剩余任务, 此时 serversAva 为空
        while tasksQue:
            i,task = tasksQue.popleft()
            stime,score,sidx = heappop(serversUsed)
            ans[i] = sidx
            heappush(serversUsed, (task+stime,score,sidx))
        return ans
    def assignTasks_v2(self, servers: List[int], tasks: List[int]) -> List[int]:
        """ [官答](https://leetcode.cn/problems/process-tasks-using-servers/solution/process-tasks-using-servers-by-leetcode-rot1m/) """
        idle = [(score, i) for i,score in enumerate(servers)]; heapify(idle)
        busy = []
        ans = [-1] * len(tasks)
        
        def release(ts):
            # 释放在ts及其之前结束的机器
            while busy and busy[0][0]<=ts:
                _, idx = heappop(busy)
                heappush(idle, (servers[idx], idx))
        ts = 0  # 全局变量, 记录下一个task开始被处理的时间 (因为可能需要等待)
        for time, task in enumerate(tasks):
            # 第i个task在 time 时刻开始等待处理
            release(time)
            ts = max(ts, time)
            # 若没有空闲机器, 则等待 —— 更新 ts
            if not idle:
                ts =busy[0][0]
                release(ts)
            _, idx = heapq.heappop(idle)
            ans[time] = idx
            heappush(busy, (ts+task, idx))
        return ans
    
    
    """ 1834. 单线程 CPU #medium
给定一组tasks, 每个任务是开始时间和需要运行的时间. 现在只有一个CPU, 会选择任务队列中运行时间最短的那一个执行. 问CPU处理的任务顺序
约束: 任务数量 1e5; 任务时间 1e9
提示: 维护一个 #最小堆 记录当前待运行的任务
思路1: 如何维护其他还没进入等待队列的任务? 可以对开始时间进行排序.
    具体而言, 可以用一个指针来记录已入对的任务数量. 如下.
    在写的时候用的是 pop(0) 发现超时了, 因为要注意Python中这一操作的复杂度为 O(N)!
思路2: 除了进行 #排序, 也可以还是用 #堆 来实现「取出ts时刻之前的task」这一任务.
细节: 如何实现对于所有任务进行遍历执行? 
总结: 尽量少使用 pop(0) 操作, 其复杂度为 O(N) !! 可以用 `deque` 替代
"""
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        n = len(tasks)
        tasks = [(start, task, i) for i,(start, task) in enumerate(tasks)]; tasks.sort()
        taskQueue = []
        ans = []
        # 注意, 用pop写会超时!!
        # def release(ts):  
        #     while tasks and tasks[0][0] <= ts:
        #         _, task, i = tasks.pop(0)
        #         heappush(taskQueue, (task, i))
        def release(ts):
            nonlocal ptr
            while ptr<n and tasks[ptr][0] <= ts:
                heappush(taskQueue, (tasks[ptr][1], tasks[ptr][2]))
                ptr += 1
        ts = 1
        ptr = 0
        for _ in range(n):
            # 循环条件: 这里不好判断了, 直接遍历n次
            release(ts)
            if not taskQueue:
                ts = tasks[ptr][0]
                release(ts)
            task, i = heappop(taskQueue)
            ans.append(i); ts += task
        return ans
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        # 采用 heap 来实现, 就不会超时
        tasks = [(start, task, i) for i,(start, task) in enumerate(tasks)]; heapify(tasks)
        taskQueue = []
        ans = []; ts = 1
        def release(ts):
            while tasks and tasks[0][0] <= ts:
                _, task, i = heappop(tasks)
                heappush(taskQueue, (task, i))
        while tasks or taskQueue:
            # 循环条件: 还有任务待执行, 或者还有没入队列的任务
            release(ts)
            if not taskQueue:
                ts = tasks[0][0]
                release(ts)
            task, i = heappop(taskQueue)
            ans.append(i); ts += task
        return ans


    """ 1883. 准时抵达会议现场的最小跳过休息次数 #hard
你需要在时间限制hoursBefore前经过n条路到达会场, 你的速度给定, 每条路的长度不同; 走完一条路之后, 一般情况下需要休息到整数时刻走下一条路. 在路口你可以选择「跳过」操作直接走下一条路. 问为了在时间限制内到达最少需要多少次跳过操作?
限制: n 1e3; 每条路长度 1e5, 速度 1e6, hoursBefore 1e7
思路1 #DP
    表示: `f[i][j]` 表示通过前i条路, 最多用j次跳过的最短时间. 结果范围 f[n] 中时间小于 hoursBefore 最小的j即可.
    递推: `f[i][j] = min{ ceil(f[i-1][j]+dist[i]/speed), f[i-1][j-1]+dist[i]/speed }` 第一项表示已经用满了j次机会, 因此需要上取整; 第二项表示这次使用跳过.
    关于 **浮点数**: 注意浮点数的运算是有精度的, 例如在Python中 `ceil(8.0 + 1.0 / 3 + 1.0 / 3 + 1.0 / 3)` 因为误差会, 加法的结果会比9大一点, 最后得到了错误的取整结果10. 错误的用例: 路段长度都是 100000 速度 75000, 每次的浮点数都是 1/3左右, 所以会有误差.
        在本题中, 为了避免这一问题, 可以在加法操作后减去一个不影响的数值EPS, 从而避免由于精度带来的误差. 例如, 这里路径长度为整数, 而速度最大为 1e6 量级, 因此实际计算的时间的最小量级在 1e-6 以内, 我们可以取 EPS=1e-7.
        参见[官答](https://leetcode.cn/problems/minimum-skips-to-arrive-at-meeting-on-time/solution/minimum-skips-to-arrive-at-meeting-on-ti-dp7v/)
    除了上述技巧, 还可以 **将浮点数运算转为整数**, 从而避免上述问题.
        也即, 用 `f[i][j]` 表示对应的时间内人没有阻碍可以跑的距离. 则有递推 `f[i][j] = min{ ceil((f[i-1][j]+dist[i])/speed) * speed, f[i-1][j-1]+dist[i] }` 这里的第一项需要取整之后再乘以速度转为距离单位, 变为整数.
        see [灵神](https://leetcode.cn/problems/minimum-skips-to-arrive-at-meeting-on-time/solution/jiang-dp-mu-biao-gai-wei-zui-xiao-hua-fe-kg1k/)
总结: 这是第一次遇到卡浮点数运算精度的题, 分析比较简单, 但很有意思!
"""
    def minSkips(self, dist: List[int], speed: int, hoursBefore: int) -> int:
        EPS = 1e-7
        if sum(dist)/speed > hoursBefore: return -1
        n = len(dist)
        f = [[float('inf')]*(n+1) for _ in range(n)]
        f[0][1] = ceil(dist[0]/speed)
        for i in range(1, n): f[0][i+1] = dist[0]/speed
        for i in range(1, n):
            for j in range(1, n+1):
                f[i][j] = min(ceil(f[i-1][j]+dist[i]/speed - EPS), f[i-1][j-1]+dist[i]/speed)
        for idx in range(n):
            if f[-1][idx+1] <= hoursBefore: return idx
        return -1
    def minSkips(self, dist: List[int], speed: int, hoursBefore: int) -> int:
        """ see [灵神](https://leetcode.cn/problems/minimum-skips-to-arrive-at-meeting-on-time/solution/jiang-dp-mu-biao-gai-wei-zui-xiao-hua-fe-kg1k/) """
        if sum(dist)/speed > hoursBefore: return -1
        n = len(dist)
        f = [[float('inf')]*(n+1) for _ in range(n)]
        f[0][1] = ceil(dist[0]/speed) * speed
        for i in range(1, n): f[0][i+1] = dist[0]
        for i in range(1, n):
            for j in range(1, n+1):
                f[i][j] = min(ceil((f[i-1][j]+dist[i])/speed) * speed, f[i-1][j-1]+dist[i])
        for idx in range(n):
            if f[-1][idx+1] / speed <= hoursBefore: return idx
        return -1
    
    
sol = Solution()
result = [
    # sol.isSumEqual(firstWord = "acb", secondWord = "cba", targetWord = "cdb"),
    # sol.isSumEqual(firstWord = "aaa", secondWord = "a", targetWord = "aab"),
    # sol.maxValue(n = "99", x = 9),
    # sol.maxValue(n = "-13", x = 2),
    sol.assignTasks(servers = [3,3,2], tasks = [1,2,3,2,1,2]),
    sol.assignTasks(servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1]),
    sol.assignTasks([3,3,1], [10,10,99,99]),
    # sol.getOrder(tasks = [[1,2],[2,4],[3,2],[4,1]]),
    # sol.getOrder(tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]),
    # sol.minSkips(dist = [1,3,2], speed = 4, hoursBefore = 2),
    # sol.minSkips(dist = [7,3,5,5], speed = 2, hoursBefore = 10),
    # sol.minSkips(dist = [7,3,5,5], speed = 1, hoursBefore = 10),
]
for r in result:
    print(r)
