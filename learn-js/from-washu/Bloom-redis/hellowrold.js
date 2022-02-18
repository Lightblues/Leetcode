// 测试 collapse 部分参考 <https://crossoverjie.top/2018/11/26/guava/guava-bloom-filter/>

const BloomFilter = require('bloomfilter-redis');
const redis = require("redis");
const ioredis = require("ioredis");


let helloworld = async function (){
    const bf = new BloomFilter({// all params have a default value, and I choose some to present below
        redisSize: 256, // this will create a string value which is 256 MegaBytes in length
        hashesNum: 16, // how many hash functions do we use
        redisKey: 'test-bf', // this will create a string whose keyname is `Node_Bloomfilter_Redis`
        redisClient: redis.createClient(), // you can choose to create the client by yourself
    });
    try {
        for (let s of ['我爱你', 'I love you', 'je t\'aime', 'ich liebe dich', 'Ti Amo', 'te amo vos amo']){
            await bf.add(s);
        }
        for (let s of ['사랑해요', 'I love you', '爱してる']) {
            let res = await bf.contains(s);
            console.log(res);
        }
    } catch (e) {console.error(e)}
};

let testPipleline = async () => {
    const bf = new BloomFilter({// all params have a default value, and I choose some to present below
        redisSize: 2, // this will create a string value which is 256 MegaBytes in length
        hashesNum: 6, // how many hash functions do we use
        redisKey: 'test-bf', // this will create a string whose keyname is `Node_Bloomfilter_Redis`
        redisClient: new ioredis(), // you can choose to create the client by yourself
    });
    let arr = ['我爱你', 'I love you', 'je t\'aime', 'ich liebe dich', 'Ti Amo', 'te amo vos amo'],
        testArr = ['사랑해요', 'I love you', '爱してる'];
    let promiseContainsArr = [];

    for (let str of arr) {
        await bf.add(str);
    }
    testArr.forEach(str => {
        promiseContainsArr.push(bf.contains(str)); // assembly contains tasks
    });

    Promise.all(promiseContainsArr).then(results => {
            console.log(`promise.all() returns: ${results}`); // [ false, true, false ]. Yeah, that's the right answer
    });
}


/*
问题：redisSize 支持浮点数吗？
如何阐述字段？
[已完成] 将redis包换成 ioredis ？

查看存储的 testCollapse 字符串信息，注意 STRLEN 返回的是字节数
127.0.0.1:6379> STRLEN testCollapse
1048575
127.0.0.1:6379> BITCOUNT testCollapse
485390


total = 1000000
    Collpase rate: 0.003789
    Time used: 166.022s
*/

let testCollapse = async () => {
    const redis_key = "testCollapse";
    // 要先删除 这个名字
    const total = 1000000;
    const redis_client = redis.createClient();


    const bf = new BloomFilter({
        redisSize: total/1000000,
        hashesNum: 5,
        redisKey: redis_key,
        redisClient: redis_client
    });

    try {
        let start_time = Date.now();
        let collapse_counter = 0;
        for (let i = 0; i<total; i++){
            if (!(i%1000)){
                console.log(i);
            }
            i = i.toString();
            if (await bf.contains(i)) {
                collapse_counter++;
            } else {
                await bf.add(i);
            }
        }
        console.log(`Collpase rate: ${collapse_counter/total}`);
        console.log(`Time used: ${(Date.now() - start_time)/1000}s`);
    } catch (e) {console.err(e)}
};




// testCollapse();
testPipleline();
