package main

import "fmt"

/* 0035.Search-Insert-Position/
Given a sorted array and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
You may assume no duplicates in the array.

Input: [1,3,5,6], 7
Output: 4
这一题是经典的二分搜索的变种题，在有序数组中找到最后一个比 target 小的元素。*/
func searchInsert(nums []int, target int) int {
	low, high := 0, len(nums)-1
	for low <= high {
		mid := low + (high-low)>>1
		if nums[mid] >= target {		// [1], 1 应该返回 0
			high = mid-1
		} else {
			if mid==len(nums)-1 || nums[mid+1]>=target{
				return mid+1
			}
			low = mid+1
		}
	}
	return 0  // 注意这里的返回条件
}
func f35(){
	fmt.Println(searchInsert([]int{1,3,5,6}, 0))
}



/* 0069.Sqrtx/
实现 int sqrt(int x) 函数。计算并返回 x 的平方根，其中 x 是非负整数。由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。
Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since 
             the decimal part is truncated, 2 is returned. */
// 解法一 二分, 找到最后一个满足 n^2 <= x 的整数n
func mySqrt(x int) int {
	l, h := 0, x
	for l<=h{
		mid := l+(h-l)>>2
		if mid*mid > x{
			h = mid-1
		} else {
			if (mid+1)*(mid+1) > x{
				return mid
			}
			l = mid+1
		}
	}
	return -1
}
// 解法二 牛顿迭代法 https://en.wikipedia.org/wiki/Integer_square_root
// 即求 f(r)=r^2-x 的零点
func mySqrt1(x int) int {
	r := x
	for r*r > x {
		r = (r + x/r) / 2
	}
	return r
}
func f69(){
	fmt.Println(mySqrt(8), mySqrt(0))
}

/* 0074.Search-a-2D-Matrix/
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.

Input:
matrix = [
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
target = 3
Output: true

其实就是一维的有序列表搜索, 不过需要进行坐标变换*/

func searchMatrix(matrix [][]int, target int) bool {
	return true
}

func main(){
	f69()
}