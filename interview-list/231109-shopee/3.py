""" 
给定一颗二叉树, 输出层序遍历的结果. 

input: {3,9,20,#,#,15,7}
output: [[3],[9,20],[15,7]]
"""
nodes = input().strip().strip('{').strip('}').split(',')
n = len(nodes)
idx = 0; length = 1
ans = []
while idx < n:
    layer = nodes[idx:idx+length]
    layer = [int(x) for x in layer if x != '#']
    ans.append(layer)
    idx += length
    length <<= 1
ans = str(ans).replace(' ', '')
print(ans)
