const ioredis = require("ioredis");
const BloomFilter = require('bloomfilter-redis');



let testBloom = async () => {
    const redis_client = new ioredis();
    // await redis.set("foo", "bar");
    // let res = await redis.get("foo");
    // console.log(res);
    const redisKey = "test_key1";
    redis_client.del(redisKey);
    const bf = new BloomFilter({
        redisSize: 5,
        hashesNum: 5,
        redisKey: redisKey,
        redisClient: redis_client
    });
    await bf.init();
}

let testCollapse = async () => {
    const redis_key = "testCollapse";
    const total = 10000;
    const redis_client = new ioredis();
    redis_client.del(redis_key);

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
    } catch (e) {
        console.err(e);
    }
}

testCollapse();
