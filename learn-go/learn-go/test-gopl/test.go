package main

import "fmt"

func testIntOverflow() {
	f := 1e100  // a float64
	i := int(f) // 结果依赖于具体实现
	fmt.Println(f, i)
}

func testIntFormats() {
	// 05 表示八进制. %o 输出
	// %d, %x, %o, %b, 分别输出十进制, 十六进制, 八进制, 二进制
	o := 0666
	fmt.Printf("%d %[1]o %#[1]o\n", o) // "438 666 0666"
	x := int64(0xdeadbeef)
	fmt.Printf("%d %[1]x %#[1]x %#[1]X\n", x)
	// Output:
	// 3735928559 deadbeef 0xdeadbeef 0XDEADBEEF
}

func testChar() {
	ascii := 'a'
	unicode := '国'
	newline := '\n'
	fmt.Printf("%d %[1]c %[1]q\n", ascii)   // "97 a 'a'"
	fmt.Printf("%d %[1]c %[1]q\n", unicode) // "22269 国 '国'"
	fmt.Printf("%d %[1]q\n", newline)       // "10 '\n'"
}

func testString() {
	s := "hello, world"
	fmt.Println(len(s))      // "12"
	fmt.Println(s[0], s[7])  // "104 119" ('h' and 'w')
	fmt.Printf(s[:2] + "\n") // "he"
	fmt.Printf("%c\n", s[2]) // "l"
}

func main() {
	testIntOverflow()
	testIntFormats()
	testChar()
	testString()
}
