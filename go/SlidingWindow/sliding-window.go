package main

import (
	"fmt"
)

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

/* 0003. Longest Substring Without Repeating Characters
Given a string, find the length of the longest substring without repeating characters.
找到字符串中最长的不重复子串的长度。

Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

思路: 双指针, 滑动搜索
当右指针遇到重复的字符 (通过 map 记录已访问的) 时, 移动左指针直到将该重复字符去除
*/
// 解法二 滑动窗口
func lengthOfLongestSubstring(s string) int {
	if len(s) == 0 {
		return 0
	}
	var freq [127]int
	result, left, right := 0, 0, -1

	for left < len(s) {
		// 如果左指针指向的字符已经出现过, 则移动左指针直到将该重复字符去除
		if right+1 < len(s) && freq[s[right+1]] == 0 {
			freq[s[right+1]]++
			right++
		} else {
			freq[s[left]]--
			left++
		}
		result = max(result, right-left+1)
	}
	return result
}

// 解法三 滑动窗口-哈希桶
func lengthOfLongestSubstring2(s string) int {
	right, left, res := 0, 0, 0
	indexes := make(map[byte]int, len(s))
	for right < len(s) {
		// 出现重复的条件: 桶中已经有该字符, 并且位置在当前遍历的字符中
		if idx, ok := indexes[s[right]]; ok && idx >= left {
			left = idx + 1
		}
		indexes[s[right]] = right
		right++
		res = max(res, right-left)
	}
	return res
}

// 解法一 位图
func lengthOfLongestSubstring3(s string) int {
	var bitSet [256]bool
	result, left, right := 0, 0, 0
	for right < len(s) {
		if bitSet[s[right]] {
			bitSet[s[left]] = false
			left++
		} else {
			bitSet[s[right]] = true
			right++
		}
		result = max(result, right-left)
	}
	return result
}

func f3() {
	fmt.Println(lengthOfLongestSubstring3("abcabcbb"))
}

/*  0030. Substring with Concatenation of All Words
You are given a string, s, and a list of words, words, that are all of the same length. Find all starting indices of substring(s) in s that is a concatenation of each word in words exactly once and without any intervening characters.

Input:
  s = "barfoothefoobarman",
  words = ["foo","bar"]
Output: [0,9]
Explanation: Substrings starting at index 0 and 9 are "barfoor" and "foobar" respectively.
The output order does not matter, returning [9,0] is fine too.

给定一组相同长度的words, 它们排列拼接得到的长度为 nL 的字符串, 找出给定的字符串 s中所有这些字符串的起始位置。
思路: 由于words中的词长度固定, 所以可以暴力遍历.
*/
func findSubstring(s string, words []string) []int {
	res := []int{}
	counter := map[string]int{} // 统计所有所需的 words
	for _, word := range words {
		counter[word]++
	}

	length, totalLen, tmpCounter := len(words[0]), len(words[0])*len(words), copyMap(counter)
	// 遍历, start 为开始匹配的位置, i 为检查到达的位置
	// 这里大佬将 两个变量放在一起遍历, 挺乱的, 不如分离成 start, i 双重遍历
	for i, start := 0, 0; start <= len(s)-totalLen; {
		if tmpCounter[s[i:i+length]] > 0 {
			tmpCounter[s[i:i+length]]--
			if checkWords(tmpCounter) && (i+length-start) == totalLen {
				res = append(res, start)
				start++
				i = start
				tmpCounter = copyMap(counter)
				continue
			}
			i = i + length
		} else {
			// 匹配失败, 重新开始
			start++
			i = start
			tmpCounter = copyMap(counter)
		}
	}
	return res
}

// 复制 map
func copyMap(m map[string]int) map[string]int {
	c := map[string]int{}
	for k, v := range m {
		c[k] = v
	}
	return c
}

// 检查是否已经完成匹配
func checkWords(s map[string]int) bool {
	flag := true
	for _, v := range s {
		if v > 0 {
			flag = false
			break
		}
	}
	return flag
}

func f30() {
	fmt.Println(findSubstring("barfoothefoobar", []string{"foo", "bar"}))
}

func main() {
	// f3()
	// f30()
	fmt.Println('a', 'a'-'A', "a", 'a'+32) // 注意 char 就是 byte
}
