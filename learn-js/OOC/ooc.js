/* 对象的原型 */
function testObject() {
    var xiaoming;
    var Student = {
        name: "Robot",
        height: 1.2,
        run: function () {
            console.log(this.name + " is running...");
        },
    };

    /* 测试 __proto__ 属性 */
    xiaoming = {
        name: "小明",
    };
    // 代码仅用于演示目的。在编写JavaScript代码时，不要直接用obj.__proto__去改变一个对象的原型
    xiaoming.__proto__ = Student;

    xiaoming.run();
    console.log(xiaoming.name, xiaoming.height);

    /* 这是创建原型继承的一种方法 */
    function createStudent(name) {
        // 基于Student原型创建一个新对象:
        var s = Object.create(Student);
        // 初始化新对象:
        s.name = name;
        return s;
    }

    xiaoming = createStudent("小明");
    xiaoming.run(); // 小明 is running...
    xiaoming.__proto__ === Student; // true
}

/* 请利用构造函数定义`Cat`，并让所有的Cat对象有一个`name`属性，并共享一个方法`say()`，返回字符串`'Hello, xxx!'`： */
function taskPrototype() {
    function Cat(name) {
        this.name = name;
    }
    Cat.prototype.say = function () {
        return `Hello, ${this.name}!`;
    };

    // 测试:
    var kitty = new Cat("Kitty");
    var doraemon = new Cat("哆啦A梦");
    if (
        kitty &&
        kitty.name === "Kitty" &&
        kitty.say &&
        typeof kitty.say === "function" &&
        kitty.say() === "Hello, Kitty!" &&
        kitty.say === doraemon.say
    ) {
        console.log("测试通过!");
    } else {
        console.log("测试失败!");
    }
}

/* 继承 */
function testInheritOrigin() {
    function Student(props) {
        this.name = props.name || "Unnamed";
    }
    Student.prototype.hello = function () {
        alert("Hello, " + this.name + "!");
    };

    // PrimaryStudent构造函数:
    function PrimaryStudent(props) {
        Student.call(this, props);
        this.grade = props.grade || 1;
    }

    /* 以下这块代码可以用下面实现的 inherits 函数替代
    这里 F 函数的作用: 
    1. 指定构造函数 F 的 prototype 属性(注意prototype为函数所特有的属性) 为 Student.prototype; 从而使得 new 出来的 F对象有属性 `(new F()).__proto__ === Student.prototype`
    2. 构造一个 F对象 (记为 f), 这个对象就是我们要构造的 PrimaryStudent.prototype 原型, 通过 1 我们指定好了这一对象 `__proto__` 属性
    3. 链接 对象f 和 构造函数PrimaryStudent, 使得它们互为 constructor, prototype
     */
    // 空函数F:
    function F() {}
    // 把F的原型指向Student.prototype:
    F.prototype = Student.prototype;
    // 把PrimaryStudent的原型指向一个新的F对象，F对象的原型正好指向Student.prototype:
    PrimaryStudent.prototype = new F();
    // 把PrimaryStudent原型的构造函数修复为PrimaryStudent:
    PrimaryStudent.prototype.constructor = PrimaryStudent;

    // 继续在PrimaryStudent原型（就是new F()对象）上定义方法：
    PrimaryStudent.prototype.getGrade = function () {
        return this.grade;
    };

    // 创建xiaoming:
    var xiaoming = new PrimaryStudent({
        name: "小明",
        grade: 2,
    });
    xiaoming.name; // '小明'
    xiaoming.grade; // 2

    // 验证原型:
    xiaoming.__proto__ === PrimaryStudent.prototype; // true
    xiaoming.__proto__.__proto__ === Student.prototype; // true

    // 验证继承关系:
    xiaoming instanceof PrimaryStudent; // true
    xiaoming instanceof Student; // true
}

/* 可以简化逻辑, 写一个 inherits 函数 */
function inherits(Child, Parent) {
    var F = function () {};
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
}

function testInherits() {
    function Student(props) {
        this.name = props.name || "Unnamed";
    }

    Student.prototype.hello = function () {
        alert("Hello, " + this.name + "!");
    };

    function PrimaryStudent(props) {
        Student.call(this, props);
        this.grade = props.grade || 1;
    }

    // 实现原型继承链:
    inherits(PrimaryStudent, Student);

    // 绑定其他方法到PrimaryStudent原型:
    PrimaryStudent.prototype.getGrade = function () {
        return this.grade;
    };
}

function testClass() {
    class Animal {
        constructor(name) {
            this.name = name;
        }
    }
    class Cat extends Animal {
        constructor(name) {
            super(name);
        }
        say() {
            return `Hello, ${this.name}!`;
        }
    }

    // 测试:
    var kitty = new Cat("Kitty");
    var doraemon = new Cat("哆啦A梦");
    if (
        new Cat("x") instanceof Animal &&
        kitty &&
        kitty.name === "Kitty" &&
        kitty.say &&
        typeof kitty.say === "function" &&
        kitty.say() === "Hello, Kitty!" &&
        kitty.say === doraemon.say
    ) {
        console.log("测试通过!");
    } else {
        console.log("测试失败!");
    }
}

// testObject();
// taskPrototype();
// testInheritOrigin();
// testInherits();
testClass();
