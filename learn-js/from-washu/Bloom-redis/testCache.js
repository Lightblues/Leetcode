const ioredis = require("ioredis");
const BloomFilter = require('bloomfilter-redis');

const NOTE_ID_BLOOM_REDIS_KEY = "xiaohongshu_note_id_bloom";

const checkRawNotesDataExistsByRedisBloom = async (noteIds) => {
    // const EXPECTED_NOTE_TOTAL_NUMBER = 4E4;

    const bf = new BloomFilter({
        redisSize: 2048 ,  // 2GB
        hashesNum: 15,      // hash 数量
        redisKey: NOTE_ID_BLOOM_REDIS_KEY,
        redisClient: new ioredis(),
    });

    let promisesArray = [];
    noteIds.forEach(noteId => {
        promisesArray.push(bf.contains(noteId.toString()));
    });
    let filters = await Promise.all(promisesArray)
        // 返回形式：[ false, false, false ]
        // .then((res) => {
        //     console.log(res)
        // })
    // console.log(filters)
    for (let i = 0; i < noteIds.length; ++i) {
        // if (filters[i]) mCachedNoteIdSet.add(noteIds[i]);
        await bf.add(noteIds[i].toString());
    }
    return filters;
}


// test
(async ()=> {
    let res = await checkRawNotesDataExistsByRedisBloom(["1", "2", "z"]);
    console.log(res);
    // res = await checkRawNotesDataExistsByRedisBloom(["1", "2", "z"]);
    // console.log(res);
})();
