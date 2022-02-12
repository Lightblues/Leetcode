function testInput() {
    var input = document.getElementById("email");
    // console.log(input);
    // input.value = "test@example.com"; // 文本框的内容已更新
    var t = input.value; // '用户输入的值'
    console.log(t);
}

/* 要求
用户名必须是3-10位英文字母或数字；
口令必须是6-20位；
两次输入口令必须一致。 */
var checkRegisterForm = function () {
    var form = document.getElementById("test-register");
    var username = document.getElementById("username").value,
        password = document.getElementById("password").value,
        password2 = document.getElementById("password-2").value;
    var re1 = /[a-zA-Z0-9]{3,10}/,
        re2 = /\w{6,20}/;
    if (re1.test(username) && re2.test(password) && password === password2) {
        return true;
    }
    return false;
};

function taskForm() {
    // 测试:
    (function () {
        window.testFormHandler = checkRegisterForm;
        var form = document.getElementById("test-register");
        if (form.dispatchEvent) {
            var event = new Event("submit", {
                bubbles: true,
                cancelable: true,
            });
            form.dispatchEvent(event);
        } else {
            form.fireEvent("onsubmit");
        }
    })();
}

// testInput();
taskForm();
