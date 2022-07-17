#![allow(unused)]
fn char_size() {
    let x = '中';
    println!("字符'中'占用了{}字节的内存大小",std::mem::size_of_val(&x));
}

fn dead_end() -> ! {
    panic!("你已经到了穷途末路，崩溃吧！");
    // println!("你已经到了穷途末路，崩溃吧！");
}

fn forever() -> ! {
    loop {
      //...
    };
}

fn test_str() {
    let s = String::from("hello world");

    // 创建索引
    let hello = &s[0..5];
    let world = &s[6..11];
    println!("{} {}!", hello, world);
}

// fn main() {
//     char_size();
//     // dead_end();
//     forever();
// }

fn main() {
    // get_option(1);
    // println!("Success!");

    test_str();
}

fn get_option(tp: u8) -> Option<i32> {
    match tp {
        1 => {
            // TODO
        }
        _ => {
            // TODO
        }
    };
    
    // 这里与其返回一个 None，不如使用发散函数替代
    never_return_fn()
}

// 使用三种方法实现以下发散函数
// use std::thread;
// use std::time;
// fn never_return_fn() -> ! {
//     loop {
//         std::thread::sleep(std::time::Duration::from_secs(1))
//     }
// }
fn never_return_fn() -> ! {
    unimplemented!()
}