package main

// https://yar999.gitbook.io/gopl-zh/ch4/ch4-01

import (
	"fmt"
	// "popcount"
	"math/bits"
	// 不知道怎么引用
	// "github.com/tmthrgd/go-popcount"
)

func testCount() {
	// c := popcount.CountBytes([]int{2, 3})
	c := bits.OnesCount(3)
	fmt.Println(c)

	// c = popcount.CountBytes8(3)
	// fmt.Print(c)
}

func main() {
	testCount()
}
