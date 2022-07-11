fn greet_world() {
    let southern_germany = "Grüß Gott!";
    let chinese = "世界，你好";
    let english = "World, hello";
    let regions = [southern_germany, chinese, english];
    // 转为迭代器. 如果不写的话 for会进行隐式转换
    for region in regions.iter() {
        // ! 是宏操作符
        println!("{}", &region);
    }
}

fn main() {
    greet_world();
}
