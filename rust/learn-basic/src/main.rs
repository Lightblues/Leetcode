fn test_str() {
    let s = String::from("hello world");

    // 创建索引
    let hello = &s[0..=5];
    let world = &s[6..11];
    println!("{} {}!", hello, world);
}
fn test_utf8() {
    let s = "中国人";
    // 中文在 UTF-8 中占用三个字节,下面的代码就会崩溃
    // let a = &s[0..2];
    let a = &s[0..2]; // 中
    println!("{}", a);
}

fn string_catenate() {
    let string_append = String::from("hello ");
    let string_rust = String::from("rust");
    // add 操作的第二个参数必须是一个引用类型.
    // &string_rust会自动解引用为 &str
    let result = string_append + &string_rust;
    //
    let mut result = result + "!";
    result += "!!!";

    println!("连接字符串 + -> {}", result);
}

fn string_add() {
    let s1 = String::from("hello,");
    let s2 = String::from("world!");
    // 在下句中，s1的所有权被转移走了，因此后面不能再使用s1
    let s3 = s1 + &s2;
    assert_eq!(s3, "hello,world!");
    // 下面的语句如果去掉注释，就会报错
    // println!("{}",s1);
}

fn string_str_trans() {
    let mut s = String::from("hello,world!");
    // 取引用转为 &str 类型
    say_hello(&s);
    say_hello(&mut s[..5]); // 切片也是一种引用
    say_hello(s.as_str());
}
fn say_hello(s: &str) {
    println!("{}", s);
}

fn test_slice_mut() {
    let mut arr = [1, 2, 3, 4];
    let sarr = &mut arr[1..3];
    println!("{:?}", sarr);
    sarr[0] = 9;
    println!("{:?}", sarr);
    println!("{:?}", arr);
}

fn string_slice_mut() {
    let mut s = String::from("hello world");
    let hello = &mut s[0..5];
    // let world = &s[6..11];
    hello.replace("h", "H");
    print!("{}", hello);
    print!("{}", s);

    // println!("{} {}!", hello, world);
}

fn main() {
    // num_complex();
    // char_size();
    // test_str();
    // test_utf8();
    string_catenate();
    string_add();
    string_str_trans();
    string_slice_mut();
}
