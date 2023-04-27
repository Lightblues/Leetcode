package main

import (
	"fmt"

	"rsc.io/quote"
)

// import "golang.org/x/tour/pic"

// 返回一个“返回int的函数”
func fibonacci() func() int {
	f,g := 1,0
	return func() int {
		f,g = g,f+g
		return f
	}
}
func getFibonacci(){
	fmt.Println(quote.Go())
	f := fibonacci()
	for i := 0; i < 10; i++ {
		fmt.Println(f())
	}
}

func testNil(){
	arr := [][]int{}
	arr = append(arr, nil)
	fmt.Println(arr, len(arr))
	for i:=0; i<len(arr); i++{
		fmt.Println("i =",i, ", ", arr[i])
	}
}

func main() {
	testNil()
}
