// 所有 identifier 都要指明类型; 返回值默认为 (), 否则需要明确
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main(){
    println!("{}", add(1, 2));
}