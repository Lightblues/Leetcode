const { BloomFilter } = require("@albert-team/rebloom");
const ioredis = require("ioredis");
const NOTE_ID_BLOOM_REDIS_KEY = "xiaohongshu_note_id_bloom";

const checkRawNotesDataExistsByRedisBloom = async (noteIds) => {
    const redisClient = new ioredis({
        host: "localhost",
        port: 6380,
    })
    await redisClient.del(NOTE_ID_BLOOM_REDIS_KEY);
    await redisClient.disconnect();

    const bloomFilter = new BloomFilter(NOTE_ID_BLOOM_REDIS_KEY, {
        host: 'localhost',
        port: 6380,
    });

    await bloomFilter.connect();
    // 注意需要提前分配空间，否则碰撞概率较高
    const EXPECTED_NOTE_TOTAL_NUMBER = 4E12;
    await bloomFilter.reserve(1E-7, EXPECTED_NOTE_TOTAL_NUMBER);

    let res = await bloomFilter.mexists(noteIds);
    return res;
}

(async () => {
    const res = await checkRawNotesDataExistsByRedisBloom([1,2,3,4,5])
    console.log(res);
})();
