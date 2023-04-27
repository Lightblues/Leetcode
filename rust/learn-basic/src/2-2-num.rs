// use num::complex::Complex;
// fn num_complex() {
//     let a = Complex { re: 2.1, im: -1.2 };
//     let b = Complex::new(11.1, 22.2);
//     let result = a + b;
 
//     println!("{} + {}i", result.re, result.im)
// }

fn num_basic() {
    // 编译器会进行自动推导，给予twenty i32的类型
    let twenty = 20;
    // 类型标注
    let twenty_one: i32 = 21;
    // 通过类型后缀的方式进行类型标注：22是i32类型
    let twenty_two = 22i32;
  
    // 只有同样类型，才能运算
    let addition = twenty + twenty_one + twenty_two;
    println!("{} + {} + {} = {}", twenty, twenty_one, twenty_two, addition);
  
    // 对于较长的数字，可以用_进行分割，提升可读性
    let one_million: i64 = 1_000_000;
    println!("{}", one_million.pow(2));
  
    // 定义一个f32数组，其中42.0会自动被推导为f32类型
    let forty_twos = [
      42.0,
      42f32,
      42.0_f32,
    ];
  
    // 打印数组中第一个值，并控制小数位为2位
    println!("{:.2}", forty_twos[0]);
  }
  
fn num_float(){
    let a = 3.14;
    // 在没有指定a的类型的情况下, 两个都能过! 但一旦指定了就必须一致才能运算.
    let b: f64 = 3.14;
    let b: f32 = 3.14;

    println!("{}", a==b);
}

fn range_for_loop(){
    for i in 'a'..'d' {
        println!("{}", i)
    }
}

fn expression_fn() {
    let r = add_with_extra(1, 1);
    println!("{}", r);
}
fn add_with_extra(x: i32, y: i32) -> i32 {
    let x = x + 1; // 语句
    let y = y + 5; // 语句
    x + y // 表达式
}

fn expression_if() {
    assert_eq!(ret_unit_type(), ());
}
fn ret_unit_type() {
    let x = 1;
    // if 语句块也是一个表达式，因此可以用于赋值，也可以直接返回
    if (x > 1) {
    }
}


fn main() {
    // num_complex();
    expression_fn();
    expression_if();
    num_basic();
    num_float();
    range_for_loop();
}
