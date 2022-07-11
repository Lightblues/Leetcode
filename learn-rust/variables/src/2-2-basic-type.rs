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

fn main() {
    float_panic();
    float_test_eq();
  }
  