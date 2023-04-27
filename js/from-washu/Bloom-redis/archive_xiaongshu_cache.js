const BloomFilter = require('bloomfilter-redis');

const NOTE_ID_BLOOM_REDIS_KEY = "xiaohongshu_note_id_bloom";
const PROFILE_ID_BLOOM_REDIS_KEY = "xiaohongshu_profile_id_bloom";


const checkRawNotesDataExistsByRedisBloom = async (noteIds) => {
    // ref: <https://hur.st/bloomfilter/>
    // const EXPECTED_NOTE_TOTAL_NUMBER = 4E12;
    // 以下参数冲突概率为 p = 0.00000017 (1 in 5884220)
    const bf = new BloomFilter({
        redisSize: 2048 ,  // 2GB
        hashesNum: 15,
        redisKey: NOTE_ID_BLOOM_REDIS_KEY,
        redisClient: DBClients.mRedisClient.pipeline()
    });

    let promisesArray = [];
    noteIds.forEach(noteId => {
        promisesArray.push(bf.contains(noteId.toString()));
    });
    let filters = await Promise.all(promisesArray);
    // 加入内存缓存 和 Bloom 缓存
    for (let i = 0; i < noteIds.length; ++i) {
        if (filters[i]) mCachedNoteIdSet.add(noteIds[i]);
        await bf.add(noteIds[i].toString());
    }
    return filters;
};
