fn variable_jiexi() {
    let (a, mut b): (bool,bool) = (true, false);
    // a = true,不可变; b = false，可变
    // println!("a = {:?}, b = {:?}", a, b);
    println!("a = {}, b = {}", a, b);

    b = true;
    assert_eq!(a, b);
}

struct Struct {
    e: i32
}

fn variable_jiexishijiegou(){
    // 也可以使用元组、切片和结构体模式
    let (a, b, c, d, e);

    (a, b) = (1, 2);
    // _ 代表匹配一个值，但是我们不关心具体的值是什么，因此没有是一个变量名而是使用了 _
    [c, .., d, _] = [1, 2, 3, 4, 5];
    Struct { e, .. } = Struct { e: 5 };

    assert_eq!([1, 2, 1, 4, 5], [a, b, c, d, e]);
}

fn main() {
    // variable_jiexi();
    variable_jiexishijiegou();
}
