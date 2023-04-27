const ioredis = require("ioredis");
const BloomFilter = require('bloomfilter-redis');

let helloWorld = () => {
    const redisClient = new ioredis();
    let pipeline = redisClient.pipeline();

    pipeline.set("foo", "bar");
    pipeline.get("foo");
    pipeline.del("foo");
    pipeline.exec((err, results) => {
        console.log(results)
        // [ [ null, 'OK' ], [ null, 'bar' ], [ null, 1 ] ]
        // `err` is always null, and `results` is an array of responses
        // corresponding to the sequence of queued commands.
        // Each response follows the format `[err, result]`.
    });
}



let testCollapse = async () => {
    const redis_key = "testCollapse";
    const total = 10000;
    const redisClient = new ioredis();
    redisClient.del(redis_key);

    const bf = new BloomFilter({
        redisSize: total/1000000,
        hashesNum: 5,
        redisKey: redis_key,
        redisClient: redisClient
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

let testCollapsePipeline = async () => {
    const redis_key = "testCollapsePipeline";
    const total = 10000;
    const redisClient = (new ioredis(6379, "localhost")).pipeline();
    redisClient.del(redis_key);

    const bf = new BloomFilter({
        redisSize: total/1000000,
        hashesNum: 5,
        redisKey: redis_key,
        redisClient: redisClient
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

helloWorld();
// testCollapse();
