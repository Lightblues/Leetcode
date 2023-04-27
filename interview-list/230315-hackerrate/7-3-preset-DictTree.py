""" No Prefix Set
给定一组words, 判断是否有重复前缀的单词. 限制: 字符 a-j; 词长度 60; n 1e5
思路1: #字典树
"""

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'noPrefix' function below.
#
# The function accepts STRING_ARRAY words as parameter.
#
class Node:
    def __init__(self, x=None):
        self.val = x
        self.childs = [None] * 10
        self.isLeaf = False

def noPrefix(words):
    # Write your code here
    root = Node()
    for word in words:
        p = root
        flag = False        # 当前word是否为其他单词的前缀
        for c in word:
            idx = ord(c) - ord('a')
            if p.childs[idx] is None:
                p.childs[idx] = Node()
                flag = True
            p = p.childs[idx]
            if p.isLeaf:
                # 有单词是当前word的前缀
                print("BAD SET")
                print(word)
                return 
        if not flag:
            print("BAD SET")
            print(word)
            return 
        p.isLeaf = True
    print("GOOD SET")
                

if __name__ == '__main__':
    n = int(input().strip())

    words = []

    for _ in range(n):
        words_item = input()
        words.append(words_item)

    noPrefix(words)
