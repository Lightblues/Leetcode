package main

import (
	"fmt"
	"math"
	"strconv"
)

// ===================== struct & 常用函数 ================================

// ListNode 链表元素
type ListNode struct {
	Val int
	Next *ListNode
}

// List2Ints convert List to []int
func List2Ints(head *ListNode) []int {
	// 链条深度限制，链条深度超出此限制，会 panic
	limit := 100

	times := 0

	res := []int{}
	for head != nil {
		times++
		if times > limit {
			msg := fmt.Sprintf("链条深度超过%d，可能出现环状链条。请检查错误，或者放宽 l2s 函数中 limit 的限制。", limit)
			panic(msg)
		}

		res = append(res, head.Val)
		head = head.Next
	}

	return res
}

// Ints2List convert []int to List
func Ints2List(nums []int) *ListNode {
	if len(nums) == 0 {
		return nil
	}

	l := &ListNode{}
	t := l
	for _, v := range nums {
		t.Next = &ListNode{Val: v}
		t = t.Next
	}
	return l.Next
}

func abs(x int) int{
	if x>=0{
		return x
	} 
	return -x
}

// ===================== math ================================

/* 0002.Add-Two-Numbers/
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.
2 个逆序的链表，要求从低位开始相加，得出结果也逆序输出，返回值是逆序结果链表的头结点。
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807. */
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	head := &ListNode{Val: 0}
	n1, n2, carry, current := 0,0,0, head
	for l1!=nil || l2!=nil || carry !=0 {
		if l1==nil {
			n1 = 0
		} else {
			n1 = l1.Val
			l1 = l1.Next
		}
		if l2 == nil {
			n2 = 0
		} else {
			n2 = l2.Val
			l2 = l2.Next
		}
		current.Next = &ListNode{Val: (n1+n2+carry) % 10}
		current = current.Next
		carry = (n1+n2+carry)/10
	}
	return head.Next
}
func f2(){
	l1 := Ints2List([]int{1, 2, 3, 4, 5})
	l2 := Ints2List([]int{1, 2, 3, 4, 5})
	ret := addTwoNumbers(l1, l2)
	fmt.Println(List2Ints(ret))
}

/* 0007.Reverse-Integer/
Given a 32-bit signed integer, reverse digits of an integer.
Input: -123
Output: -321
Note: Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−2^31, 2^31 − 1]. For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows. 
测试用例
-1463847412 
附录一个 Python 下讨巧的一行方案
return (int(str(x)[::-1]) if int(str(x)[::-1]) <= 2 ** 31 - 1 else 0) if str(x)[0] != '-' else (int('-' + str(x)[1:][::-1]) if int('-' + str(x)[1:][::-1]) >= -2 ** 31 else 0)

这题主要的限制是在要防止 32位 sign int 溢出. 这里方案是每次 *10 之前进行检查, 官方答案对于判断条件进行了简化 https://leetcode-cn.com/problems/reverse-integer/solution/zheng-shu-fan-zhuan-by-leetcode-solution-bccn/, 但如果只是为了快速解答的话似乎没有必要. 
*/
func reverse(x int) int {
	// 1<<31 == 2147483648
	maxDiv10, minDiv10 := 214748364, -214748364
	rev := 0
	for x != 0 {
		// 防止溢出
		if (rev>maxDiv10 || rev==maxDiv10 && x%10>7) || (rev<minDiv10 || rev==minDiv10 && x%10< -8) {
			return 0
		}
		rev = rev*10 + x%10
		x = x/10
	}
	return rev
}
func f7(){
	fmt.Println(reverse(-1463847412))
}

/* 0009.Palindrome-Number/
Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
Input: -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

注意负数也不算*/
// 这里除了可以和 7题 一样进行反转, 还可以类似字符串判断是否回文
func palindromeNumber(x int) bool {
	if x<0 {
		return false
	} else if x ==0 {
		return true
	} else if x%10==0{
		return false
	}
	// arr := make([]int, 0, 32)		// 这里必须指定 size=0; 或者用 var 声明
	var arr []int
	for x!=0 {
		arr = append(arr, x%10)
		x = x/10
	}
	for i,j:=0,len(arr)-1; i<j; {
		if arr[i] != arr[j]{
			return false
		}
		i++; j--
	}
	return true
}
// 这里是反转数字; 但可能出现溢出的情况(虽然此时必然不是回文数); https://leetcode-cn.com/problems/palindrome-number/solution/hui-wen-shu-by-leetcode-solution/ 官方答案通过「仅反转数字长度的一半」避免了该问题. 
func palindromeNumber1(x int) bool {
	// if x<0 {
	// 	return false
	// }
	// rev := 0; xSave:=x
	// for x!=0 {
	// 	rev = rev*10 + x%10
	// 	x = x/10
	// }
	// return rev==xSave

	if x<0 || (x%10==0 && x!=0){
		return false
	}
	rev:=0
	for x>rev{
		rev = rev*10 + x%10
		x = x/10
	}
	// 若 x 为回文数且长度为偶数, 则 x==rev; 若为奇数, 则 x==rev/10
	// fmt.Println(x, rev)
	return x==rev || x==rev/10
}
// 解法二 数字转字符串
func palindromeNumber2(x int) bool {
	if x < 0{
		return false
	}
	s := strconv.Itoa(x)
	for i,j:=0,len(s)-1; i<j;i,j=i+1,j-1{
		if s[i]!=s[j]{
			return false
		}
	}
	return true
}
func f9(){
	fmt.Println(palindromeNumber1(101), palindromeNumber1(1))
	// fmt.Println(palindromeNumber2(101), palindromeNumber2(1))
}

/* 0012.Integer-to-Roman/
Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000 
I can be placed before V (5) and X (10) to make 4 and 9.
X can be placed before L (50) and C (100) to make 40 and 90.
C can be placed before D (500) and M (1000) to make 400 and 900.

Input: num = 1994
Output: "MCMXCIV"
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
总之就是和十进制不一样, 有不同的基数. */
func intToRoman(num int) string {
	values := []int{1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1}
	symbols := []string{"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"}
	res, i := "", 0
	for num != 0 {
		for values[i]>num {
			i++
		}
		num -= values[i]
		res += symbols[i]
	}
	return res
}
func f12(){
	fmt.Println(intToRoman(1994))
}

/* 0013.Roman-to-Integer/ 
Input: "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

这里的思路和上题类似, 注意罗马数字从大到小的基数前序是不会重复的, 所以可能直接匹配累加*/
func romanToInt(s string) int {
	values := []int{1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1}
	symbols := []string{"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"}
	res, i := 0, 0
	for len(s) >0 {
		// 这里的判断逻辑: 主体是 symbols[i] != s[:len(symbols[i])], 要注意匹配到最后一位要防止指针溢出
		for len(s)<len(symbols[i]) || symbols[i] != s[:len(symbols[i])] {
			i++
		}
		res += values[i]
		s = s[len(symbols[i]):]
	}
	return res
}
// 解法二 累加每一位的数字, 通过记录上一位数字判断其符号
func romanToInt2(s string) int {
	var roman = map[string]int{
		"I": 1,
		"V": 5,
		"X": 10,
		"L": 50,
		"C": 100,
		"D": 500,
		"M": 1000,
	}
	if s == "" {
		return 0
	}
	num, lastint, total := 0, 0, 0
	for i := 0; i < len(s); i++ {
		char := s[len(s)-(i+1) : len(s)-i]
		num = roman[char]
		if num < lastint {
			total = total - num
		} else {
			total = total + num
		}
		lastint = num
	}
	return total
}
func f13(){
	fmt.Println(romanToInt("MCMXCIV"), romanToInt("DCXXI"))
}

/* 0060.Permutation-Sequence/
给出集合 [1,2,3,…,n]，其所有元素共有 n! 种排列。
按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下：“123”，“132”，“213”，“231”，“312”，“321”，给定 n 和 k，返回第 k 个排列。

Input: n = 4, k = 9
Output: "2314"

此题难度不大, 但是有一些边界情况入需要注意. 
1. 构造了 factorial 来实现 Python 中的 math.perm; 2. 用 valid 数组标记还没有用过的数字. */
func getPermutation(n int, k int) string {
	factorial := make([]int, n)
	factorial[0] = 1
	for i:=1; i<n; i++{
		factorial[i] = factorial[i-1]*i
	}

	res := ""
	// k--
	valid := make([]int, n)
	for i:=0; i<n; i++{
		valid[i] = 1
	}
	for i:=1; i<=n; i++{
		order := (k-1) / factorial[n-i] + 1
		k = k - (order-1)*factorial[n-i]
		for j:=0; j<n; j++{
			order -= valid[j]
			if order == 0{
				valid[j] = 0
				res += strconv.Itoa(j+1)
				break	// Note!
			}
		}
	}
	return res
}
func f60(){
	// fmt.Println(strings.Join([]string{"1", "2"}, ""), string([]byte{'1', '2'}))
	fmt.Println(getPermutation(4, 9))
}

/* 0029.Divide-Two-Integers/
给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。返回被除数 dividend 除以除数 divisor 得到的商。
说明:
被除数和除数均为 32 位有符号整数。
除数不为 0。
假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−2^31,  2^31 − 1]。本题中，如果除法结果溢出，则返回 2^31 − 1。 */
// 也可以用「二分查找」的思想, 但由于无法用乘法, 并不优雅
// 解法二 非递归版的二分搜索
func divide1(dividend int, divisor int) int {
	if dividend==math.MinInt32 && divisor== -1{
		return math.MaxInt32
	}
	signed := -1
	if (dividend>0 && divisor>0) || (dividend<0 && divisor<0){
		signed=1
	}
	dvd, dvs := abs(dividend), abs(divisor)

	dvsSave := dvs
	res := 0
	for dvd >= dvsSave {
		tmp, dvs := 1, dvsSave
		for dvs<<1 <= dvd {
			dvs <<= 1
			tmp <<= 1
		}
		res += tmp
		dvd -= dvs
		// fmt.Println(dvd, dvs)
	}
	return signed*res
}
// 解法三 倍增法
func divide2(dividend, divisor int) int {
	if dividend==math.MinInt32 && divisor== -1{
		return math.MaxInt32
	}
	signed := -1
	if (dividend>0 && divisor>0) || (dividend<0 && divisor<0){
		signed=1
	}
	dvd, dvs := abs(dividend), abs(divisor)

	res, factor, cnt := 0, dvs, 1  // factor, cnt 分别记录当前的除数和因子
	for cnt>= 1{		// 注意循环种植条件: 因子 cnt==0, 也即 dividend<divisor
		if dvd>=factor {
			res += cnt
			dvd -= factor
			factor <<= 1
			cnt <<= 1
			if dvd == 0{
				break
			}
		} else {
			factor >>= 1
			cnt >>= 1
		}
	}
	return signed*res
	
}
func f29(){
	fmt.Println(divide2(-7, -2), divide2(2147483647, 1))
}


// ===================== main ================================
func main (){
	f29()
}