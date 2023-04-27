package main

/* 208. 实现 Trie (前缀树)
Trie（发音类似 "try"）或者说 前缀树 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补完和拼写检查。

请你实现 Trie 类：

Trie() 初始化前缀树对象。
void insert(String word) 向前缀树中插入字符串 word 。
boolean search(String word) 如果字符串 word 在前缀树中，返回 true（即，在检索之前已经插入）；否则，返回 false 。
boolean startsWith(String prefix) 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。

输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 True
trie.search("app");     // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app");     // 返回 True

https://leetcode-cn.com/problems/implement-trie-prefix-tree/solution/shi-xian-trie-qian-zhui-shu-by-leetcode-ti500/
*/

// Trie 前缀树
type Trie struct {
	children [26]*Trie
	isEnd bool
}

// Constructor obj := Constructor();
func Constructor() Trie {
	return Trie{}
}

// Insert obj.Insert(word);
func (t *Trie) Insert(word string)  {
	node := t
	for _,ch := range word {
		ch -= 'a'
		if node.children[ch] == nil {
			node.children[ch] = &Trie{}
		}
		node = node.children[ch]
	}
	node.isEnd = true
}

// Search param_2 := obj.Search(word);
func (t *Trie) Search(word string) bool {
	node := t
	for _,ch := range word {
		ch -= 'a'
		if node.children[ch] == nil {return false}
		node = node.children[ch]
	}
	if node.isEnd {return true}
	return false
}

// StartsWith param_3 := obj.StartsWith(prefix);
func (t *Trie) StartsWith(prefix string) bool {
	node := t
	for _,ch := range prefix {
		ch -= 'a'
		if node.children[ch] == nil {return false}
		node = node.children[ch]
	}
	return true
}


/**
 * Your Trie object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Insert(word);
 * param_2 := obj.Search(word);
 * param_3 := obj.StartsWith(prefix);
 */