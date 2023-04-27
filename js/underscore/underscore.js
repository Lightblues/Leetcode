function testMap() {
    var obj = {
        name: "bob",
        school: "No.1 middle school",
        address: "xueyuan road",
    };
    // 注意, map 返回的仅仅是 value 的 Array
    var upper = _.map(obj, function (value, key) {
        return key + ": " + value.toUpperCase();
    });
    console.log(upper);

    upper = _.mapObject(obj, function (value, key) {
        return value.toUpperCase();
    });
    console.log(upper);
}

testMap();
