"""
输入描述:
注意：输入可能有多组数据(用于不同的调查)。每组数据都包括多行，第一行先输入随机整数的个数N，接下来的N行再输入相应个数的整数。具体格式请看下面的"示例"。

输出描述:
返回多行，处理后的结果

输入
复制
3
2
2
1
11
10
20
40
32
67
40
20
89
300
400
15
输出
复制
1
2
10
15
20
32
40
67
89
300
400
说明
样例输入解释：
样例有两组测试
第一组是3个数字，分别是：2，2，1。
第二组是11个数字，分别是：10，20，40，32，67，40，20，89，300，400，15。  
"""

import sys
while True:
    try:
        n = int(sys.stdin.readline().strip())
        nums = set()
        for _ in range(n):
            num = int(sys.stdin.readline().strip())
            nums.add(num)
        for n in sorted(nums):
            print(n)
    except Exception as e:
        break
