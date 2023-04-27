const { BloomFilter } = require('@albert-team/rebloom')

const main = async () => {
    const filter = new BloomFilter('filtername', {
        host: 'localhost',
        port: 6379,
        redisClientOptions: { password: 'scrtpassword' },
    })
    await filter.connect()

    console.log(await filter.add('item0')) // 1
    console.log(await filter.exists('item0')) // 1
    console.log(await filter.exists('item1')) // 0

    await filter.disconnect()
}

main().catch((err) => console.error(err))
