package main

import (
	"fmt"
	"os"
)

func importOS(){
	if len(os.Args) != 2{
		os.Exit(1)
	}
	fmt.Println("Args[0]:", os.Args[0],)
	fmt.Println("Args[1]:", os.Args[1],)
}

func ptr(){
	var i int = 10
	println("i addr: ", &i)  // 数据对象10的地址：0xc042064058

	var ptr *int = &i
	fmt.Printf("ptr=%v\n", ptr)        // 0xc042064058
	fmt.Printf("ptr addr: %v\n", &ptr) // 指针对象ptr的地址：0xc042084018
	fmt.Printf("ptr地址: %v\n", *&ptr) // 指针对象ptr的值0xc042064058
	fmt.Printf("ptr->value: %v\n", *ptr) // 10
	fmt.Println(ptr)
}

func ptrStruct(){
	type Animal struct {
		name string
		speak string
	}
	
	bm_horse := Animal{
		name:"baima",
		speak:"neigh",  // ","不能省略，Go会报错，这个逗号有助于我们去扩展这个结构
	}
	ref_bm_horse := &Animal{"baima","neigh"}
	
	fmt.Println(bm_horse, "addr: ", &bm_horse)
	fmt.Println(ref_bm_horse, *ref_bm_horse, "addr: ", &(*ref_bm_horse))
}

type Animal struct {
    name   string
    weight int
}
// 上面的Horse数据结构中包含了一行*Animal，表示Animal的数据结构插入到Horse的结构中，这就像是一种面向对象的类继承。注意，没有给该字段显式命名，但可以隐式地访问Horse组合结构中的字段和函数。
type Horse struct {
    *Animal                  // 注意此行
    speak string
}
// 然后调用属于Animal数据结构的hello方法，它只能访问Animal中的属性，所以无法访问speak属性。
func (a *Animal) hello() {
    fmt.Println(a.name)
    fmt.Println(a.weight)
    //fmt.Println(a.speak)
}
// 重载 overload
func (h *Horse) hello(){
	fmt.Println(h.name)
	fmt.Println(h.weight)
	fmt.Println(h.speak)
}
func composition(){
	horse :=  &Horse{
		Animal: &Animal{
			"baima",
			60,
		},
		// 注释下面这行, 则 speak 为空字符串
		speak: "heigh",
	}
	horse.hello()
}

func main() {
	// ptrStruct();
	composition();
}
