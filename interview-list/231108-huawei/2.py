""" 
按照 prefix, exact 两种形式进行URL匹配, 若有多个匹配成功, 返回匹配长度最大的. 
限制: 长度 50; 规则数量 1e5; query 3e3
思路1: 字典树
"""
import string
# smap = {}
smap = {c:i for i,c in enumerate(string.ascii_lowercase)}
smap['/'] = len(smap)
N = len(smap)
class TrieNode:
    def __init__(self):
        self.children = [None for _ in range(N)]
        self.rule = None

def add_exact(rule:str, root:TrieNode):
    node = root
    for char in rule:
        char = smap[char]
        if not node.children[char]:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.rule = f"exact {rule}"
    
def add_prefix(rule:str, root:TrieNode):
    node = root
    for char in rule:
        char = smap[char]
        if not node.children[char]:
            node.children[char] = TrieNode()
        node = node.children[char]
    if node.rule is None:
        node.rule = f"prefix {rule}"

def match(url:str, root:TrieNode):
    node = root
    res = "(null)"
    for char in url:
        char = smap[char]
        if not node.children[char]:
            break
        node = node.children[char]
        if node.rule is not None:
            res = node.rule
    return res


root = TrieNode()
m = int(input())
for _ in range(m):
    rule_type, rule = input().split()
    if rule_type == 'exact':
        add_exact(rule, root)
    else:
        add_prefix(rule, root)
while True:
    try:
        url = input().strip()
        if not url:
            break
        print(match(url, root))
    except EOFError:
        break
