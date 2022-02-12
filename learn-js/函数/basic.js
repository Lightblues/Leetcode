function sum(...resttt) {
    var result = 0;
    for (let i of resttt) {
        result += i;
    }
    return result;
}

function testRest() {
    // 测试:
    var i,
        args = [];
    for (i = 1; i <= 100; i++) {
        args.push(i);
    }
    if (sum() !== 0) {
        console.log("测试失败: sum() = " + sum());
    } else if (sum(1) !== 1) {
        console.log("测试失败: sum(1) = " + sum(1));
    } else if (sum(2, 3) !== 5) {
        console.log("测试失败: sum(2, 3) = " + sum(2, 3));
    } else if (sum.apply(null, args) !== 5050) {
        console.log(
            "测试失败: sum(1, 2, 3, ..., 100) = " + sum.apply(null, args)
        );
    } else {
        console.log("测试通过!");
    }
}

function testMultiAssign() {
    // 对象的解构赋值还可以嵌套
    var person = {
        name: "小明",
        age: 20,
        gender: "male",
        passport: "G-12345678",
        school: "No.4 middle school",
        address: {
            city: "Beijing",
            street: "No.1 Road",
            zipcode: "100001",
        },
    };
    var {
        name,
        address: { city, zip },
        address,
    } = person;
    // name; // '小明'
    // city; // 'Beijing'
    // zip; // undefined, 因为属性名是zipcode而不是zip
    // // 注意: address不是变量，而是为了让city和zip获得嵌套的address对象的属性:
    // address; // Uncaught ReferenceError: address is not defined
    console.log(name, city, zip, address);
}

function testApply() {
    function getAge() {
        var y = new Date().getFullYear();
        return y - this.birth;
    }

    var xiaoming = {
        name: "小明",
        birth: 1990,
        age: getAge,
    };

    console.log(
        xiaoming.age(), // 25
        // apply 以 Array 的形式传参, [] 也可以不写
        getAge.apply(xiaoming, []), // 25, this指向xiaoming, 参数为空
        // call 则分开来传参
        getAge.call(xiaoming)
    );

    console.log(
        Math.max.apply(null, [14, 3, 77]), // 77
        Math.max.call(null, 14, 3, 77) // 77
    );
}

/* 装饰器, 统计 parseInt 被调用了几次 */
function testDecorator() {
    var count = 0;
    var oldParseInt = parseInt; // 保存原函数

    window.parseInt = function (args) {
        count += 1;
        // 1. 可以直接通过 arguments 内置对象
        // return oldParseInt.apply(null, arguments); // 调用原函数
        // 2. 也可以自己写 参数传递
        return oldParseInt(args); // 调用原函数
    };

    // 测试:
    parseInt("10");
    parseInt("20");
    parseInt("30");
    console.log("count = " + count); // 3
}

function testMapReduce() {
    function string2int(s) {
        // string  2 Array
        // var arr = s.split("");
        var arr = Array.from(s);
        return arr.map((ch) => ch - "0").reduce((x, y) => x * 10 + y);
    }
    // 测试:
    if (
        string2int("0") === 0 &&
        string2int("12345") === 12345 &&
        string2int("12300") === 12300
    ) {
        if (string2int.toString().indexOf("parseInt") !== -1) {
            console.log("请勿使用parseInt()!");
        } else if (string2int.toString().indexOf("Number") !== -1) {
            console.log("请勿使用Number()!");
        } else {
            console.log("测试通过!");
        }
    } else {
        console.log("测试失败!");
    }
}

function testParseInt() {
    var arr = ["1", "2", "3"];
    var r;
    r = arr.map(parseInt); // [1, NaN, NaN]
    r = arr.map(Number); // [1, 2, 3]
    r = arr.map((n) => parseInt(n)); // [1, 2, 3]
    console.log(r);
}

function testFilter() {
    function get_primes(arr) {
        return arr.filter((n) => {
            if (n < 2) return false;
            for (let i = 2; i < n; i++) {
                if (n % i === 0) return false;
            }
            return true;
        });
    }

    // 测试:
    var x,
        r,
        arr = [];
    for (x = 1; x < 100; x++) {
        arr.push(x);
    }
    r = get_primes(arr);
    if (
        r.toString() ===
        [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
            67, 71, 73, 79, 83, 89, 97,
        ].toString()
    ) {
        console.log("测试通过!");
    } else {
        console.log("测试失败: " + r.toString());
    }
}

/* 利用闭包实现私有变量
例子: 计数器 */
function testClosure() {
    function create_counter(initial) {
        var x = initial || 0;
        return {
            inc: function () {
                x += 1;
                return x;
            },
        };
    }
    var c1 = create_counter();
    c1.inc(); // 1
    c1.inc(); // 2
    c1.inc(); // 3

    var c2 = create_counter(10);
    c2.inc(); // 11
    c2.inc(); // 12
    c2.inc(); // 13
    console.log(
        c1.inc(), // 4
        c2.inc() // 14
    );
}

/* 箭头函数中 this 指向词法作用域 */
function testArrawFunction() {
    var age, obj;

    // 由于JavaScript函数对`this`绑定的错误处理，下面的例子无法得到预期结果
    obj = {
        birth: 1990,
        getAge: function () {
            var b = this.birth; // 1990
            var fn = function () {
                return new Date().getFullYear() - this.birth; // this指向window或undefined
            };
            return fn();
        },
    };
    age = obj.getAge();
    console.log("由于this指向window而出错: ", age);

    obj = {
        birth: 1990,
        getAge: function () {
            var b = this.birth; // 1990
            var that = this; // 指向obj
            var fn = function () {
                return new Date().getFullYear() - that.birth;
            };
            return fn();
        },
    };
    age = obj.getAge();
    console.log("保存this为that: ", age);

    // 箭头函数完全修复了`this`的指向，`this`总是指向词法作用域，也就是外层调用者`obj`
    obj = {
        birth: 1990,
        getAge: function () {
            var b = this.birth; // 1990
            var fn = () => new Date().getFullYear() - this.birth; // this指向obj对象
            return fn();
        },
    };
    age = obj.getAge();
    console.log("采用箭头函数: ", age);

    // 由于`this`在箭头函数中已经按照词法作用域绑定了，所以，用`call()`或者`apply()`调用箭头函数时，无法对`this`进行绑定，即传入的第一个参数被忽略
    obj = {
        birth: 1990,
        getAge: function (year) {
            var b = this.birth; // 1990
            var fn = () => new Date().getFullYear() - this.birth; // this.birth仍是1990
            return fn.call({ birth: 2000 }, year);
        },
    };
    age = obj.getAge();
    console.log("apply的第一个参数会被忽略", age);
}

/* 利用 generator 实现 Fibonacci */
function testGeneratorFib() {
    // 用函数实现
    function fibReturn(max) {
        var t,
            a = 0,
            b = 1,
            arr = [0, 1];
        while (arr.length < max) {
            [a, b] = [b, a + b];
            arr.push(b);
        }
        return arr;
    }
    // generator
    function* fib(max) {
        var t,
            a = 0,
            b = 1,
            n = 0;
        while (n < max) {
            yield a;
            [a, b] = [b, a + b];
            n++;
        }
        return;
    }

    /* 注意, next() 方法返回的是一个对象 */
    var f = fib(5);
    f.next(); // {value: 0, done: false}
    f.next(); // {value: 1, done: false}
    f.next(); // {value: 1, done: false}
    f.next(); // {value: 2, done: false}
    f.next(); // {value: 3, done: false}
    f.next(); // {value: undefined, done: true}

    for (var x of fib(10)) {
        console.log(x); // 依次输出0, 1, 1, 2, 3, ...
    }
}

/* 生成一个自增的ID */
function taskGenerator() {
    // 如果不用闭包, 需要一个全局变量
    // var current_id = 0;
    // function next_id() {
    //     current_id++;
    //     return current_id;
    // }
    // 利用 generator
    function* next_id() {
        var current_id = 0;
        while (true) {
            current_id++;
            yield current_id;
        }
    }
    // 测试:
    var x,
        pass = true,
        g = next_id();
    for (x = 1; x < 100; x++) {
        if (g.next().value !== x) {
            pass = false;
            console.log("测试失败!");
            break;
        }
    }
    if (pass) {
        console.log("测试通过!");
    }
}

// testRest();
// testMultiAssign();
// testApply();
// testDecorator();
// testMapReduce();
// testParseInt();
// testFilter();
// testClosure();
// testArrawFunction();
testGeneratorFib();
// taskGenerator();
