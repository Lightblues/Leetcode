fn main() {
    let penguin_data = "\
    common name,length (cm)
    Little penguin,33
    Yellow-eyed penguin,65
    Fiordland penguin,60
    Invalid,data
    ";
 
    let records = penguin_data.lines();
 
    for (i, record) in records.enumerate() {
      if i == 0 || record.trim().len() == 0 {
        continue;
      }
 
      // 声明一个 fields 变量，类型是 Vec
      // Vec 是 vector 的缩写，是一个可伸缩的集合类型，可以认为是一个动态数组
      // <_>表示 Vec 中的元素类型由编译器自行推断，在很多场景下，都会帮我们省却不少功夫
      let fields: Vec<_> = record
        .split(',')
        .map(|field| field.trim())
        .collect();
      if cfg!(debug_assertions) {
          // 输出到标准错误输出
        eprintln!("debug: {:?} -> {:?}",
               record, fields);
      }
 
      let name = fields[0];
      // 1. 尝试把 fields[1] 的值转换为 f32 类型的浮点数，如果成功，则把 f32 值赋给 length 变量
      //
      // 2. if let 是一个匹配表达式，用来从=右边的结果中，匹配出 length 的值：
      //   1）当=右边的表达式执行成功，则会返回一个 Ok(f32) 的类型，若失败，则会返回一个 Err(e) 类型，if let 的作用就是仅匹配 Ok 也就是成功的情况，如果是错误，就直接忽略
      //   2）同时 if let 还会做一次解构匹配，通过 Ok(length) 去匹配右边的 Ok(f32)，最终把相应的 f32 值赋给 length
      //
      // 3. 当然你也可以忽略成功的情况，用 if let Err(e) = fields[1].parse::<f32>() {...}匹配出错误，然后打印出来，但是没啥卵用
      if let Ok(length) = fields[1].parse::<f32>() {
          // 输出到标准输出
          println!("{}, {}cm", name, length);
      }
    }
  }
 