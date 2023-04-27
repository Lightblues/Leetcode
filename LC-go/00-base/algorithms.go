package main

import (
	"fmt"
	"sort"
)

// ================ 二分搜索 ==========
// sort.SearchInts
// 参见 sort.Search 函数
func testSearchInts(){
	d := []int{1,3,6,6,7,9,4,10,5,6}
	idx := sort.SearchInts(d, 6)
	fmt.Println(idx) // 2, 改成搜索 4也是返回2; 即应该插入的元素位置.

}
func main(){
	testSearchInts()
}
