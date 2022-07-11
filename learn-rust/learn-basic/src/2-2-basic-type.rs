fn float_panic() {
    // 由于浮点数的精度问题, 尽量避免相等运算!
    println!("{} {}", 0.1 + 0.2, 0.3);
    // 断言0.1 + 0.2与0.3相等. 无法通过.
    // assert!(0.1 + 0.2 == 0.3);
}
fn float_test_eq() {
    // 因此, 可以用abs来判断浮点数是否(近似)相等.
    println!("Test equality: {}", (0.1_f64 + 0.2 - 0.3).abs() < 0.00001)
}
fn float_f32_f64() {
    // 再给个例子: 由于f64的精度更高, 反而导致
    let abc: (f32, f32, f32) = (0.1, 0.2, 0.3);
    let xyz: (f64, f64, f64) = (0.1, 0.2, 0.3);

    println!("abc (f32)");
    println!("   0.1 + 0.2: {:x}", (abc.0 + abc.1).to_bits());
    println!("         0.3: {:x}", (abc.2).to_bits());
    println!();

    println!("xyz (f64)");
    println!("   0.1 + 0.2: {:x}", (xyz.0 + xyz.1).to_bits());
    println!("         0.3: {:x}", (xyz.2).to_bits());
    println!();

    assert!(abc.0 + abc.1 == abc.2);
    // assert!(xyz.0 + xyz.1 == xyz.2); // 这个断言错了
}

fn float_na(){
    // let x = 1.0_f64 / 0.0;
    // 注意需要指定 f64 之后才能有方法 is_nan 等, 默认的 float 类型会报错
    let x = (-4.6_f64).sqrt();
    println!("NaN: {}", x);
    assert!(x.is_nan() == true);
}


fn main() {
    float_panic();
    float_test_eq();
    float_f32_f64();
    float_na();
  }
  