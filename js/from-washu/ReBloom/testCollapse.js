const { BloomFilter } = require("@albert-team/rebloom");
const ioredis = require("ioredis");
const key = "testCollapse";

const main = async () => {
    // 创建前先删除该 key
    const redisClient = new ioredis({
        host: "localhost",
        port: 6380,
    })
    await redisClient.del(key);
    await redisClient.disconnect();

    const filter = new BloomFilter(key, {
        host: 'localhost',
        port: 6380,
        // redisClientOptions: { password: 'scrtpassword' },
    });
    const total = 10000;
    await filter.connect();
    // 注意需要提前分配空间，否则碰撞概率较高
    await filter.reserve(0.0001, 10000);

    let startTime = Date.now();
    let collapseCounter = 0;
    for (let i=0; i<total; i++) {
        if (!(i%1000)){
            console.log(i);
        }
        if (await filter.exists(i)) {
            collapseCounter++;
        } else {
            await filter.add(i);
        }
    }

    console.log(`Collpase rate: ${collapseCounter/total}`);
    console.log(`Time used: ${(Date.now() - startTime)/1000}s`);

    await filter.disconnect();
}

main()
    .catch( err => {
        console.error(err);
    })
