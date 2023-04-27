
fn bollow_changable(){
    let mut s = String::from("hello");

    // 可变引用只能存在一个
    let r1 = &mut s;
    // let r2 = &mut s;
    println!("{}", r1);
    println!("{}", r1);

    // 引用的作用域到「最后一次使用的位置」
    let r2 = &mut s;
    r2.push_str(", world");
    println!("{}", r2);
}

fn main(){
    bollow_changable();
}